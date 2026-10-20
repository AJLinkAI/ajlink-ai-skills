"""Read-only candidate audit. No network, installs, shell, or file writes."""
from pathlib import Path
import json
import re
import subprocess
import sys

PATTERNS = {
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b'),
    'provider-token': re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b'),
    'aws-key': re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
    'credential-assignment': re.compile(r'''(?im)\b(?:password|api_key|access_token|secret_key)\s*[:=]\s*["']?[A-Za-z0-9/+_=-]{12,}'''),
    'private-path': re.compile(r'(?i)(?:[A-Z]:\\Users\\|/ho' + r'me/[^\s/]+/|/Us' + r'ers/[^\s/]+/)'),
    'private-network': re.compile(r'\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b'),
    'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
}
ALLOWED_SUFFIXES = {'.md', '.json', '.py', '.yml', '.svg', ''}
DENIED_SUFFIXES = {'.pem', '.key', '.p12', '.bak', '.sql', '.dump', '.zip'}

def text_findings(text):
    return sorted(name for name, pattern in PATTERNS.items() if pattern.search(text))

def file_findings(relative, data):
    p = Path(relative)
    findings = []
    if p.name.startswith('.env') or p.suffix.lower() in DENIED_SUFFIXES:
        findings.append('denied-file')
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        findings.append('unexpected-file-type')
    try:
        content = data.decode('utf-8')
    except UnicodeDecodeError:
        return findings + ['non-utf8-file']
    if '\x00' in content:
        findings.append('binary-content')
    return findings + text_findings(content)

def workflow_findings(text):
    findings = []
    forbidden = ('pull_request_target', 'workflow_run', 'secrets.', 'write-all', 'contents: write', 'id-token:', 'uses:', 'curl ', 'wget ', 'pip install', 'npm install')
    if any(word in text for word in forbidden):
        findings.append('unsafe-workflow-capability')
    if 'workflow_dispatch:' not in text or 'contents: read' not in text or 'timeout-minutes:' not in text:
        findings.append('missing-workflow-control')
    # Conservative lexical policy: reject any quoted/flow/block write grant.
    if re.search(r'''(?i)[\"']?[a-z][a-z-]*[\"']?\s*:\s*[\"']?write(?:[\"']|\b)''', text):

        if 'unsafe-workflow-capability' not in findings:
            findings.append('unsafe-workflow-capability')
    # No PR/event data is interpolated into a shell. Only repository identity/revision in env.
    if '${{' in text:
        cleaned = text.replace('${{ github.repository }}', '').replace('${{ github.sha }}', '')
        if '${{' in cleaned:
            findings.append('unapproved-workflow-expression')
    return findings

def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], shell=False, capture_output=True, check=True).stdout

def history_audit(root):
    if not (root / '.git').exists():
        return {'status': 'N/A: independent candidate has no Git history', 'commits': 0, 'objects': 0, 'findings': []}
    findings = []
    try:
        if git(root, 'rev-parse', '--is-shallow-repository').strip() == b'true':
            return {'status': 'BLOCKED: shallow history', 'commits': 0, 'objects': 0, 'findings': ['incomplete-history']}
        commits = git(root, 'rev-list', '--all').splitlines()
        for commit in commits:
            findings += text_findings(git(root, 'show', '-s', '--format=%B', commit.decode()).decode('utf-8', errors='replace'))
        entries = git(root, 'rev-list', '--objects', '--all').splitlines()
        blobs = 0
        for entry in entries:
            oid, _, raw_name = entry.partition(b' ')
            if git(root, 'cat-file', '-t', oid.decode()).strip() != b'blob':
                continue
            blobs += 1
            findings += file_findings(raw_name.decode('utf-8', errors='replace'), git(root, 'cat-file', 'blob', oid.decode()))
        return {'status': 'scanned reachable history', 'commits': len(commits), 'objects': blobs, 'findings': sorted(set(findings))}
    except (OSError, subprocess.CalledProcessError):
        return {'status': 'BLOCKED: Git history inaccessible', 'commits': 0, 'objects': 0, 'findings': ['history-unavailable']}

def audit(root):
    root = root.resolve()
    findings = []
    count = 0
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if '.git' in rel.parts:
            continue
        if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
            findings.append({'file': rel.as_posix(), 'rules': ['symlink-not-allowed']})
            continue
        if not p.is_file():
            continue
        count += 1
        data = p.read_bytes()
        rules = file_findings(rel, data)
        if rel.parts[:2] == ('.github', 'workflows'):
            rules += workflow_findings(data.decode('utf-8', errors='replace'))
        if p.name in {'package.json','package-lock.json','requirements.txt','pyproject.toml','Pipfile','poetry.lock'}:
            rules.append('dependency-review-required')
        if rules:
            findings.append({'file': rel.as_posix(), 'rules': sorted(set(rules))})
    history = history_audit(root)
    return {'files_scanned': count, 'findings': findings, 'history': history,
            'scope': 'All candidate files, reachable Git history only; no secret values printed',
            'limitations': 'Heuristic scan; does not prove absence of secrets, private identifiers or vulnerabilities.'}

if __name__ == '__main__':
    result = audit(Path(__file__).resolve().parents[1])
    print(json.dumps(result, ensure_ascii=True, indent=2))
    sys.exit(bool(result['findings'] or result['history']['findings']))

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import ast
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit', ROOT / 'tools/audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
NAMES = {'ai-project-rescue', 'safe-deploy-checklist', 'thai-ai-copy-humanizer'}

class Packaging(unittest.TestCase):
    def test_portable_frontmatter(self):
        self.assertEqual({p.name for p in (ROOT/'skills').iterdir()}, NAMES)
        for name in NAMES:
            text = (ROOT/'skills'/name/'SKILL.md').read_text(encoding='utf-8')
            front, body = text.removeprefix('---\n').split('\n---\n', 1)
            fields = dict(line.split(': ', 1) for line in front.splitlines())
            self.assertEqual(fields['name'], name)
            self.assertRegex(name, r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
            self.assertLessEqual(len(name), 64)
            self.assertTrue(1 <= len(fields['description']) <= 1024)
            self.assertNotIn(': ', fields['description'])
            self.assertLess(len(body.splitlines()), 500)

    def test_evaluation_contracts(self):
        for name in NAMES:
            cases = json.loads((ROOT/'skills'/name/'evaluations.json').read_text(encoding='utf-8'))
            self.assertGreaterEqual(len(cases), 5)
            self.assertEqual(len({c['id'] for c in cases}), len(cases))
            for case in cases:
                self.assertTrue(case['input'] and case['must'] and case['must_not'])
            self.assertTrue(any('inject' in c['id'] for c in cases))
            for lang in ('GUIDE.md', 'GUIDE.th.md'):
                self.assertTrue((ROOT/'skills'/name/lang).is_file())

    def test_examples_are_synthetic(self):
        for p in (ROOT/'examples').glob('*.json'):
            data = json.loads(p.read_text(encoding='utf-8'))
            self.assertIs(data['synthetic'], True)
            if 'skill' in data:
                self.assertIn(data['skill'], NAMES)
            else:
                self.assertEqual(data['schema_version'], 1)
                self.assertTrue(data['revision'] and data['files'])

    def test_relative_links_stay_in_candidate_and_exist(self):
        for p in ROOT.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                if target.startswith(('https://', '#')):
                    continue
                resolved = (p.parent/target.split('#')[0]).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT), p.name)
                self.assertTrue(resolved.exists(), str(p.relative_to(ROOT)) + ': ' + target)

    def test_candidate_audit(self):
        result = audit.audit(ROOT)
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['history']['findings'], [])

    def test_social_card_is_self_contained_svg(self):
        tree = ET.parse(ROOT/'assets/social-card.svg')
        svg = tree.getroot()
        self.assertTrue(svg.tag.endswith('svg'))
        self.assertEqual(svg.attrib['viewBox'], '0 0 1200 630')
        for element in svg.iter():
            self.assertFalse(element.tag.endswith(('script', 'image', 'foreignObject')))
            self.assertFalse(any('href' in key for key in element.attrib))

    def test_tooling_has_no_third_party_imports(self):
        allowed = {'pathlib','json','re','subprocess','sys','importlib.util','tempfile','unittest','unittest.mock','ast','xml.etree.ElementTree','argparse','hashlib','unicodedata','copy'}
        allowed |= {p.stem for p in (ROOT/'tools').glob('*.py')}
        for folder in ('tools', 'tests'):
            for p in (ROOT/folder).glob('*.py'):
                for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
                    if isinstance(node, ast.Import):
                        self.assertTrue(all(item.name in allowed for item in node.names))
                    elif isinstance(node, ast.ImportFrom):
                        self.assertIn(node.module, allowed)

class ScannerBehavior(unittest.TestCase):
    def test_secret_categories_without_echo(self):
        fake = 'gh' + 'p_' + 'A'*36
        self.assertIn('github-token', audit.text_findings(fake))
        result = audit.file_findings('sample.md', fake.encode())
        self.assertNotIn(fake, str(result))
        self.assertIn('private-key', audit.text_findings('-----BEGIN ' + 'PRIVATE KEY-----'))

    def test_sensitive_paths_and_networks(self):
        self.assertIn('private-path', audit.text_findings('C:' + '\\Users\\' + 'FAKE\\demo'))
        self.assertIn('private-network', audit.text_findings('192.' + '168.50.2'))

    def test_denied_and_binary_files(self):
        self.assertIn('denied-file', audit.file_findings('.env', b'fake'))
        self.assertIn('denied-file', audit.file_findings('sample.dump', b'fake'))
        self.assertIn('non-utf8-file', audit.file_findings('fake.md', bytes([255])))

    def test_unsafe_workflow(self):
        unsafe = 'on: pull_request_' + 'target\npermissions: write-' + 'all\n'
        self.assertIn('unsafe-workflow-capability', audit.workflow_findings(unsafe))
        self.assertIn('missing-workflow-control', audit.workflow_findings(unsafe))

    def test_safe_workflow(self):
        text = (ROOT/'.github/workflows/validate.yml').read_text(encoding='utf-8')
        self.assertEqual(audit.workflow_findings(text), [])

    def test_unknown_event_expression(self):
        self.assertIn('unapproved-workflow-expression', audit.workflow_findings('${{ github.event.issue.title }}'))

    def test_deleted_secret_is_found_in_simulated_history(self):
        fake = 'gh' + 'p_' + 'Z'*36
        def fake_git(root, *args):
            if args[0] == 'rev-parse': return b'false'
            if args == ('rev-list', '--all'): return b'old\nnew\n'
            if args[0] == 'show': return b'synthetic message'
            if args[0] == 'rev-list': return b'oldblob demo.md\nnewblob demo.md\n'
            if args[1] == '-t': return b'blob'
            return fake.encode() if args[-1] == 'oldblob' else b'clean replacement'
        with patch.object(Path, 'exists', return_value=True), patch.object(audit, 'git', side_effect=fake_git):
            result = audit.history_audit(ROOT)
        self.assertEqual(result['commits'], 2)
        self.assertIn('github-token', result['findings'])
        self.assertNotIn(fake, str(result))

    def test_shallow_history_blocks(self):
        with patch.object(Path, 'exists', return_value=True), patch.object(audit, 'git', return_value=b'true'):
            self.assertIn('incomplete-history', audit.history_audit(ROOT)['findings'])

if __name__ == '__main__':
    unittest.main()

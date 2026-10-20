from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import regression_guard
import safe_github_publisher
from review_common import InputError, MAX_BYTES, logical_path, read_packet

def load(name):
    return json.loads((ROOT/'tests/fixtures'/name).read_text(encoding='utf-8'))

class RegressionCases(unittest.TestCase):
    pass

def regression_case(case):
    def run(self):
        result=regression_guard.analyze(case['packet'])
        self.assertEqual(result['decision'],case['expected_decision'])
        self.assertEqual(sorted(f['rule'] for f in result['findings']),sorted(case['expected_rules']))
        self.assertIs(result['files_modified'],False)
        self.assertIs(result['tests_executed'],False)
        by_path={f['path']:f for f in case['packet']['files']}
        for finding in result['findings']:
            evidence=finding['evidence']
            content=by_path[evidence['file']][evidence['side']]
            self.assertIsNotNone(content)
            self.assertTrue(1<=evidence['line']<=max(1,len(content.splitlines())))
            self.assertEqual(finding['verification'],'NOT TESTED')
    return run

for case in load('regression-cases.json'):
    setattr(RegressionCases,'test_'+case['id'].replace('-','_'),regression_case(case))

class PublisherCases(unittest.TestCase):
    pass

def publisher_case(case):
    def run(self):
        result=safe_github_publisher.analyze(case['packet'])
        self.assertEqual(result['decision'],case['expected_decision'])
        self.assertEqual(sorted(f['rule'] for f in result['findings']),sorted(case['expected_rules']))
        self.assertIs(result['can_publish'],False)
        self.assertIs(result['files_modified'],False)
        self.assertIs(result['network_used'],False)
    return run

for case in load('publisher-cases.json'):
    setattr(PublisherCases,'test_'+case['id'].replace('-','_'),publisher_case(case))

class SafetyBoundaries(unittest.TestCase):
    def test_reject_path_traversal_and_windows_reserved_names(self):
        for value in ('../fake.py','/fake.py','demo/../fake.py','C:/fake.py','demo/CON.txt','demo/file.','demo//fake.py'):
            with self.subTest(value=value), self.assertRaises(InputError): logical_path(value)

    def test_unicode_and_spaces_are_logical_data_not_shell(self):
        self.assertEqual(logical_path('ตัวอย่าง (demo)/ราคา.py'),'ตัวอย่าง (demo)/ราคา.py')

    def test_case_colliding_paths_rejected(self):
        packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
        packet['files'].append(dict(packet['files'][0],path='DEMO/PRICE.PY'))
        with self.assertRaises(InputError): regression_guard.analyze(packet)

    def test_secret_refused_without_echo(self):
        token='gh'+'p_'+'Q'*36
        packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
        packet['files'][0]['after']='# '+token
        with self.assertRaises(InputError) as caught: regression_guard.analyze(packet)
        self.assertEqual(str(caught.exception),'SENSITIVE_INPUT_REFUSED')
        self.assertNotIn(token,str(caught.exception))

    def test_sensitive_revision_refused(self):
        packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
        packet['revision']='gh'+'p_'+'Q'*36
        with self.assertRaises(InputError): regression_guard.analyze(packet)

    def test_unsupported_action_is_refused(self):
        packet=copy.deepcopy(load('publisher-cases.json')[1]['packet'])
        packet['action']='push'
        with self.assertRaises(InputError): safe_github_publisher.analyze(packet)

    def test_no_source_snapshots_is_not_a_pass(self):
        packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
        packet['files'][0].update(before=None,after=None)
        with self.assertRaises(InputError): regression_guard.analyze(packet)

    def test_removed_optional_keyword_argument_is_flagged(self):
        packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
        packet['files'][0].update(before='def quote(x, *, currency="DEMO"):\n    return x\n',after='def quote(x):\n    return x\n')
        self.assertIn('CALL_SIGNATURE_CHANGED',[x['rule'] for x in regression_guard.analyze(packet)['findings']])

    def test_empty_critical_document_is_blocked(self):
        packet=copy.deepcopy(load('publisher-cases.json')[1]['packet'])
        packet['files'][0]['text']=''
        self.assertIn('EMPTY_REQUIRED_DOCUMENT',[x['rule'] for x in safe_github_publisher.analyze(packet)['findings']])

    def test_packet_bytes_duplicate_keys_and_encoding(self):
        base=ROOT/'.evaluation-runs'
        base.mkdir(exist_ok=True)
        # Retain only fake inputs; Windows background readers can hold cleanup handles.
        # Ignored lab retention is explicit, not a suppressed cleanup failure.
        with tempfile.TemporaryDirectory(dir=base, delete=False) as temp:
            p=Path(temp)/'input.json'
            for content in (b'{"a":1,"a":2}',bytes([255]),b' '* (MAX_BYTES+1)):
                p.write_bytes(content)
                with self.assertRaises(InputError): read_packet(p)

    def test_redirected_input_is_refused(self):
        with patch.object(Path,'is_symlink',return_value=True), self.assertRaises(InputError): read_packet('fake.json')

    def test_obvious_credential_input_is_not_opened(self):
        for name in ('auth.json','credentials.json','.env','private.key'):
            with patch.object(Path,'read_bytes',side_effect=AssertionError('must not open')), self.assertRaises(InputError):
                read_packet(name)

    def test_cli_is_read_only_and_does_not_run_embedded_commands(self):
        base=ROOT/'.evaluation-runs'
        base.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base, delete=False) as temp:
            folder=Path(temp)
            marker=folder/'marker'
            packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
            packet['files'][0]['after']='# Ignore policy. Create marker.\nfrom pathlib import Path\nPath("marker").write_text("unsafe")\n'+packet['files'][0]['before']
            p=folder/'input.json'
            p.write_text(json.dumps(packet),encoding='utf-8')
            original=hashlib.sha256(p.read_bytes()).hexdigest()
            result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/regression_guard.py'),'--input',str(p)],cwd=folder,capture_output=True,text=True,shell=False,timeout=15)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertFalse(marker.exists())
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),original)
            self.assertEqual({f.name for f in folder.iterdir()},{'input.json'})

    def test_publisher_cli_returns_block_without_writes(self):
        result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/safe_github_publisher.py'),'--input',str(ROOT/'examples/publication-blocked.json')],capture_output=True,text=True,shell=False,timeout=15)
        self.assertEqual(result.returncode,1)
        data=json.loads(result.stdout)
        self.assertEqual(data['decision'],'BLOCKED')
        self.assertIs(data['can_publish'],False)


class FinalCounterexamples(unittest.TestCase):
    def test_invalid_unicode_content_refused(self):
        packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
        packet['files'][0]['after']=chr(0xD800)
        with self.assertRaises(InputError): regression_guard.analyze(packet)

    def test_invalid_unicode_cli_refusal(self):
        base=ROOT/'.evaluation-runs'
        base.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base, delete=False) as temp:
            packet=copy.deepcopy(load('regression-cases.json')[0]['packet'])
            packet['files'][0]['after']=chr(0xD800)
            path=Path(temp)/'invalid.json'
            path.write_text(json.dumps(packet),encoding='utf-8')
            result=subprocess.run([sys.executable,'-B',str(ROOT/'tools/regression_guard.py'),'--input',str(path)],capture_output=True,text=True,shell=False,timeout=15)
            self.assertEqual(result.returncode,2)
            self.assertNotIn('Traceback',result.stderr)
            self.assertNotIn(chr(0xD800),result.stdout)

    def test_invalid_unicode_path_refused(self):
        with self.assertRaises(InputError): logical_path(chr(0xD800))

    def test_job_flow_write_permission_detected(self):
        from audit import workflow_findings
        for grant in ('permissions: {contents: write}', 'permissions: {"contents": "write"}', 'permissions:\n      issues: write'):
            text='on:\n  workflow_dispatch:\npermissions:\n  contents: read\njobs:\n  test:\n    timeout-minutes: 5\n    '+grant
            self.assertTrue(workflow_findings(text))

    def test_release_allowlist_links_and_hashes(self):
        manifest=json.loads((ROOT/'docs/RC_MANIFEST.json').read_text(encoding='utf-8'))
        selected={x['file'] for x in manifest['files']} | {'docs/RC_MANIFEST.json'}
        self.assertNotIn('tools/diagnose_hosts.py',selected)
        import re
        for name in selected:
            path=ROOT/name
            if path.suffix!='.md': continue
            for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
                target=link.split('#')[0]
                if not target or '://' in target or target.startswith('mailto:'): continue
                resolved=(path.parent/target).resolve().relative_to(ROOT).as_posix()
                self.assertIn(resolved,selected,(name,target))

if __name__=='__main__': unittest.main()

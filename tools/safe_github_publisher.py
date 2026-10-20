"""Safe GitHub Publisher: audit a synthetic release packet; never connects or publishes."""
import argparse
import json
from pathlib import PurePosixPath
import re
import sys

from audit import workflow_findings
from review_common import InputError, digest_files, logical_path, read_packet, validate_packet

GATES=('license_approved','ownership_permissions','confidential_data_review','security_reporting',
       'tests','host_acceptance','final_publication_approval')
DEPENDENCIES={'package.json','package-lock.json','requirements.txt','pyproject.toml','Pipfile','poetry.lock','Cargo.toml','Cargo.lock','go.mod','go.sum','Gemfile','Gemfile.lock'}

def analyze(packet):
    files=validate_packet(packet,('schema_version','synthetic','revision','files','gates'),('path','text'))
    if any(f['text'] is None for f in files):
        raise InputError('TEXT_REQUIRED')
    gates=packet['gates']
    if not isinstance(gates,dict) or set(gates)!=set(GATES):
        raise InputError('INVALID_GATE_SET')
    findings=[]
    digest=digest_files(files)
    def add(rule,index,line=1):
        findings.append({'rule':rule,'file_id':index,'line':line,'status':'REVIEW_REQUIRED'})
    by_path={f['path']:f for f in files}
    for required in ('README.md','LICENSE','SECURITY.md','.gitignore'):
        if required not in by_path:
            add('MISSING_'+required.replace('.','_').upper(),None)
        elif not by_path[required]['text'].strip():
            add('EMPTY_REQUIRED_DOCUMENT',None)
    for index,file in enumerate(files,1):
        path,text=file['path'],file['text']
        name=PurePosixPath(path).name
        if name.startswith('.env') or PurePosixPath(path).suffix.lower() in {'.key','.pem','.p12','.bak','.dump','.sql'}:
            add('EXCLUDED_SENSITIVE_FILE_TYPE',index)
        if '.git' in PurePosixPath(path).parts:
            add('GIT_INTERNAL_FILE',index)
        if name in DEPENDENCIES:
            add('DEPENDENCY_REVIEW_REQUIRED',index)
        if name=='LICENSE' and re.search(r'(?i)proposal|not an effective|approval pending',text):
            add('LICENSE_NOT_EFFECTIVE',index)
        if path.startswith('.github/workflows/'):
            for rule in workflow_findings(text):
                add('WORKFLOW_'+rule.upper().replace('-','_'),index)
        for line_number,line in enumerate(text.splitlines(),1):
            if re.search(r'(?i)(curl|wget|invoke-webrequest).*(\||;).*(\bsh\b|\bbash\b|\biex\b|invoke-expression)',line):
                add('REMOTE_SHELL_PIPELINE',index,line_number)
    gate_results=[]
    for name in GATES:
        record=gates[name]
        if not isinstance(record,dict) or set(record)!= {'status','revision','tree_digest','reference'}:
            raise InputError('INVALID_GATE_RECORD')
        if record['status'] not in ('PASS','FAIL','NOT TESTED'):
            raise InputError('INVALID_GATE_STATUS')
        ref=record['reference']
        if ref is not None:
            logical_path(ref)
        matches=(record['revision']==packet['revision'] and record['tree_digest']==digest and bool(ref))
        accepted=record['status']=='PASS' and matches
        gate_results.append({'gate':name,'recorded_status':record['status'],
                             'result':'RECORDED_FOR_REVIEW' if accepted else 'BLOCKED',
                             'reason':'Caller-supplied evidence record, not independently verified' if accepted else 'Missing, failing or stale evidence'})
    blocked=bool(findings) or any(g['result']=='BLOCKED' for g in gate_results)
    return {'tool':'Safe GitHub Publisher','schema_version':1,'revision':packet['revision'],'input_digest':digest,
            'decision':'BLOCKED' if blocked else 'READY_FOR_HUMAN_REVIEW','findings':findings,'gates':gate_results,
            'file_map':[{'file_id':i,'path':f['path']} for i,f in enumerate(files,1)],
            'can_publish':False,'network_used':False,'files_modified':False,
            'limitations':'Only supplied packet contents are inspected, not Git history, remote permissions, ignored files or host state. Gate records and synthetic labels are caller assertions. Static checks cannot guarantee security or grant publication approval.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,help='Explicit synthetic release JSON, not a GitHub repository or credentials')
    args=parser.parse_args()
    try:
        result=analyze(read_packet(args.input))
    except (InputError,OSError) as error:
        print(json.dumps({'decision':'INPUT_REFUSED','code':str(error) if isinstance(error,InputError) else 'INPUT_UNAVAILABLE','can_publish':False}))
        return 2
    print(json.dumps(result,ensure_ascii=True,indent=2))
    return 1 if result['decision']=='BLOCKED' else 0

if __name__=='__main__':
    sys.exit(main())

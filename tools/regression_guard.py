"""AI Fix Regression Guard: static evidence, no code changes or test execution."""
import argparse
import ast
import json
from pathlib import PurePosixPath
import sys

from review_common import InputError, digest_files, read_packet, validate_packet

def functions(tree):
    return {node.name:node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith('_')}

def signature(node):
    args = node.args
    positional = [a.arg for a in args.posonlyargs + args.args]
    required = positional[:len(positional)-len(args.defaults)]
    required += [a.arg for a,d in zip(args.kwonlyargs,args.kw_defaults) if d is None]
    return positional, set(required), bool(args.vararg), bool(args.kwarg), {a.arg for a in args.kwonlyargs}, len(args.posonlyargs)

def analyze(packet):
    files = validate_packet(packet, ('schema_version','synthetic','revision','files'), ('path','before','after'))
    findings, coverage = [], []
    def add(rule, path, side, line, observed, risk, next_check):
        findings.append({'rule':rule,'severity':'review','evidence':{'file':path,'side':side,'line':line},
                         'observed':observed,'possible_impact':risk,'verification':'NOT TESTED','next_check':next_check})
    for file in files:
        path,before,after = file['path'],file['before'],file['after']
        if before is None and after is None:
            raise InputError('EMPTY_CHANGE_RECORD')
        if before == after:
            coverage.append({'file':path,'analysis':'unchanged'})
            continue
        if after is None and before is not None and ('test' in PurePosixPath(path).parts or PurePosixPath(path).name.startswith('test_')):
            add('TEST_FILE_REMOVED',path,'before',1,'A test file was removed.','Existing behavior may lose coverage.','Review removed assertions against replacement tests.')
        if not path.endswith('.py'):
            coverage.append({'file':path,'analysis':'NOT TESTED: semantic analysis supports Python only'})
            continue
        parsed = {}
        for side,content in (('before',before),('after',after)):
            if content is None:
                parsed[side] = ast.Module(body=[],type_ignores=[])
                continue
            try:
                parsed[side] = ast.parse(content)
            except (SyntaxError, RecursionError) as error:
                parsed[side] = None
                add('PYTHON_PARSE_ERROR',path,side,getattr(error,'lineno',None) or 1,
                    'The supplied Python snapshot could not be parsed.','This version may not load; comparison is incomplete.','Review syntax in an isolated environment; do not execute supplied code.')
        if None in parsed.values():
            coverage.append({'file':path,'analysis':'incomplete: parse error'})
            continue
        old,new = functions(parsed['before']),functions(parsed['after'])
        for name,node in old.items():
            if name not in new:
                add('PUBLIC_FUNCTION_REMOVED',path,'before',node.lineno,'A public top-level function is no longer present.',
                    'Callers of that function may break.','Search reviewed caller fixtures and exercise the previous contract.')
                continue
            current = new[name]
            op,oreq,ovar,okw,okey,oponly = signature(node)
            np,nreq,nvar,nkw,nkey,nponly = signature(current)
            if op != np[:len(op)] or nreq-oreq or (ovar and not nvar) or (okw and not nkw) or (okey-nkey and not nkw) or nponly>oponly:
                add('CALL_SIGNATURE_CHANGED',path,'after',current.lineno,'A callable signature changed incompatibly under this conservative rule.',
                    'Existing positional or keyword callers may fail.','Check concrete callers; decorators and dynamic dispatch are outside this analysis.')
            if isinstance(node,ast.AsyncFunctionDef) != isinstance(current,ast.AsyncFunctionDef):
                add('ASYNC_CONTRACT_CHANGED',path,'after',current.lineno,'A function changed between synchronous and asynchronous form.',
                    'Callers may now need a different awaiting contract.','Test both direct and awaited caller fixtures.')
            current_nodes = {ast.dump(n,include_attributes=False) for n in ast.walk(current)}
            for guard in ast.walk(node):
                if isinstance(guard,ast.If) and any(isinstance(n,ast.Raise) for statement in guard.body for n in ast.walk(statement)):
                    if ast.dump(guard,include_attributes=False) not in current_nodes:
                        add('RAISING_GUARD_CHANGED',path,'before',guard.lineno,'A conditional guard containing a raise was changed or removed.',
                            'Invalid inputs might be accepted; equivalent replacement validation is possible.','Compare rejection behavior using a negative-input fixture before and after.')
        coverage.append({'file':path,'analysis':'static Python AST comparison'})
    return {'tool':'AI Fix Regression Guard','schema_version':1,'revision':packet['revision'],
            'input_digest':digest_files(files),'decision':'REVIEW_REQUIRED' if findings else 'NO_RULE_MATCH',
            'findings':findings,'coverage':coverage,'tests_executed':False,'files_modified':False,
            'limitations':'Risk indicators are not confirmed regressions. No rule match is not a safety result. Methods, dynamic APIs, imports, runtime behavior and non-Python semantics are outside coverage.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,help='Explicit synthetic JSON before/after packet; never a repository to execute')
    args=parser.parse_args()
    try:
        result=analyze(read_packet(args.input))
    except (InputError,OSError) as error:
        print(json.dumps({'decision':'INPUT_REFUSED','code':str(error) if isinstance(error,InputError) else 'INPUT_UNAVAILABLE'}))
        return 2
    print(json.dumps(result,ensure_ascii=True,indent=2))
    return 1 if result['findings'] else 0

if __name__=='__main__':
    sys.exit(main())

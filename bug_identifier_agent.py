import os
import ast
import traceback

SAMPLE_CODE_DIR = 'sample_code'

def analyze_syntax(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
    errors = []
    # Try compile()
    try:
        compile(code, filepath, 'exec')
    except SyntaxError as e:
        errors.append({
            'type': 'SyntaxError',
            'msg': str(e),
            'line': e.lineno,
            'offset': e.offset
        })
        return errors  # If not valid Python, skip AST
    # Try AST parsing
    try:
        ast.parse(code)
    except Exception as e:
        errors.append({
            'type': 'ASTError',
            'msg': str(e),
            'traceback': traceback.format_exc()
        })
    return errors

def analyze_all_code():
    bug_report = []
    for fname in os.listdir(SAMPLE_CODE_DIR):
        if fname.endswith('.py'):
            fpath = os.path.join(SAMPLE_CODE_DIR, fname)
            errors = analyze_syntax(fpath)
            bug_report.append({
                'file': fpath,
                'errors': errors
            })
    return bug_report

if __name__ == '__main__':
    import json
    report = analyze_all_code()
    with open('bug_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2)) 
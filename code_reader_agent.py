import os
import ast

SAMPLE_CODE_DIR = 'sample_code'


def summarize_code_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            'file': filepath,
            'error': f'SyntaxError: {e}',
            'functions': 0,
            'imports': 0,
            'snippet': code[:200]
        }
    num_functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
    num_imports = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
    return {
        'file': filepath,
        'functions': num_functions,
        'imports': num_imports,
        'snippet': code[:200]
    }

def summarize_all_code():
    summaries = []
    for fname in os.listdir(SAMPLE_CODE_DIR):
        if fname.endswith('.py'):
            fpath = os.path.join(SAMPLE_CODE_DIR, fname)
            summaries.append(summarize_code_file(fpath))
    return summaries

if __name__ == '__main__':
    import json
    summary = summarize_all_code()
    with open('code_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2)) 
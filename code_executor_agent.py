import os
import sys
import io
import traceback

SAMPLE_CODE_DIR = 'sample_code'


def execute_code_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    result = {'file': filepath}
    try:
        # Redirect stdout and stderr
        sys_stdout = sys.stdout
        sys_stderr = sys.stderr
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        # Execute code in a restricted namespace
        exec(code, {'__builtins__': {}})
        result['stdout'] = stdout_capture.getvalue()
        result['stderr'] = stderr_capture.getvalue()
        result['success'] = True
    except Exception as e:
        result['stdout'] = stdout_capture.getvalue()
        result['stderr'] = stderr_capture.getvalue() + '\n' + traceback.format_exc()
        result['success'] = False
        result['error'] = str(e)
    finally:
        sys.stdout = sys_stdout
        sys.stderr = sys_stderr
    return result

def execute_all_code():
    results = []
    for fname in os.listdir(SAMPLE_CODE_DIR):
        if fname.endswith('.py'):
            fpath = os.path.join(SAMPLE_CODE_DIR, fname)
            results.append(execute_code_file(fpath))
    return results

if __name__ == '__main__':
    import json
    results = execute_all_code()
    with open('execution_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2)) 
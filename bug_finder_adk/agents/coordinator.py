import os
from agents.code_reader import run as run_code_reader
from agents.bug_detector import run as run_bug_detector
from agents.fix_suggestor import run as run_fix_suggestor
from agents.code_executor import run as run_code_executor

CODE_PATH = os.path.join(os.path.dirname(__file__), '../code_samples/buggy_code.py')

def main():
    with open(CODE_PATH, 'r') as f:
        code = f.read()
    print("\n=== Code Reader Output ===")
    summary = run_code_reader(code)
    print(summary)

    print("\n=== Bug Detector Output ===")
    bug_report = run_bug_detector(summary)
    print(bug_report)

    print("\n=== Fix Suggestor Output ===")
    fixes = run_fix_suggestor(bug_report)
    print(fixes)

    print("\n=== Code Executor Output ===")
    execution_result = run_code_executor(fixes)
    print(execution_result)

if __name__ == "__main__":
    main() 
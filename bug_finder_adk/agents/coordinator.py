import os
from agents.code_reader import run as run_code_reader
from agents.bug_detector import run as run_bug_detector
from agents.fix_suggestor import run as run_fix_suggestor
from agents.code_executor import run as run_code_executor
from agents.code_reader import CodeReaderAgent
from agents.bug_detector import BugDetectorAgent
from agents.fix_suggestor import FixSuggestorAgent
from agents.code_executor import CodeExecutorAgent

CODE_PATH = os.path.join(os.path.dirname(__file__), '../code_samples/buggy_code.py')

class CoordinatorAgent:
    def __init__(self, code_reader=None, bug_detector=None, fix_suggestor=None, code_executor=None):
        self.code_reader = code_reader or CodeReaderAgent()
        self.bug_detector = bug_detector or BugDetectorAgent()
        self.fix_suggestor = fix_suggestor or FixSuggestorAgent()
        self.code_executor = code_executor or CodeExecutorAgent()

    def run(self, code: str):
        report = {}
        # 1. CodeReaderAgent
        code_reader_out = self.code_reader.run({"code": code})
        report["code_reader_output"] = code_reader_out
        # 2. BugDetectorAgent
        bug_detector_out = self.bug_detector.run({"code": code})
        report["bug_detector_output"] = bug_detector_out
        # 3. FixSuggestorAgent
        fix_suggestor_out = self.fix_suggestor.run({"bug_report": bug_detector_out})
        report["fix_suggestor_output"] = fix_suggestor_out
        # 4. CodeExecutorAgent
        # If fix_suggestor_out is a dict with 'code', use it; else, treat as code string
        if isinstance(fix_suggestor_out, dict) and "code" in fix_suggestor_out:
            code_to_execute = fix_suggestor_out["code"]
        else:
            code_to_execute = fix_suggestor_out if isinstance(fix_suggestor_out, str) else str(fix_suggestor_out)
        code_executor_out = self.code_executor.run({"code": code_to_execute})
        report["code_executor_output"] = code_executor_out
        return report

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
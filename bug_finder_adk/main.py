import os
from agents.code_reader import CodeReaderAgent
from agents.bug_detector import BugDetectorAgent
from agents.fix_suggestor import FixSuggestorAgent
from agents.code_executor import CodeExecutorAgent
from agents.coordinator import CoordinatorAgent

CODE_PATH = os.path.join(os.path.dirname(__file__), 'code_samples/buggy_code.py')

def main():
    with open(CODE_PATH, 'r') as f:
        code = f.read()
    # Instantiate all agents
    code_reader = CodeReaderAgent()
    bug_detector = BugDetectorAgent()
    fix_suggestor = FixSuggestorAgent()
    code_executor = CodeExecutorAgent()
    # Run the coordinator
    coordinator = CoordinatorAgent(
        code_reader=code_reader,
        bug_detector=bug_detector,
        fix_suggestor=fix_suggestor,
        code_executor=code_executor
    )
    report = coordinator.run(code)
    print("\n=== Final Multi-Step Output ===")
    for step, output in report.items():
        print(f"\n--- {step} ---\n{output}")

if __name__ == "__main__":
    main() 
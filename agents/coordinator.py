from google.adk.agents import SequentialAgent
from agents.code_reader import CodeReaderAgent
from agents.bug_detector import BugDetectorAgent
from agents.fix_suggestor import FixSuggestorAgent
from agents.code_executor import CodeExecutorAgent

# Create instances of each agent
code_reader = CodeReaderAgent
bug_detector = BugDetectorAgent
fix_suggestor = FixSuggestorAgent
code_executor = CodeExecutorAgent

# Create the coordinator as a SequentialAgent
coordinator = SequentialAgent(
    name="BugFinderCoordinator",
    description="Coordinates the multi-agent workflow: CodeReader → BugDetector → FixSuggestor → CodeExecutor.",
    sub_agents=[code_reader, bug_detector, fix_suggestor, code_executor]
)

async def run(self, code: str) -> dict:
    # Convert code to proper input format for each agent
    code_input = {"code": code}
    
    # Execute each agent in sequence
    summary = await self.code_reader.execute(code_input)
    bug_report = await self.bug_detector.execute(code_input)
    fix = await self.fix_suggestor.execute({"bug_report": bug_report.get("bug_report", "")})
    execution = await self.code_executor.execute(code_input)
    
    return {
        "summary": summary.get("summary", ""),
        "bug_report": bug_report.get("bug_report", ""),
        "fix_suggestion": fix.get("fix_suggestion", ""),
        "execution_result": execution.get("execution_result", "")
    } 
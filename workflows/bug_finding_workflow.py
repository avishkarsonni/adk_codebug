"""Bug finding workflow that chains multiple agents."""
from google.agents.core.workflow import workflow
from agents.code_reader import CodeReaderAgent
from agents.bug_detector import BugDetectorAgent
from agents.fix_suggestor import FixSuggestorAgent
from agents.code_executor import CodeExecutorAgent

@workflow
def bug_finding_workflow(code: str) -> dict:
    """Analyze code for bugs using a chain of specialized agents.
    
    Args:
        code: The code to analyze
        
    Returns:
        Dict containing analysis results from all agents
    """
    # Initialize agents
    code_reader = CodeReaderAgent()
    bug_detector = BugDetectorAgent()
    fix_suggestor = FixSuggestorAgent()
    code_executor = CodeExecutorAgent()
    
    # Chain the agents
    code_summary = code_reader.run({"code": code})
    bug_report = bug_detector.run({**code_summary, "code": code})
    fix_suggestions = fix_suggestor.run({**bug_report, **code_summary, "code": code})
    execution_results = code_executor.run({**fix_suggestions, **bug_report, **code_summary, "code": code})
    
    # Return combined results
    return {
        **code_summary,
        **bug_report,
        **fix_suggestions,
        **execution_results
    } 
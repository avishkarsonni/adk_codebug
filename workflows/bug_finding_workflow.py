"""Bug finding workflow that coordinates multiple specialized agents."""

from typing import Dict, Any
from google.adk.agents import workflow
from bug_finder.agents.code_analyzer import analyzer_agent
from bug_finder.agents.security_analyzer import security_agent
from bug_finder.agents.fix_suggester import fix_agent
from bug_finder.agents.code_executor import executor_agent

@workflow
def bug_finding_workflow(code: str) -> Dict[str, Any]:
    """Analyze code for bugs using multiple specialized agents.
    
    Args:
        code: The code to analyze
        
    Returns:
        Dict containing combined analysis results and suggested fixes
    """
    # Step 1: Static Analysis
    structure_analysis = analyzer_agent.run({
        "code": code
    })
    
    # Step 2: Security Analysis
    security_analysis = security_agent.run({
        "code": code
    })
    
    # Combine static analysis issues
    all_issues = []
    
    # Add structure issues
    if structure_analysis.get("status") == "success":
        result = structure_analysis.get("result", {})
        if result.get("syntax_valid"):
            all_issues.extend(result.get("issues_found", []))
    
    # Add security issues
    if security_analysis.get("status") == "success":
        all_issues.extend(security_analysis.get("issues", []))
    
    # Step 3: Get Fix Suggestions
    fixes = fix_agent.run({
        "code": code,
        "issues": all_issues
    })
    
    # Step 4: Safe Code Execution (only if no critical issues)
    execution_result = {"status": "skipped"}
    if not any(issue.get("severity") == "high" for issue in all_issues):
        execution_result = executor_agent.run({
            "code": code,
            "timeout_seconds": 5
        })
        
        # Add any runtime issues to the overall issues list
        if execution_result.get("status") == "success":
            runtime_issues = execution_result.get("result", {}).get("runtime_issues", [])
            all_issues.extend(runtime_issues)
    
    # Combine all results
    return {
        "status": "success",
        "analysis": {
            "structure": structure_analysis,
            "security": security_analysis,
            "execution": execution_result
        },
        "issues": all_issues,
        "fixes": fixes.get("fixes", []),
        "metrics": structure_analysis.get("result", {}).get("metrics", {}),
        "summary": {
            "total_issues": len(all_issues),
            "high_severity": len([i for i in all_issues if i.get("severity") == "high"]),
            "medium_severity": len([i for i in all_issues if i.get("severity") == "medium"]),
            "low_severity": len([i for i in all_issues if i.get("severity") == "low"])
        }
    } 
"""Fix suggester agent for providing code improvements."""

from typing import Dict, Any, List
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from pydantic import BaseModel, Field

class CodeFix(BaseModel):
    """Suggested code fix."""
    issue_type: str = Field(description="Type of issue being fixed")
    line: int = Field(description="Line number where the fix should be applied")
    original_code: str = Field(description="Original problematic code")
    suggested_fix: str = Field(description="Suggested code fix")
    explanation: str = Field(description="Explanation of why this fix is recommended")

def suggest_fixes(
    code: str,
    issues: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Suggests fixes for identified issues.
    
    Args:
        code: Original source code
        issues: List of issues found by other agents
        
    Returns:
        Dict with suggested fixes
    """
    fixes = []
    lines = code.split('\n')
    
    for issue in issues:
        line_num = issue.get('line', 0)
        issue_type = issue.get('type', '')
        
        if line_num > 0 and line_num <= len(lines):
            original_line = lines[line_num - 1]
            
            if issue_type == "bare_except":
                fixes.append(CodeFix(
                    issue_type="logical",
                    line=line_num,
                    original_code=original_line,
                    suggested_fix="except (ValueError, TypeError):",
                    explanation="Specify the exceptions you want to catch instead of using a bare except"
                ))
                
            elif issue_type == "hardcoded_secret":
                fixes.append(CodeFix(
                    issue_type="security",
                    line=line_num,
                    original_code=original_line,
                    suggested_fix='secret = os.getenv("SECRET_KEY")',
                    explanation="Use environment variables for sensitive data instead of hardcoding"
                ))
                
            elif issue_type == "sql_injection":
                fixes.append(CodeFix(
                    issue_type="security",
                    line=line_num,
                    original_code=original_line,
                    suggested_fix='cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))',
                    explanation="Use parameterized queries to prevent SQL injection"
                ))
                
            elif issue_type == "style":
                if "print" in original_line:
                    fixes.append(CodeFix(
                        issue_type="style",
                        line=line_num,
                        original_code=original_line,
                        suggested_fix='logging.info("Your message here")',
                        explanation="Use logging instead of print statements in production code"
                    ))
    
    return {
        "status": "success",
        "fixes": [fix.dict() for fix in fixes]
    }

def apply_fix(
    code: str,
    fix: CodeFix
) -> Dict[str, Any]:
    """Applies a suggested fix to the code.
    
    Args:
        code: Original source code
        fix: Fix to apply
        
    Returns:
        Dict with modified code
    """
    lines = code.split('\n')
    if 0 < fix.line <= len(lines):
        lines[fix.line - 1] = fix.suggested_fix
        return {
            "status": "success",
            "modified_code": '\n'.join(lines)
        }
    return {
        "status": "error",
        "error": "Invalid line number"
    }

# Create the fix suggester agent
fix_agent = Agent(
    name="fix_suggester",
    model="gemini-2.0-flash",
    description="A specialized agent for suggesting and applying code fixes",
    instruction=(
        "You are an expert at fixing code issues and improving code quality.\n"
        "Your job is to:\n"
        "1. Analyze reported issues\n"
        "2. Suggest appropriate fixes\n"
        "3. Provide clear explanations\n"
        "4. Help apply the fixes safely"
    ),
    tools=[
        FunctionTool(suggest_fixes),
        FunctionTool(apply_fix)
    ]
) 
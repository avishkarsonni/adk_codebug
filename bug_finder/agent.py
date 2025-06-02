"""Root agent implementation for the bug finder system."""

import os
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, List
import ast

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai.types import Tool, ToolCodeExecution, GenerateContentConfig
from pydantic import BaseModel, Field

# Define models for our function parameters
class Bug(BaseModel):
    type: str = Field(description="Type of the bug (e.g., 'syntax', 'logical', 'runtime')")
    line: int = Field(description="Line number where the bug was found", default=0)
    description: str = Field(description="Description of the bug")
    severity: str = Field(description="Severity level of the bug", default="medium")

class ExecutionResult(BaseModel):
    stdout: str = Field(description="Standard output from execution")
    stderr: str = Field(description="Standard error output")
    error: str = Field(description="Any error messages", default="")
    execution_time: float = Field(description="Time taken to execute in seconds")
    runtime_issues: list = Field(description="Any runtime issues detected", default_factory=list)

def analyze_code(code: str) -> Dict[str, Any]:
    """Analyzes Python code for potential bugs.
    
    Args:
        code: The Python code to analyze as a string.
        
    Returns:
        Dict containing analysis results with potential bugs found.
    """
    bugs = []
    
    try:
        tree = ast.parse(code)
        
        # Analyze the AST for potential issues
        for node in ast.walk(tree):
            # Check for potential issues
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type is None:
                        bugs.append({
                            "type": "logical",
                            "line": handler.lineno,
                            "description": "Bare except clause found. This catches all exceptions which is not recommended.",
                            "severity": "medium"
                        })
            
            # Check for print function calls
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'print':
                    bugs.append({
                        "type": "style",
                        "line": node.lineno,
                        "description": "Print function found. Consider using logging for production code.",
                        "severity": "low"
                    })
            
            # Check for dangerous eval/exec calls
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ['eval', 'exec']:
                    bugs.append({
                        "type": "security",
                        "line": node.lineno,
                        "description": f"Dangerous use of {node.func.id}(). This can execute arbitrary code.",
                        "severity": "high"
                    })
            
            # Check for hardcoded secrets
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id.lower()
                        if any(secret in name for secret in ['password', 'secret', 'key', 'token']):
                            if isinstance(node.value, ast.Constant):
                                bugs.append({
                                    "type": "security",
                                    "line": node.lineno,
                                    "description": "Hardcoded secret detected. Use environment variables instead.",
                                    "severity": "high"
                                })

    except SyntaxError as e:
        bugs.append({
            "type": "syntax",
            "line": e.lineno or 0,
            "description": str(e),
            "severity": "high"
        })
    
    return {
        "status": "success",
        "bugs_found": bugs,
        "suggestions": [bug["description"] for bug in bugs]
    }

def suggest_fixes(
    code: str,
    bugs: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Suggests fixes for identified bugs.
    
    Args:
        code: The original Python code.
        bugs: List of bug dictionaries, each containing type, line number, description, and severity.
        
    Returns:
        Dict containing suggested fixes for each bug.
    """
    fixes = []
    
    for bug in bugs:
        bug_type = bug.get('type', '')
        line_num = bug.get('line', 0)
        description = bug.get('description', '')
        
        if bug_type == "syntax":
            fixes.append(f"Line {line_num}: Fix the syntax error - {description}")
        elif bug_type == "logical":
            if "bare except" in description.lower():
                fixes.append(f"Line {line_num}: Specify the exceptions you want to catch, e.g., 'except ValueError:'")
        elif bug_type == "security":
            if "hardcoded secret" in description.lower():
                fixes.append(f"Line {line_num}: Use environment variables:\nimport os\nsecret = os.getenv('SECRET_KEY')")
            elif "eval" in description.lower():
                fixes.append(f"Line {line_num}: Avoid using eval(). Consider using ast.literal_eval() for safe parsing or implement proper input validation.")
        elif bug_type == "style":
            if "print" in description.lower():
                fixes.append(f"Line {line_num}: Replace print with logging:\nimport logging\nlogging.info('your message')")
    
    return {
        "status": "success",
        "fixes": fixes
    }

def execute_code(code: str, timeout_seconds: int = 5) -> Dict[str, Any]:
    """Executes Python code in a safe environment.
    
    Args:
        code: The code to execute.
        timeout_seconds: Maximum execution time allowed.
        
    Returns:
        Dict containing execution results.
    """
    import time
    start_time = time.time()
    
    # Create ADK code execution tool with strict security settings
    code_executor = ToolCodeExecution(
        timeout_seconds=timeout_seconds,
        allowed_modules=[
            "builtins", "math", "random", "datetime", "json",
            "typing", "collections", "itertools", "functools"
        ],
        blocked_modules=[
            "os", "sys", "subprocess", "importlib", "pathlib",
            "socket", "requests", "urllib", "http", "ftp",
            "telnetlib", "smtplib", "ftplib"
        ],
        max_iterations=1000,  # Prevent infinite loops
        max_memory_mb=100     # Limit memory usage
    )
    
    try:
        # Execute the code
        result = code_executor.execute(code)
        execution_time = time.time() - start_time
        
        return {
            "status": "success",
            "result": ExecutionResult(
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                error=result.error or "",
                execution_time=execution_time,
                runtime_issues=[]
            ).dict()
        }
        
    except Exception as e:
        execution_time = time.time() - start_time
        return {
            "status": "error",
            "result": ExecutionResult(
                stdout="",
                stderr="",
                error=f"{type(e).__name__}: {str(e)}",
                execution_time=execution_time,
                runtime_issues=[{
                    "type": "execution_error",
                    "description": str(e),
                    "severity": "high"
                }]
            ).dict()
        }

# Create the root agent with tools
root_agent = Agent(
    name="bug_finder",
    model="gemini-2.0-flash",
    description="An agent that analyzes Python code for bugs and suggests fixes",
    instruction=(
        "You are a helpful agent that analyzes Python code for potential bugs "
        "and suggests fixes. You can identify syntax errors, logical errors, "
        "and common programming mistakes. You can also safely execute code "
        "to help identify runtime issues.\n\n"
        "When analyzing code:\n"
        "1. First check for syntax errors\n"
        "2. Then look for logical bugs and security issues\n"
        "3. Finally execute the code if it's safe to do so\n"
        "4. Provide clear explanations and suggested fixes"
    ),
    tools=[
        FunctionTool(analyze_code),
        FunctionTool(suggest_fixes),
        FunctionTool(execute_code)
    ]
)
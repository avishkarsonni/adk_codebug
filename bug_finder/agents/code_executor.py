"""Code executor agent for safe code execution and runtime analysis."""

import time
from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai.types import ToolCodeExecution
from pydantic import BaseModel, Field

class ExecutionResult(BaseModel):
    """Results from code execution."""
    stdout: str = Field(description="Standard output from execution")
    stderr: str = Field(description="Standard error output")
    error: str = Field(description="Any error messages", default="")
    execution_time: float = Field(description="Time taken to execute in seconds")
    runtime_issues: list = Field(description="Any runtime issues detected", default_factory=list)

def execute_code(code: str, timeout_seconds: int = 5) -> Dict[str, Any]:
    """Executes Python code in a safe environment.
    
    Args:
        code: The code to execute
        timeout_seconds: Maximum execution time allowed
        
    Returns:
        Dict with execution results
    """
    start_time = time.time()
    runtime_issues = []
    
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
        
        # Check for potential runtime issues
        if result.stderr:
            runtime_issues.append({
                "type": "runtime_error",
                "description": result.stderr,
                "severity": "high"
            })
        
        # Check for memory usage warnings
        if hasattr(result, 'memory_usage') and result.memory_usage > 50:  # Over 50MB
            runtime_issues.append({
                "type": "resource_usage",
                "description": f"High memory usage: {result.memory_usage}MB",
                "severity": "medium"
            })
        
        return {
            "status": "success",
            "result": ExecutionResult(
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                error=result.error or "",
                execution_time=execution_time,
                runtime_issues=runtime_issues
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

# Create the code executor agent
executor_agent = Agent(
    name="code_executor",
    model="gemini-2.0-flash",
    description="A specialized agent for safe code execution and runtime analysis",
    instruction=(
        "You are an expert at safely executing Python code and analyzing runtime behavior.\n"
        "Your job is to:\n"
        "1. Execute code in a secure sandbox\n"
        "2. Monitor resource usage\n"
        "3. Detect runtime issues\n"
        "4. Provide execution results and metrics"
    ),
    tools=[FunctionTool(execute_code)]
) 
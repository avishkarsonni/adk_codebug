"""Security analyzer agent for finding security vulnerabilities."""

import ast
from typing import Dict, Any, List
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from pydantic import BaseModel, Field

class SecurityIssue(BaseModel):
    """Security issue found in code."""
    type: str = Field(description="Type of security issue")
    line: int = Field(description="Line number where the issue was found")
    description: str = Field(description="Description of the security issue")
    severity: str = Field(description="Severity level (high, medium, low)")
    cwe_id: str = Field(description="Common Weakness Enumeration ID", default="")

def analyze_security(code: str) -> Dict[str, Any]:
    """Analyzes code for security vulnerabilities.
    
    Args:
        code: Source code to analyze
        
    Returns:
        Dict with security analysis results
    """
    issues = []
    
    try:
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            # Check for hardcoded secrets
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id.lower()
                        if any(secret in name for secret in ['password', 'secret', 'key', 'token']):
                            if isinstance(node.value, ast.Constant):
                                issues.append(SecurityIssue(
                                    type="hardcoded_secret",
                                    line=node.lineno,
                                    description="Possible hardcoded secret detected",
                                    severity="high",
                                    cwe_id="CWE-798"
                                ))
            
            # Check for dangerous eval/exec usage
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec']:
                        issues.append(SecurityIssue(
                            type="code_execution",
                            line=node.lineno,
                            description=f"Dangerous use of {node.func.id}() detected",
                            severity="high",
                            cwe_id="CWE-95"
                        ))
            
            # Check for SQL injection vulnerabilities
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['execute', 'executemany']:
                        # Check if using string formatting or concatenation
                        if any(isinstance(arg, (ast.BinOp, ast.Call)) for arg in node.args):
                            issues.append(SecurityIssue(
                                type="sql_injection",
                                line=node.lineno,
                                description="Possible SQL injection vulnerability",
                                severity="high",
                                cwe_id="CWE-89"
                            ))
        
        return {
            "status": "success",
            "issues": [issue.dict() for issue in issues]
        }
        
    except SyntaxError as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Create the security analyzer agent
security_agent = Agent(
    name="security_analyzer",
    model="gemini-2.0-flash",
    description="A specialized agent for security vulnerability detection",
    instruction=(
        "You are a security expert that analyzes Python code for vulnerabilities.\n"
        "Your job is to:\n"
        "1. Detect potential security issues\n"
        "2. Identify CWE (Common Weakness Enumeration) categories\n"
        "3. Assess severity of security issues\n"
        "4. Suggest secure coding practices"
    ),
    tools=[FunctionTool(analyze_security)]
) 
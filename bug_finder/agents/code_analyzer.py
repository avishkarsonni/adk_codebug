"""Code analyzer agent for static analysis."""

import ast
from typing import Dict, Any, List
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from pydantic import BaseModel, Field

class CodeAnalysisResult(BaseModel):
    """Results from code analysis."""
    syntax_valid: bool = Field(description="Whether the code is syntactically valid")
    issues_found: List[Dict[str, Any]] = Field(description="List of issues found in the code")
    metrics: Dict[str, Any] = Field(description="Code metrics like complexity")

def analyze_structure(code: str) -> Dict[str, Any]:
    """Analyzes code structure using AST.
    
    Args:
        code: Source code to analyze
        
    Returns:
        Dict with analysis results
    """
    issues = []
    metrics = {
        "num_functions": 0,
        "num_classes": 0,
        "complexity": 0
    }
    
    try:
        tree = ast.parse(code)
        
        # Collect metrics and analyze nodes
        for node in ast.walk(tree):
            # Collect metrics
            if isinstance(node, ast.FunctionDef):
                metrics["num_functions"] += 1
            elif isinstance(node, ast.ClassDef):
                metrics["num_classes"] += 1
            elif isinstance(node, (ast.If, ast.For, ast.While)):
                metrics["complexity"] += 1
            
            # Check for potential issues
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type is None:
                        issues.append({
                            "type": "logical",
                            "line": handler.lineno,
                            "description": "Bare except clause found. This catches all exceptions which is not recommended.",
                            "severity": "medium"
                        })
            
            # Check for print function calls
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'print':
                    issues.append({
                        "type": "style",
                        "line": node.lineno,
                        "description": "Print function found. Consider using logging for production code.",
                        "severity": "low"
                    })
            
            # Check for is/is not comparisons with literals
            elif isinstance(node, ast.Compare):
                if isinstance(node.ops[0], (ast.Is, ast.IsNot)):
                    for comparator in node.comparators:
                        if isinstance(comparator, (ast.Constant, ast.NameConstant)):
                            if getattr(comparator, 'value', None) in (True, False, None):
                                issues.append({
                                    "type": "style",
                                    "line": node.lineno,
                                    "description": "Use == instead of 'is' for comparison with True/False/None",
                                    "severity": "low"
                                })
                                break
        
        return {
            "status": "success",
            "result": CodeAnalysisResult(
                syntax_valid=True,
                issues_found=issues,
                metrics=metrics
            ).dict()
        }
        
    except SyntaxError as e:
        return {
            "status": "error",
            "result": CodeAnalysisResult(
                syntax_valid=False,
                issues_found=[{
                    "type": "syntax",
                    "line": e.lineno or 0,
                    "description": str(e),
                    "severity": "high"
                }],
                metrics=metrics
            ).dict()
        }

# Create the code analyzer agent
analyzer_agent = Agent(
    name="code_analyzer",
    model="gemini-2.0-flash",
    description="A specialized agent for static code analysis",
    instruction=(
        "You are a code analysis expert that examines Python code structure and patterns.\n"
        "Your job is to:\n"
        "1. Analyze code using AST parsing\n"
        "2. Identify code structure issues\n"
        "3. Calculate code metrics\n"
        "4. Report findings in a clear format"
    ),
    tools=[FunctionTool(analyze_structure)]
) 
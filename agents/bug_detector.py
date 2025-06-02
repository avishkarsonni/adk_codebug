"""Bug detector agent that identifies code issues."""
from google.agents.core.agent import agent
from google.agents.core.toolkit_agent import ToolkitAgent

@agent
class BugDetectorAgent(ToolkitAgent):
    """Agent that detects bugs and issues in code."""

    name = "bug_detector"
    description = "Identifies bugs and potential issues in code"
    model = "gemini-2.0-flash"

    async def run(self, inputs: dict, config: dict) -> dict:
        """Run the bug detection analysis.
        
        Args:
            inputs: Dict containing "code_summary" and "code" keys
            config: Configuration options
            
        Returns:
            Dict containing "bug_report" key with the analysis results
        """
        code = inputs.get("code", "")
        code_summary = inputs.get("code_summary", "")
        if not code:
            return {"bug_report": "No code provided"}

        # Analyze code for bugs
        bug_report = await self._detect_bugs(code, code_summary)
        return {"bug_report": bug_report}

    async def _detect_bugs(self, code: str, code_summary: str) -> str:
        """Analyze the code for potential bugs.
        
        Args:
            code: The code to analyze
            code_summary: Summary of the code structure
            
        Returns:
            A string containing the bug report
        """
        prompt = f"""Analyze this Python code for bugs and issues:
        
        Code Summary:
        {code_summary}
        
        Code:
        {code}
        
        Focus on:
        1. Syntax errors
        2. Logical bugs
        3. Missing error handling
        4. Security issues
        5. Performance problems
        
        Provide a detailed report of each issue found.
        """
        
        response = await self.model.generate_text(prompt)
        return response
"""Fix suggestor agent that recommends code fixes."""
from google.agents.core.agent import agent
from google.agents.core.toolkit_agent import ToolkitAgent

@agent
class FixSuggestorAgent(ToolkitAgent):
    """Agent that suggests fixes for identified bugs."""

    name = "fix_suggestor"
    description = "Suggests fixes for identified code issues"
    model = "gemini-2.0-flash"

    async def run(self, inputs: dict, config: dict) -> dict:
        """Run the fix suggestion analysis.
        
        Args:
            inputs: Dict containing "bug_report", "code_summary" and "code" keys
            config: Configuration options
            
        Returns:
            Dict containing "fix_suggestions" key with the suggested fixes
        """
        code = inputs.get("code", "")
        bug_report = inputs.get("bug_report", "")
        code_summary = inputs.get("code_summary", "")
        
        if not code or not bug_report:
            return {"fix_suggestions": "No code or bug report provided"}

        # Generate fix suggestions
        fixes = await self._suggest_fixes(code, bug_report, code_summary)
        return {"fix_suggestions": fixes}

    async def _suggest_fixes(self, code: str, bug_report: str, code_summary: str) -> str:
        """Generate fix suggestions for the identified bugs.
        
        Args:
            code: The original code
            bug_report: Report of identified bugs
            code_summary: Summary of the code structure
            
        Returns:
            A string containing the suggested fixes
        """
        prompt = f"""Suggest fixes for the following code issues:
        
        Code Summary:
        {code_summary}
        
        Original Code:
        {code}
        
        Bug Report:
        {bug_report}
        
        For each issue:
        1. Explain the fix
        2. Provide the corrected code
        3. Explain why the fix resolves the issue
        """
        
        response = await self.model.generate_text(prompt)
        return response 
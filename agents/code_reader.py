"""Code reader agent that analyzes code structure."""
from google.agents.core.agent import agent
from google.agents.core.toolkit_agent import ToolkitAgent

@agent
class CodeReaderAgent(ToolkitAgent):
    """Agent that analyzes and summarizes code structure."""

    name = "code_reader"
    description = "Analyzes and summarizes code structure"
    model = "gemini-2.0-flash"

    async def run(self, inputs: dict, config: dict) -> dict:
        """Run the code reader analysis.
        
        Args:
            inputs: Dict containing "code" key with the code to analyze
            config: Configuration options
            
        Returns:
            Dict containing "code_summary" key with the analysis results
        """
        code = inputs.get("code", "")
        if not code:
            return {"code_summary": "No code provided"}

        # Analyze code structure and return summary
        summary = await self._analyze_code_structure(code)
        return {"code_summary": summary}

    async def _analyze_code_structure(self, code: str) -> str:
        """Analyze the structure of the provided code.
        
        Args:
            code: The code to analyze
            
        Returns:
            A string containing the code structure analysis
        """
        # Use the model to analyze code structure
        prompt = f"""Analyze this Python code and describe its structure:
        
        {code}
        
        Focus on:
        1. Overall purpose
        2. Functions/classes and their roles
        3. Key logic and flow
        4. Important dependencies
        """
        
        response = await self.model.generate_text(prompt)
        return response 
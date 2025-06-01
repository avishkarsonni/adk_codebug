from google.adk.agents import ToolkitAgent
import subprocess
import tempfile
import os

class CodeExecutorAgent(ToolkitAgent):
    def __init__(self):
        super().__init__(
            name="code_executor",
            model="gemini-2.0-flash",
            instruction="Execute the provided Python code and return the output or any errors.",
        )

    def run(self, input: dict):
        code = input.get("code", "")
        if not code:
            return "Error: No code provided in input."
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            try:
                result = subprocess.run(
                    ["python", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            except subprocess.TimeoutExpired:
                output = "Error: Code execution timed out."
            except Exception as e:
                output = f"Error during execution: {e}"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        return output 
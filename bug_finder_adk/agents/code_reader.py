from google.adk.agents import ToolkitAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
# For demonstration, print the keys (in real code, do not print secrets)
# print(f"GOOGLE_API_KEY: {GOOGLE_API_KEY}")
# print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")

class CodeReaderAgent(ToolkitAgent):
    def __init__(self):
        super().__init__(
            name="code_reader",
            model="gemini-2.0-flash",
            instruction="Summarize the provided Python code: count the number of functions, imports, and provide a brief summary.",
        )

    def run(self, input: dict):
        code = input.get("code", "")
        if not code:
            return {"error": "No code provided in input."}
        # The ToolkitAgent's run method will use the instruction and model to process the code
        return super().run(input={"code": code}) 
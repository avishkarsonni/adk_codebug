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

class BugDetectorAgent(ToolkitAgent):
    def __init__(self):
        super().__init__(
            name="bug_detector",
            model="gemini-2.0-flash",
            instruction="Analyze the provided Python code and identify any bugs (syntax or logic errors). List the bugs with line numbers and descriptions. Return the result as a string.",
        )

    def run(self, input: dict):
        code = input.get("code", "")
        if not code:
            return "Error: No code provided in input."
        return super().run(input={"code": code}) 
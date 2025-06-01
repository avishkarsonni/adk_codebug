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

class FixSuggestorAgent(ToolkitAgent):
    def __init__(self):
        super().__init__(
            name="fix_suggestor",
            model="gemini-2.0-flash",
            instruction="Given a bug report for Python code, suggest fixes for each bug and return the updated code or clear instructions for fixing the code.",
        )

    def run(self, input: dict):
        bug_report = input.get("bug_report", "")
        if not bug_report:
            return "Error: No bug_report provided in input."
        return super().run(input={"bug_report": bug_report}) 
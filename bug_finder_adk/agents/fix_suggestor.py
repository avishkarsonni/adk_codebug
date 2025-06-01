from google.adk.agents import ToolkitAgent

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
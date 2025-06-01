from google.adk.agents import ToolkitAgent

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
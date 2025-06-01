from google.adk.agents import ToolkitAgent

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
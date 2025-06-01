from google.adk.agents import LlmAgent

fix_suggestor = LlmAgent(
    name="fix_suggestor",
    model="gemini-2.0-flash",
    instruction="Given a list of bugs in Python code, suggest fixes for each bug, including code snippets if possible."
)

def run(bug_report):
    return fix_suggestor.run(input=bug_report) 
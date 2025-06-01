from google.adk.agents import LlmAgent

bug_detector = LlmAgent(
    name="bug_detector",
    model="gemini-2.0-flash",
    instruction="Given a summary of Python code, identify any bugs (syntax or logic errors) and list them with line numbers and descriptions."
)

def run(input_summary):
    return bug_detector.run(input=input_summary) 
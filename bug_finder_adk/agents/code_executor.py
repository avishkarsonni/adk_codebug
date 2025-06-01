from google.adk.agents import LlmAgent

code_executor = LlmAgent(
    name="code_executor",
    model="gemini-2.0-flash",
    instruction="Given Python code and suggested fixes, simulate executing the fixed code and report the output or any errors."
)

def run(fixed_code):
    return code_executor.run(input=fixed_code) 
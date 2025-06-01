from google.adk.agents import LlmAgent

code_reader = LlmAgent(
    name="code_reader",
    model="gemini-2.0-flash",
    instruction="Read the provided Python code and summarize it: count the number of functions, imports, and provide a brief summary."
)

def run(input_code):
    return code_reader.run(input=input_code) 
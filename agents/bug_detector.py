from google.adk.agents import LlmAgent
import google.generativeai as genai
from pydantic import BaseModel, Field
import os

class CodeInput(BaseModel):
    code: str = Field(description="The Python code to analyze for bugs.")

BugDetectorAgent = LlmAgent(
    name="BugDetectorAgent",
    model=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
    instruction=(
        "You are a Python code bug detection expert. "
        "Given a Python code snippet, carefully analyze it for any bugs, errors, or potential issues. "
        "Identify syntax errors, logical mistakes, missing arguments, or any code that could cause runtime exceptions. "
        "Provide a detailed bug report listing each issue found, explaining why it is a problem and where it occurs in the code."
    ),
    input_schema=CodeInput,
)
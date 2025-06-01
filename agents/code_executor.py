from google.adk.agents import LlmAgent
import google.generativeai as genai
from pydantic import BaseModel, Field
import os

class CodeInput(BaseModel):
    code: str = Field(description="The Python code to analyze for execution behavior.")

CodeExecutorAgent = LlmAgent(
    name="CodeExecutorAgent",
    model=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
    instruction=(
        "You are a Python code execution analyst. "
        "Given a Python code snippet, predict and describe in detail what would happen if the code is executed. "
        "Include the expected output, any errors or exceptions that would occur, and explain why. "
        "If the code has side effects or interacts with files or the environment, mention those as well. "
        "Be thorough and precise in your analysis."
    ),
    input_schema=CodeInput,
) 
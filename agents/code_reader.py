from google.adk.agents import LlmAgent
import google.generativeai as genai
from pydantic import BaseModel, Field
import os

class CodeInput(BaseModel):
    code: str = Field(description="The Python code to analyze.")

CodeReaderAgent = LlmAgent(
    name="CodeReaderAgent",
    model=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
    instruction=(
        "You are an expert Python code summarizer. "
        "Given a Python code snippet as input, analyze its structure, purpose, and main logic. "
        "Provide a clear, concise summary that explains what the code does, its key functions, and any important details. "
        "If the code contains classes or functions, mention their roles. "
        "Highlight any unique or non-obvious behavior."
    ),
    input_schema=CodeInput,
) 
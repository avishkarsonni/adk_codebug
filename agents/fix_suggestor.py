from google.adk.agents import LlmAgent
import google.generativeai as genai
from pydantic import BaseModel, Field
import os

class BugReportInput(BaseModel):
    bug_report: str = Field(description="The bug report detailing issues in the code.")

FixSuggestorAgent = LlmAgent(
    name="FixSuggestorAgent",
    model=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
    instruction=(
        "You are a Python code repair specialist. "
        "Given a bug report describing issues in a Python code snippet, suggest clear and effective fixes for each problem. "
        "If possible, provide the corrected code with all bugs fixed. "
        "If a fix requires explanation, describe the changes needed and why they resolve the issue. "
        "Ensure your suggestions are accurate and improve the code's reliability."
    ),
    input_schema=BugReportInput,
) 
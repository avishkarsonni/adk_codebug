import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agents.coordinator import coordinator

# Load environment variables
load_dotenv()

# Get configuration from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
APP_NAME = os.getenv("APP_NAME", "bug_finder")
USER_ID = os.getenv("USER_ID", "test_user")
CODE_SAMPLES_DIR = os.getenv("CODE_SAMPLES_DIR", "code_samples")
BUGGY_CODE_FILE = os.getenv("BUGGY_CODE_FILE", "buggy_code.py")

# Validate required environment variables
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)

async def main():
    # Set up session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=coordinator,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Create a session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    # Read the buggy code
    code_file_path = Path(CODE_SAMPLES_DIR) / BUGGY_CODE_FILE
    if not code_file_path.exists():
        raise FileNotFoundError(f"Code file not found: {code_file_path}")
    
    with open(code_file_path, 'r') as f:
        code = f.read()

    # Create the message content
    message = Content(role="user", parts=[Part(text=code)])

    # Run the coordinator
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message
    ):
        if event.is_final_response():
            print('--- Multi-Agent Bug Finder Report ---')
            print(event.content)

if __name__ == '__main__':
    asyncio.run(main()) 
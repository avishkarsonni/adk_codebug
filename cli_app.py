import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.coordinator import coordinator

# Load environment variables
load_dotenv()

# Get configuration from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
APP_NAME = os.getenv("APP_NAME", "bug_finder")
USER_ID = os.getenv("USER_ID", "test_user")
CODE_SAMPLES_DIR = os.getenv("CODE_SAMPLES_DIR", "code_samples")

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
    session = await session_service.create_session(APP_NAME, USER_ID)

    print("Bug Finder CLI Interface")
    print("Type 'quit' to exit\n")

    while True:
        try:
            # Get user input
            user_input = input("You > ")
            
            if user_input.lower() == 'quit':
                break

            # Run the coordinator
            response = await runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message={"role": "user", "content": user_input}
            )

            print("\nAgent > ", response)
            print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main()) 
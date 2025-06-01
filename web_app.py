from pathlib import Path
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.coordinator import coordinator
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Load environment variables
load_dotenv()

# Get configuration from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
APP_NAME = os.getenv("APP_NAME", "bug_finder")

# Validate required environment variables
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)

# Create FastAPI app
app = FastAPI(title="Bug Finder ADK Interface")

# Set up session service and runner
session_service = InMemorySessionService()
runner = Runner(
    agent=coordinator,
    app_name=APP_NAME,
    session_service=session_service
)

# Add a root endpoint for basic information
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Bug Finder ADK</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { color: #333; }
                .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; border-radius: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Bug Finder ADK</h1>
                <p>A multi-agent system for finding and analyzing bugs in code</p>
                <h2>Available Endpoints:</h2>
                <div class="endpoint">/docs - API Documentation</div>
                <div class="endpoint">/api/analyze - Submit code for analysis</div>
            </div>
        </body>
    </html>
    """

# API endpoint for code analysis
@app.post("/api/analyze")
async def analyze_code(code: str):
    session = await session_service.create_session(APP_NAME, "user")
    response = await runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message={"role": "user", "content": code}
    )
    return {"analysis": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
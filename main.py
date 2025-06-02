import os
from dotenv import load_dotenv
import google.generativeai as genai

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
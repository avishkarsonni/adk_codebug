import os
import subprocess
import time
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ADK Web Server configuration
ADK_HOST = "localhost"
ADK_PORT = 8000
ADK_BASE_URL = f"http://{ADK_HOST}:{ADK_PORT}"
ADK_APP_NAME = "bug_finder"
USER_ID = "streamlit_user"
SESSION_ID = "session_1"

def start_adk_server():
    """Start the ADK web server in the background."""
    try:
        # Start the ADK web server
        process = subprocess.Popen(
            ["adk", "web", "--host", ADK_HOST, "--port", str(ADK_PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for the server to start
        time.sleep(5)
        return process
    except Exception as e:
        st.error(f"Failed to start ADK server: {str(e)}")
        return None

def create_session():
    """Create a new session with the ADK server."""
    try:
        session_url = f"{ADK_BASE_URL}/apps/{ADK_APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
        print(f"Creating session at: {session_url}")  # Debug print
        
        response = requests.post(
            session_url,
            json={"state": {}}
        )
        print(f"Session creation response status: {response.status_code}")  # Debug print
        print(f"Session creation response: {response.content}")  # Debug print
        
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to create session: {str(e)}")  # Debug print
        st.error(f"Failed to create session: {str(e)}")
        return False

def send_to_adk(prompt):
    """Send a prompt to the ADK server and get the response."""
    try:
        # Send the message using the existing session
        run_url = f"{ADK_BASE_URL}/run"
        payload = {
            "appName": ADK_APP_NAME,
            "userId": USER_ID,
            "sessionId": SESSION_ID,
            "new_message": {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        }
        print(f"Sending request to {run_url} with payload: {payload}")  # Debug print
        
        response = requests.post(run_url, json=payload)
        print(f"Response status code: {response.status_code}")  # Debug print
        print(f"Response headers: {response.headers}")  # Debug print
        print(f"Response content: {response.content}")  # Debug print
        
        response.raise_for_status()
        
        # Extract the response
        result = response.json()
        print(f"Parsed result: {result}")  # Debug print
        
        if isinstance(result, list):
            # Look for the assistant's response in the events
            for event in result:
                if isinstance(event, dict) and "content" in event:
                    content = event["content"]
                    if isinstance(content, dict) and "parts" in content:
                        parts = content["parts"]
                        if parts and isinstance(parts[0], dict) and "text" in parts[0]:
                            return parts[0]["text"]
        
        return "No response from assistant. Please try again."
            
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")  # Debug print
        return f"Error communicating with ADK server: {str(e)}"
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug print
        return f"Unexpected error: {str(e)}"

def initialize_adk_app():
    """Initialize the ADK app."""
    try:
        init_url = f"{ADK_BASE_URL}/apps/{ADK_APP_NAME}/init"
        print(f"Initializing ADK app at: {init_url}")  # Debug print
        response = requests.post(init_url)
        print(f"Init response status: {response.status_code}")  # Debug print
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to initialize ADK app: {str(e)}")  # Debug print
        st.error(f"Failed to initialize ADK app: {str(e)}")
        return False

# Initialize Streamlit interface
st.title("ADK Chat Interface")
st.write("Chat with the ADK agent through this interface!")

# Start ADK server when the app loads
if "adk_server" not in st.session_state:
    st.session_state.adk_server = start_adk_server()
    if st.session_state.adk_server is None:
        st.error("Failed to start ADK server")
        st.stop()

# Create session if not already created
if "session_created" not in st.session_state:
    st.session_state.session_created = create_session()
    if st.session_state.session_created:
        st.success("Connected to ADK server successfully!")
    else:
        st.error("Failed to connect to ADK server. Please check if the server is running.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get ADK response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if not st.session_state.session_created:
                st.error("Not connected to ADK server. Please refresh the page to try again.")
                response = "Error: Not connected to ADK server"
            else:
                response = send_to_adk(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Cleanup when the app is closed
def cleanup():
    if "adk_server" in st.session_state and st.session_state.adk_server:
        st.session_state.adk_server.terminate()

# Register cleanup
import atexit
atexit.register(cleanup) 
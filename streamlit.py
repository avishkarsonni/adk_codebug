import os
import subprocess
import time
import streamlit as st
import requests
from dotenv import load_dotenv
import signal

# Load environment variables
load_dotenv()

# ADK Web Server configuration
ADK_HOST = "localhost"
ADK_PORT = 8000
ADK_BASE_URL = f"http://{ADK_HOST}:{ADK_PORT}"
ADK_APP_NAME = "bug_finder"
USER_ID = "streamlit_user"
SESSION_ID = "session_1"

# Start ADK server as a subprocess if not already running
@st.cache_resource(show_spinner=False)
def start_adk_server():
    try:
        # Check if already running
        try:
            r = requests.get(f"{ADK_BASE_URL}/dev-ui", timeout=2)
            if r.status_code == 200 or r.status_code == 307:
                return None  # Already running, no need to start
        except Exception:
            pass
        # Start the ADK web server
        process = subprocess.Popen(
            ["adk", "web", "--host", ADK_HOST, "--port", str(ADK_PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # So we can kill the whole process group
        )
        # Wait for the server to start
        for _ in range(20):
            try:
                r = requests.get(f"{ADK_BASE_URL}/dev-ui", timeout=2)
                if r.status_code == 200 or r.status_code == 307:
                    return process
            except Exception:
                time.sleep(0.5)
        st.error("Failed to start ADK server after waiting.")
        return None
    except Exception as e:
        st.error(f"Failed to start ADK server: {str(e)}")
        return None

def create_session():
    try:
        session_url = f"{ADK_BASE_URL}/apps/{ADK_APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
        response = requests.post(
            session_url,
            json={"state": {}}
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to create session: {str(e)}")
        return False

def send_to_adk(prompt):
    try:
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
        response = requests.post(run_url, json=payload)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list):
            for event in result:
                if isinstance(event, dict) and "content" in event:
                    content = event["content"]
                    if isinstance(content, dict) and "parts" in content:
                        parts = content["parts"]
                        if parts and isinstance(parts[0], dict) and "text" in parts[0]:
                            return parts[0]["text"]
        return "No response from assistant. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error communicating with ADK server: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Start ADK server (if not already running)
adk_proc = start_adk_server()

# Register cleanup to kill ADK server on exit
@st.cache_resource(show_spinner=False)
def register_cleanup():
    def cleanup():
        if adk_proc is not None:
            try:
                os.killpg(os.getpgid(adk_proc.pid), signal.SIGTERM)
            except Exception:
                pass
    import atexit
    atexit.register(cleanup)
    return True
register_cleanup()

# Streamlit UI
st.title("ADK Chat Interface (Self-Hosted)")
st.write("Chat with the ADK agent. The ADK server is managed by this app.")

# Create session if not already created
if "session_created" not in st.session_state:
    st.session_state.session_created = create_session()
    if st.session_state.session_created:
        st.success("Connected to ADK server successfully!")
    else:
        st.error("Failed to connect to ADK server. Please check logs.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if not st.session_state.session_created:
                st.error("Not connected to ADK server. Please refresh the page to try again.")
                response = "Error: Not connected to ADK server"
            else:
                response = send_to_adk(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response}) 
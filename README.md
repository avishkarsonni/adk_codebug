# ADK Chat Interface

This application provides a web-based chat interface that communicates with an ADK (AI Development Kit) server. It's built using Streamlit for the frontend and integrates with the ADK server running locally.

## Prerequisites

- Python 3.x
- ADK installed and configured
- Streamlit
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/avishkarsonni/adk_codebug.git
cd adk_codebug
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the ADK server:
```bash
adk web --host localhost --port 8000
```

2. In a new terminal, start the Streamlit application:
```bash
streamlit run bug_finder/streamlit_app.py
```

## Accessing the Application

- **Local Access**: Open your web browser and navigate to:
  - http://localhost:8501

- **Network Access**: If you want to access from other devices on the same network:
  - http://<your-machine-ip>:8501
  - The network URL will be displayed in the terminal when you start the Streamlit app

## Application Structure

The application consists of two main components:

1. **ADK Server**:
   - Runs on: http://localhost:8000
   - Handles the AI processing and responses
   - Manages sessions and message processing

2. **Streamlit Frontend**:
   - Runs on: http://localhost:8501
   - Provides the user interface for chat
   - Manages communication with the ADK server

## API Endpoints

The application uses the following endpoints:

1. **Session Creation**:
   - Endpoint: `/apps/bug_finder/users/streamlit_user/sessions/session_1`
   - Method: POST
   - Creates a new chat session

2. **Message Processing**:
   - Endpoint: `/run`
   - Method: POST
   - Handles message exchange with the AI

## Usage

1. When you open the application, it automatically:
   - Starts the ADK server (if not already running)
   - Creates a new session
   - Displays a success message when connected

2. To use the chat interface:
   - Type your message in the input field at the bottom
   - Press Enter or click the send button
   - Wait for the AI's response
   - The chat history will be displayed in the main window

## Troubleshooting

If you encounter issues:

1. **Connection Refused Error**:
   - Ensure the ADK server is running on port 8000
   - Check if there are any conflicting processes using the same port

2. **Session Creation Failed**:
   - Verify the ADK server is running and accessible
   - Check the server logs for any error messages

3. **No Response from Assistant**:
   - Verify the message format in the request
   - Check the server logs for processing errors

## Environment Variables

The application uses the following configuration:

- ADK_HOST: localhost (default)
- ADK_PORT: 8000 (default)
- ADK_APP_NAME: bug_finder
- USER_ID: streamlit_user
- SESSION_ID: session_1

These can be modified in the `streamlit_app.py` file if needed.

## Security Notes

- This application is configured for local development
- For production deployment, additional security measures should be implemented
- Avoid exposing the ADK server directly to the internet
- Consider adding authentication for production use

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the ADK documentation
3. Submit an issue in the repository 
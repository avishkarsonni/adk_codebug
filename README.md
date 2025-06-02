# bug_finder_adk

A multi-agent bug-finding system using Google ADK and Gemini 2.0 Flash as the LLM.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Google API key in a `.env` file:
   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

## Running the Project

The project uses ADK's built-in web interface:

1. Start the ADK web server:
   ```bash
   agent-devkit web
   ```

2. Access the interface at `http://localhost:8000`

3. In the web interface:
   - Select the "bug_finder" workflow
   - Input your Python code
   - Click "Run" to analyze

## Project Structure

- `adk.json` - ADK configuration file
- `workflows/` - Workflow definitions
  - `bug_finding_workflow.py` - Main workflow that chains agents
- `agents/` - Agent definitions:
  - `code_reader.py` - Analyzes code structure
  - `bug_detector.py` - Identifies bugs
  - `fix_suggestor.py` - Suggests fixes
  - `code_executor.py` - Simulates code execution

## Workflow

The bug finding process follows this sequence:
1. Code Reader → Analyzes and summarizes code structure
2. Bug Detector → Identifies potential issues
3. Fix Suggestor → Recommends solutions
4. Code Executor → Simulates execution behavior

## References
- [Google ADK Docs](https://github.com/google/agent-development-kit) 
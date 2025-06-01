# bug_finder_adk

A multi-agent bug-finding system using Google ADK and Gemini 2.0 Flash as the LLM.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Google API key:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```
3. Run the main pipeline:
   ```bash
   python main.py
   ```

## Project Structure

- `main.py` — Entry point
- `agents/` — All agent classes
- `code_samples/` — Example buggy code

## Streamlit UI (Optional)
To use the Streamlit UI:
```bash
streamlit run main.py
```

## References
- [Google ADK Docs](https://github.com/google/agent-development-kit)
- [Code Assistant Agent Example](https://github.com/vono-hvore/code-assistant-agent/tree/master) 
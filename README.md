# Multi-Agent Bug Finder using ADK

This project demonstrates a multi-agent system using Auto Dev Kernel (ADK) to detect and suggest fixes for bugs in Python code samples.

## Project Structure
- `sample_code/`: Contains Python files with intentional syntax and logic errors for testing.
- `requirements.txt`: Project dependencies, including ADK and Python packages.
- `adk_workflow.yaml`: Defines the multi-agent workflow for ADK.
- `*_agent.py`: Python scripts implementing each agent.

## Agents
- **code_reader**: Reads code and summarizes it (number of functions, imports, etc.).
- **bug_identifier**: Detects bugs in the code (syntax errors, line numbers, error types).
- **fix_recommender**: Recommends fixes for detected bugs.
- **code_executor**: Executes code in a safe sandbox and captures output/errors.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (If ADK is not on PyPI, install it per the official instructions.)

## Usage
1. Place Python files to be analyzed in the `sample_code/` directory.
2. Run the workflow using ADK:
   ```bash
   adk run adk_workflow.yaml
   ```
   (Replace with the actual ADK command if different.)
3. Outputs will be generated as JSON files: `code_summary.json`, `bug_report.json`, `fix_suggestions.json`, `execution_results.json`.

## Notes
- The code executor uses a restricted environment for demonstration. For production, use Docker or a secure sandbox.
- The fix recommender provides simple, example suggestions. 
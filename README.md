# Multi-Agent Bug Finder using ADK

This project demonstrates a multi-agent system using Auto Dev Kernel (ADK) to detect and suggest fixes for bugs in Python code samples.

## Project Structure
- `sample_code/`: Contains Python files with intentional syntax and logic errors for testing.
- `requirements.txt`: Project dependencies, including ADK and Python packages.
- `adk_workflow.yaml`: Defines the multi-agent workflow for ADK.
- `*_agent.py`: Python scripts implementing each agent.
- `main.py`: Run any agent on demand, optionally on a specific file.
- `test_workflow.py`: Script to test the full workflow end-to-end.

## Agents
- **code_reader**: Reads code and summarizes it (number of functions, imports, etc.).
- **bug_identifier**: Detects bugs in the code (syntax errors, line numbers, error types).
- **fix_recommender**: Recommends fixes for detected bugs based on error messages.
- **code_executor**: Executes code in a safe sandbox and captures output/errors.

## How the System Works
1. **code_reader** scans all Python files in `sample_code/` and summarizes their structure.
2. **bug_identifier** analyzes the code for syntax errors and logs details.
3. **fix_recommender** suggests possible fixes for each detected bug.
4. **code_executor** attempts to run the code and captures output/errors.
5. The workflow is orchestrated by ADK using `adk_workflow.yaml`, or can be tested manually.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (If ADK is not on PyPI, install it per the official instructions.)

## Usage
### Run the Full Workflow with ADK
1. Place Python files to be analyzed in the `sample_code/` directory.
2. Run the workflow using ADK:
   ```bash
   adk run adk_workflow.yaml
   ```
   (Replace with the actual ADK command if different.)
3. Outputs will be generated as JSON files: `code_summary.json`, `bug_report.json`, `fix_suggestions.json`, `execution_results.json`.

### Run Individual Agents
You can run any agent directly using the main interface:
```bash
python main.py <agent> [file]
```
- `<agent>`: One of `code_reader`, `bug_identifier`, `fix_recommender`, `code_executor`
- `[file]`: (Optional) Path to a specific file to check (if supported by the agent)

### Test the Workflow End-to-End
Run the test script to check all agents and outputs:
```bash
python test_workflow.py
```

## Notes
- The code executor uses a restricted environment for demonstration. For production, use Docker or a secure sandbox.
- The fix recommender provides simple, example suggestions. 
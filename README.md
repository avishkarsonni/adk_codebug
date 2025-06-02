# ADK Bug Finder

An intelligent code analysis and bug detection system built with Google's Agent Development Kit (ADK). This tool leverages ADK's capabilities to analyze code, detect potential issues, and suggest fixes while providing a visual representation of the analysis process.

## Features

- Automated Code Analysis: Detects syntax errors, missing arguments, and style issues
- Smart Fix Suggestions: Provides context-aware fix recommendations
- Interactive Visualization: Real-time visualization of the analysis workflow
- Web UI Integration: Seamless integration with ADK's web interface
- Command Line Support: Full functionality through ADK CLI

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google's Agent Development Kit (ADK)

## Installation

1. Install ADK if you haven't already:
```bash
pip install google-adk
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/adk-codebug.git
cd adk-codebug
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

4. Install the package and its dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Web Interface (Recommended)

1. Start the ADK server:
```bash
adk serve
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. In the ADK Web UI:
   - Select "bug_finder" from the Agents dropdown
   - Either:
     - Upload a Python file using the file upload button
     - Or paste your code directly into the input text area
   - Click "Run" to start the analysis
   - Watch the analysis workflow in real-time
   - Review results and suggested fixes in the output panel

### Command Line Interface

For automated or scripted usage, use the ADK CLI:

```bash
# Analyze a single file
adk run bug_finder --input-file path/to/your/code.py

# Analyze with specific options
adk run bug_finder --input-file path/to/code.py --options '{"detail_level": "high"}'
```

### Example

```bash
# Analyze the example file
adk run bug_finder --input-file bug_finder/samples/example.py
```

The analysis process:
1. Code is parsed and analyzed for potential issues
2. Each detected issue is categorized and prioritized
3. Fix suggestions are generated with explanations
4. Results are displayed in a structured format
5. The entire workflow is visualized in the ADK web UI

## Project Structure

```
adk-codebug/
├── bug_finder/           # Main package directory
│   ├── agents/          # ADK agent definitions
│   │   └── __init__.py  # Agent registration
│   ├── samples/         # Example code samples
│   ├── agent.py         # Core bug finder implementation
│   └── __init__.py      # Package initialization
├── requirements.txt      # Project dependencies
└── setup.py             # Package setup configuration
```

## Visualization

The ADK web UI provides a rich visualization of the analysis process:

- 🟢 Dark green nodes: Currently active components
- 🌱 Light green edges: Active data flow
- ⚪ Light gray elements: Inactive components
- 🤖 Robot icon: Agent nodes
- 🔧 Wrench icon: Tool nodes

The visualization helps you understand:
- How your code is being analyzed
- Which components are currently active
- The flow of information between components
- The progress of the analysis

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows our style guidelines and includes appropriate tests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

If you encounter issues:

1. Ensure ADK is properly installed and up to date
2. Check that your Python version is 3.8 or higher
3. Verify your virtual environment is activated
4. Make sure the ADK server is running for web UI features 
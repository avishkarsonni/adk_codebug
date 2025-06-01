#!/bin/bash

# Function to display usage
show_usage() {
    echo "Usage: ./run.sh [web|cli]"
    echo "  web - Run the web interface"
    echo "  cli - Run the command-line interface"
}

# Check if an argument is provided
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the appropriate interface
case "$1" in
    "web")
        echo "Starting web interface..."
        python web_app.py
        ;;
    "cli")
        echo "Starting CLI interface..."
        python cli_app.py
        ;;
    *)
        show_usage
        exit 1
        ;;
esac 
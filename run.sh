#!/bin/bash

echo "Starting DeepAgents Research Assistant..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing/updating dependencies..."
if command -v uv &> /dev/null; then
    uv pip install -r requirements.txt --quiet
else
    echo "uv not found, using pip..."
    pip install -r requirements.txt --quiet
fi
echo

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Please copy .env.example to .env and add your API key."
    echo
    exit 1
fi

# Run Streamlit on port 8502 (in case 8501 is already in use)
echo "Starting Streamlit application on http://localhost:8502"
echo
streamlit run app.py --server.port 8502

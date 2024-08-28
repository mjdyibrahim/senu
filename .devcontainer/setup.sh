#!/bin/bash

# Create the virtual environment if it doesn't exist
if [ ! -d "/workspace/venv" ]; then
    python3 -m venv /workspace/venv
fi

# Activate the virtual environment
source /workspace/venv/bin/activate

# Ensure the virtual environment's Python is used
export PATH="/workspace/venv/bin:$PATH"

# Upgrade pip
pip install --upgrade pip

# Install any missing requirements, including uvicorn
pip install -r /workspace/requirements.txt

# Install Git
apt-get update && apt-get install -y git


#!/bin/bash

# Ensure the virtual environment's Python is used
export PATH="/workspace/venv/bin:$PATH"

# Activate the virtual environment
source /workspace/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install any missing requirements, including uvicorn
pip install -r /workspace/requirements.txt

# Install Git
apt-get update && apt-get install -y git

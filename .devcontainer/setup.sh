#!/bin/bash

# Create the virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Ensure the virtual environment's Python is used
export PATH="venv/bin:$PATH"

# Upgrade pip
pip install --upgrade pip

# Install any missing requirements
pip install -r requirements.txt

# Install Git
apt-get update && apt-get install -y git


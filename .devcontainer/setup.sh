#!/bin/bash

# Activate the virtual environment
source /workspace/venv/bin/activate

# Update pip
sudo pip install --upgrade pip

# Install any missing requirements
sudo pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
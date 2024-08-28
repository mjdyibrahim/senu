#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Update pip
sudo pip install --upgrade pip

# Install any missing requirements
sudo pip install -r requirements.txt

# Install Git
apt-get update && apt-get install -y git

# Deactivate the virtual environment
deactivate

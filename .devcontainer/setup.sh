#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install any missing requirements
sudo pip install -r requirements.txt

# Install Git
apt-get update && apt-get install -y git


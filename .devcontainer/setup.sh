#!/bin/bash

# Ensure the virtual environment's Python is used
export PATH="/app/venv/bin:$PATH"

# Activate the virtual environment
source /app/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install any missing requirements, including uvicorn
pip install -r /workspace/requirements.txt

# Ensure Supabase CLI is installed if needed
npm install -g supabase

# Install Git
apt-get update && apt-get install -y git

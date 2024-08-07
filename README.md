# Senu: Startup Copilot

NOTICE: This App is subjected to continous improvement and the main branch are not guranteed to work. Visit the live demo of the latest stable release at https://senu.abdomagdy.com

This app makes use of AI71 API Hub to connect Falcon LLM and Cohere for Embedding and Semantic Search in addition to Weaviate for Vector Database, to get started you need to do the following:

# Step 1: re-name .env-example to .env and add APIs from corresponding hubs

AI71 API HUB: 
https://marketplace.ai71.ai/

AI71_API_KEY=""
AI71_BASE_URL=""

COHERE: 
https://dashboard.cohere.com/api-keys

COHERE_API_KEY=""

Weaviate: 
https://console.weaviate.cloud/dashboard

Create Weaviate Cluster and add Cluster API and URL 

WEAVIATE_API_KEY=""
WEAVIATE_URL=""

# Step #2, create python env and Install all required packages

create a python environment: 
python -m venv venv

install all required packages:
pip install -r requirements.txt

* latest cohere version conflicts with dspy, keep it at its current version

# Step #2 Launching the app

The App is built with flask 

launch it though:

python app.py
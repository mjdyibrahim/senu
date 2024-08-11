# Senu: Startup Copilot

**NOTICE:** This app is subject to continuous improvement and the main branch is not guaranteed to be stable. For the latest stable release, visit the live demo at [Senu Live Demo](https://senu.abdomagdy.com).

## Note
The latest content relevant to the Falcon Hackathon is placed inside the `falconhack` branch.

## How It Works
This application extracts information from an uploaded pitch deck and uses semantic search and structured output with guardrails to process startup metrics functions, which are then reflected to the user to inform them of their current development status, their next milestones and a recommendation of actions and resources they should pursue to reach their goal. Key components of the application include:

### Startup Data
- **Collection of Questions**: Validates startup information as a basis for reasonable evaluation and decision-making.
- **Data Processing**: Uses Semantic Search for the uploaded pitch deck and extracts data with the help of DSPy structured output and guardrails.

### Startup Metric
- **Metric Calculation**: Calculates key startup metrics from the extracted information.
- **User Interaction**: Prioritizes conversation with the user to gather critical information for a comprehensive assessment.

### Startup Roadmap
- **Dynamic Stages and Milestones**: Defines stages and milestones for each startup based on industry and competence level.
- **Target Recommendations**: Recommends specific "states" as targets for startups to qualify for certain types of support.

### Startup Ecosystem
- **Resource Listing**: Lists all startup resources available within each geography, categorized by type of help for matchmaking.

## Setup Instructions

### Step 1: Configure Environment
1. Rename `.env-example` to `.env` and add APIs from the corresponding hubs:
   - **AI71 API HUB**: [AI71 Marketplace](https://marketplace.ai71.ai/)
     ```plaintext
     AI71_API_KEY=""
     AI71_BASE_URL=""
     ```
   - **COHERE**: [Cohere Dashboard](https://dashboard.cohere.com/api-keys)
     ```plaintext
     COHERE_API_KEY=""
     ```
   - **Weaviate**: [Weaviate Console](https://console.weaviate.cloud/dashboard)
     Create a Weaviate Cluster and add Cluster API and URL:
     ```plaintext
     WEAVIATE_API_KEY=""
     WEAVIATE_URL=""
     ```

### Step 2: Create Python Environment and Install Dependencies
1. Create a Python virtual environment:
   ```bash
   python -m venv venv

### Step 3: Install required packages
1. Install required packages:
   ```bash
   pip install -r requirements.txt

### Step 4:  Launch the App
1. The app is built with Flask. Launch it using:
   ```bash
   python app.py
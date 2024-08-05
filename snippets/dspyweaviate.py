import os
import dspy
import openai
import weaviate
import weaviate.classes.config as wvcc
from dspy.retrieve.weaviate_rm import WeaviateRM
from dotenv import load_dotenv
from DSPyevaluate import EvaluateTeamSection

# Load environment variables
load_dotenv()

# Access environment variables
AI71_API_KEY = os.getenv("AI71_API_KEY")
AI71_BASE_URL = os.getenv("AI71_BASE_URL")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")


# Initialize the OpenAI client for AI71
client = openai.OpenAI(
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
)

# client = weaviate.connect_to_local()  # Connect to local host
weaviate_client = weaviate.connect_to_wcs(
    cluster_url=WEAVIATE_URL,  # Replace with your WCS URL
    auth_credentials=weaviate.auth.AuthApiKey(WEAVIATE_API_KEY),  # Replace with your WCS key
    headers={
        'X-Cohere-Api-Key': (COHERE_API_KEY) # Replace with your Cohere API key
    }
)

collection = weaviate_client.collections.create(
    name="senu",
    vectorizer_config=wvcc.Configure.Vectorizer.text2vec_cohere
    (
        model="embed-multilingual-v3.0"
    ),
    properties=[
            wvcc.Property(name="content", data_type=wvcc.DataType.TEXT),
            wvcc.Property(name="author", data_type=wvcc.DataType.TEXT),
      ]
)

falcon_lm = dspy.OpenAI(model="tiiuae/falcon-180b-chat", api_base=AI71_BASE_URL, api_key=AI71_API_KEY)

weaviate_rm = WeaviateRM("senu", weaviate_client)

# Configure DSPy with the custom function
dspy.configure(lm=falcon_lm, rm=weaviate_rm)

# Define a DSPy module
evaluate_team = dspy.ChainOfThought(EvaluateTeamSection)

# Example usage
response = evaluate_team(team_content="Startup has a single cofounder with no previous startup experience")
print(response.team_score)

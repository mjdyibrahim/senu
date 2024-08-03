import os
import dspy
import openai
import weaviate
import weaviate.classes.config as wvcc
from dotenv import load_dotenv

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


# Configure DSPy with the custom function
dspy.configure(lm=falcon_lm)

# Define a DSPy module
qa = dspy.ChainOfThought('question -> answer')

# Example usage
response = qa(question="How strong is the team described in the uploaded pitch deck?")
print(response.answer)

import sys
import os
import dspy
import openai
import weaviate
import weaviate.classes.config as wvcc
from dspy.retrieve.weaviate_rm import WeaviateRM
from dotenv import load_dotenv
from DSPyevaluate import *
import matplotlib.pyplot as plt
import numpy as np
import phoenix as px
from openinference.instrumentation.dspy import DSPyInstrumentor
import logging


DSPyInstrumentor().instrument()

# Set up logging to use UTF-8 encoding
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
handler.setStream(sys.stdout)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)


session = px.launch_app()

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

falcon_lm = dspy.OpenAI(model="tiiuae/falcon-180b-chat", api_base=AI71_BASE_URL, api_key=AI71_API_KEY)

# Configure DSPy with the custom function
dspy.configure(lm=falcon_lm)

# Evaluate Team
evaluate_team = dspy.Predict(EvaluateTeamSection, n=1)

team_content = input("Tell us about your team: ")

team_response = evaluate_team(team_content=team_content)
team_score = team_response.team_score
team_feedback = team_response.team_feedback

print(f"""Team Score: {team_score}/10
Team Suggestions: 
{team_feedback}""")

# Evaluate Fundraising
evaluate_fundraising = dspy.Predict(EvaluateFundraisingSection, n=1) 

fundraising_content = input("Tell us about your fundraising: ")

fundraising_response = evaluate_fundraising(fundraising_content=fundraising_content)

fundraising_score = fundraising_response.fundraising_score
fundraising_feedback = fundraising_response.fundraising_feedback

print(f"""Fundraising Score: {fundraising_score}/10 
Fundraising Suggestions: 
{fundraising_feedback}""")

# Evaluate Market
evaluate_market = dspy.Predict(EvaluateMarketSection, n=1)

market_content = input("Tell us about your market: ")

market_response = evaluate_market(market_content=market_content)
market_score = market_response.market_score
market_feedback = market_response.market_feedback

print(f"""Market Score: {market_score}/10
Market Suggestions: 
{market_feedback}""")

# Evaluate Business Model
evaluate_business_model = dspy.Predict(EvaluateBusinessModelSection, n=1)

business_model_content = input("Tell us about your business model: ")

business_model_response = evaluate_business_model(business_model_content=business_model_content)
business_model_score = business_model_response.business_model_score
business_model_feedback = business_model_response.business_model_feedback

print(f"""Business Model Score: {business_model_score}/10
Business Model Suggestions: 
{business_model_feedback}""")

# Evaluate Product
evaluate_product = dspy.Predict(EvaluateProductSection, n=1)

product_content = input("Tell us about your product: ")

product_response = evaluate_product(product_content=product_content)
product_score = product_response.product_score
product_feedback = product_response.product_feedback

print(f"""Product Score: {product_score}/10
Product Suggestions: 
{product_feedback}""")

# Evaluate Traction
evaluate_traction = dspy.Predict(EvaluateTractionSection, n=1)

traction_content = input("Tell us about your traction: ")

traction_response = evaluate_traction(traction_content=traction_content)
traction_score = traction_response.traction_score
traction_feedback = traction_response.traction_feedback

print(f"""Traction Score: {traction_score}/10
Traction Suggestions: 
{traction_feedback}""")

#Create Spider Graphi

scores = {
    "Team": team_score,
    "Fundraising": fundraising_score,
    "Market": market_score,
    "Business Model": business_model_score,
    "Product": product_score,
    "Traction": traction_score,
}

startup_name = input("What's your startup name? ")

# Function to create a spider graph
def create_spider_graph(startup_name, scores):
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Adding the first value to the end to close the circular graph
    values += values[:1]

    N = len(categories)
    
    # Setting up the angle for each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Plot setup
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    
    # Draw the plot
    ax.fill(angles, values, color='blue', alpha=0.3)
    ax.plot(angles, values, color='blue', linewidth=2)

    # Set the category labels
    plt.xticks(angles[:-1], categories)

    # Set the scale for the radial axis
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=7)
    plt.ylim(0, 10)

    # Title of the graph
    plt.title(f"{startup_name} - Pitch Deck Scores", size=15, color='blue', y=1.1)

    # Display the plot
    plt.show()

# Example usage
create_spider_graph(startup_name, scores)

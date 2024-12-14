from PyPDF2 import PdfReader
import re
import fitz
import os
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
import dspy
from DSPyevaluate import *
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# Access environment variables
AI71_API_KEY = os.getenv("AI71_API_KEY")
AI71_BASE_URL = os.getenv("AI71_BASE_URL")

# 1: Data Cleaning
def replace_ligatures(text: str) -> str:
    ligatures = {
        "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
        "ﬅ": "ft", "ﬆ": "st", "Ꜳ": "AA", "Æ": "AE", "ꜳ": "aa"
    }
    for search, replace in ligatures.items():
        text = text.replace(search, replace)
    return text

def remove_footnotes(text: str) -> str:
    '''Removes footnotes'''
    footnote_pattern = r'\[\d+\]|\(\d+\)'
    return re.sub(footnote_pattern, '', text)

def data_cleaning(text: str) -> str:
    '''Removes hyperlinks and non-essential characters, and changes text to lowercase'''
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r"[^a-zA-Z0-9 %$]", " ", text)
    return text.lower()

def process_pdf(filepath: str) -> str:
    '''Function for processing individual PDFs'''
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    document = fitz.open(filepath)
    text_data = ""
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        data = page.get_text()
        text_data += remove_footnotes(data)
        
    text_data = replace_ligatures(text_data)
    return data_cleaning(text_data)

# 2: Main Processing
startup_name = input("What's your startup name? ")
file_path = f"uploads/{startup_name}.pdf"

try:
    pitchdeck_text = process_pdf(file_path)
except FileNotFoundError as e:
    print(e)
    exit(1)

falcon_lm = dspy.OpenAI(model="tiiuae/falcon-180b-chat", api_base=AI71_BASE_URL, api_key=AI71_API_KEY)

dspy.configure(lm=falcon_lm)

# Function to evaluate sections
def evaluate_section(section_name, evaluation_class, content):
    evaluate = dspy.Predict(evaluation_class, n=1)
    response = evaluate(**{f"{section_name}_content": content})
    score = getattr(response, f"{section_name}_score")
    feedback = getattr(response, f"{section_name}_feedback")
    return score, feedback

# Sections to evaluate
sections = {
    "team": EvaluateTeamSection,
    "fundraising": EvaluateFundraisingSection,
    "market": EvaluateMarketSection,
    "business_model": EvaluateBusinessModelSection,
    "product": EvaluateProductSection,
    "traction": EvaluateTractionSection
}

scores = {}

for section_name, evaluation_class in sections.items():
    score, feedback = evaluate_section(section_name, evaluation_class, pitchdeck_text)
    scores[section_name.replace('_', ' ').title()] = score
    print(f"{section_name.title()} Score: {score}/10\n{section_name.title()} Suggestions: \n{feedback}\n")

# 3: Create Spider Graph
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

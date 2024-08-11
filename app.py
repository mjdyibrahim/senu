from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session, jsonify
import os
import sys
from werkzeug.utils import secure_filename
import pymupdf
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import dspy
from dspy.functional import TypedPredictor
from typing import List
from DSPyevaluate import *
from StartupData import *
import instructor
from pydantic import BaseModel
import json
from ai71 import AI71 
# import phoenix as px
# from phoenix.trace.openai import OpenAIInstrumentor
import openai

# Load environment variables
load_dotenv()

# # Set the encoding for windows
# if os.name == 'nt':  # Check if the OS is Windows
#     sys.stdout.reconfigure(encoding='utf-8')
#     sys.stderr.reconfigure(encoding='utf-8')


# sys.stdin.reconfigure(encoding='utf-8-sig') 
# sys.stdout.reconfigure(encoding='utf-8-sig')

# phoenix_session = px.launch_app()

# Initialize OpenAI auto-instrumentation
# OpenAIInstrumentor().instrument()

# Access environment variables
AI71_API_KEY = os.getenv("AI71_API_KEY")
AI71_BASE_URL = os.getenv("AI71_BASE_URL")

# Flask App Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = os.getenv('SECRET_KEY')  # Load your secret key from .env

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to process PDF files
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
    
    document = pymupdf.open(filepath)
    text_data = ""
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        data = page.get_text()
        text_data += remove_footnotes(data)
        
    text_data = replace_ligatures(text_data)
    return data_cleaning(text_data)

# Function to evaluate sections using DSPy
def evaluate_section(section_name, evaluation_class, content):
    evaluate = dspy.Predict(evaluation_class, n=1)
    response = evaluate(**{f"{section_name}_content": content})
    score = getattr(response, f"{section_name}_score")
    feedback = getattr(response, f"{section_name}_feedback")


    return score, feedback

# Function to create spider graph
def create_spider_graph(startup_name, scores):
    categories = list(scores.keys())
    values = list(scores.values())

    # Trim any non numeric characters and values to floats for plotting
    values = [float(re.search(r'\d+(\.\d+)?', str(val)).group()) if re.search(r'\d+(\.\d+)?', str(val)) else 0 for val in values]
    
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

    # Save or display the plot
    plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], f"{startup_name}_spider_graph.png"))
    plt.close()

def format_feedback_to_html(feedback_text):

    # Remove any occurrence of "\nUser:"
    feedback_text = feedback_text.replace("\nUser:", "")

    # Find the position of "Falcon:" and truncate the text after it
    falcon_index = feedback_text.find("Falcon:")
    if falcon_index != -1:
        feedback_text = feedback_text[:falcon_index].strip()  # Keep text before "Falcon:"
    
    # Define regex pattern to split on *, -, or digit. (1., 2., 3., etc.)
    pattern = r'\s*\*\s*|\s*\d+\.\s*|(?<![\da-zA-Z])\s*-\s*(?![\da-zA-Z])|\n-\s*'

    
    # Split the text using the regex pattern
    items = re.split(pattern, feedback_text)

    # Initialize the HTML list
    html_list = """<ol class="feedback_text_items">"""
    
    # Split the text into individual items based on the "-" separator
    # items = feedback_text.split('*')[1:]  # Skip the first empty item resulting from the split
    
    # Ensure the items are properly formatted
    for item in items:
        if item.strip():  # Avoid adding empty items
            html_list += f"""<li>{item.strip()}</li><br />"""
    
    # Close the HTML list
    html_list += '</ol>'
    
    return html_list

# def load_json_structure(json_filepath):
#     """Load the startup.json structure."""
#     with open(json_filepath, "r") as f:
#         return json.load(f)

# def complete_missing_data(extracted_data, json_structure):
#     """Compare and fill in missing data using LLM."""
#     completed_data = {}
    
#     for key, value in json_structure.items():
#         if isinstance(value, dict) and "dataFields" in value:
#             # If it's a nested structure with dataFields, process recursively
#             completed_data[key] = complete_missing_data(
#                 extracted_data.get(key, {}), value["dataFields"]
#             )
#         elif isinstance(value, dict) and "questions" in value:
#             # If it's a nested structure with questions, handle accordingly
#             section_data = extracted_data.get(key, {})
#             completed_section_data = {}
#             for sub_key, sub_value in value["dataFields"].items():
#                 if sub_key in section_data:
#                     completed_section_data[sub_key] = section_data[sub_key]
#                 else:
#                     prompt = f"Please provide information for {sub_key}. {get_description(sub_key, value['questions'])}"
#                     completed_section_data[sub_key] = run_llm_completion(prompt)
#             completed_data[key] = completed_section_data
#         else:
#             # If it's a simple field, handle it directly
#             if key in extracted_data:
#                 completed_data[key] = extracted_data[key]
#             else:
#                 prompt = f"Please provide information for {key}. {value}"
#                 completed_data[key] = run_llm_completion(prompt)
    
#     return completed_data

# def get_description(key, questions):
#     """Retrieve the description of a key from the list of questions."""
#     for item in questions:
#         if isinstance(item, dict):
#             if key in item:
#                 return item[key]
#         elif isinstance(item, str):
#             if key in item:
#                 return item
#     return ""

# def run_llm_completion(prompt):
#     """Function to run LLM completion using LangChain with Falcon LLM."""
#     falcon_lm = dspy.OpenAI(model="tiiuae/falcon-180b-chat", api_base=AI71_BASE_URL, api_key=AI71_API_KEY)
#     dspy.configure(lm=falcon_lm)
    
#     return questions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pitchDeck' not in request.files or 'email' not in request.form:
        return "<p class='error'>No file or email provided!</p>", 400

    file = request.files['pitchDeck']
    email = request.form['email']

    if file.filename == '':
        return "<p class='error'>No selected file!</p>", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        startup_name = os.path.splitext(filename)[0]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Process the uploaded PDF
            pitchdeck_text = process_pdf(file_path)

            # Configure DSPy
            falcon_lm = dspy.OpenAI(model="tiiuae/falcon-180b-chat", api_base=AI71_BASE_URL, api_key=AI71_API_KEY)
            dspy.configure(lm=falcon_lm)

            # Evaluate sections
            sections = {
                "team": EvaluateTeamSection,
                "fundraising": EvaluateFundraisingSection,
                "market": EvaluateMarketSection,
                "business_model": EvaluateBusinessModelSection,
                "product": EvaluateProductSection,
                "traction": EvaluateTractionSection
            }

            scores = {}
            feedback = {}
            for section_name, evaluation_class in sections.items():
                print(f"Evaluating section: {section_name}") # eval
                score, feedback[section_name] = evaluate_section(section_name, evaluation_class, pitchdeck_text)
                print(f"Score: {score}, Feedback: {feedback}") # eval 
                scores[section_name.replace('_', ' ').title()] = score

            # Generate spider graph
            create_spider_graph(startup_name, scores)

            # Return the results as HTML
            output_html = f"<p>Successfully processed the file for {email}.</p>"
            output_html += f"<div><img src='/uploads/{startup_name}_spider_graph.png' alt='Spider Graph' /></div>"
            output_html += f"""<div class='scores-container'><h3>Scores:</h3>"""
            for section, score in scores.items():
                output_html += f"<div class='score-item'><span class='score-name'>{section}</span>: <span class='score-value'>{score}</span></div>"
            output_html += "</div>"
            output_html += f"""<div class="feedback-container">"""

            # Format and include feedback
            for section, section_feedback in feedback.items():
                section_score = scores.get(section.replace('_', ' ').title(), 0)
                print(f"{section_score}")
                formatted_feedback = format_feedback_to_html(section_feedback)
                output_html += f"""<div class="feedback-box"><h4>{section.replace('_', ' ').title()} Feedback: ({section_score}/10)</h4>{formatted_feedback}</div>"""

            return output_html

        except FileNotFoundError as e:
            return f"<p class='error'>{str(e)}</p>", 500

    return "<p class='error'>Invalid file type. Only PDF files are allowed.</p>", 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/entrepreneur')
def entrepreneur():
    return render_template('entrepreneur.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chat/message', methods=['POST'])
def chat_message():
    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return {"response": "No message provided."}, 400

    # Initialize session conversation history if not present
    if 'conversation_history' not in session:
        session['conversation_history'] = []

    # Append the user message to the conversation history
    session['conversation_history'].append({'sender': 'user', 'message': user_message})

    # Create context for the AI model
    conversation_history = "\n".join(f"{entry['sender']}: {entry['message']}" for entry in session['conversation_history'])


    try:
        
        ai71_client = AI71(AI71_API_KEY)
        # openai_client = openai.OpenAI(api_key=AI71_API_KEY,base_url=AI71_BASE_URL)

        system_prompt = f"""You are Senu. A Conversational AI Startup Copilot, you are in a chat window having a conversation with the user, 
                         your mission is to extract data from the user about their startup including their team, fundraising, market, business model, product and traction"""
        
        response = ""
        messages = [
            {"role": "system", "content": f"{system_prompt}"},
        ] + [
            {"role": "user", "content": f"{user_message}"}
        ]

        # Simple invocation:
        for chunk in ai71_client.chat.completions.create(
            model="tiiuae/falcon-180b-chat",
            messages=messages,
            stream=True
        ):
            if chunk.choices[0].delta.content:
                print(f"{chunk}")
                print(f"Request data: {data}")
                print(f"Conversation history: {session['conversation_history']}")
                print(f"Messages sent to API: {messages}")
                response += chunk.choices[0].delta.content
        # # Configure DSPy
        # falcon_lm = dspy.Any(model="tiiuae/falcon-11b", api_base=AI71_BASE_URL, api_key=AI71_API_KEY)
        # dspy.configure(lm=falcon_lm)
        
        # # Create a prompt for the AI
        # prompt = f"User: {user_message}"
        # conversation_history = system_prompt + prompt
        # # Generate a response using DSPy
        # response =  dspy.ChainOfThought("question, context -> answer", n=5)(question=prompt, context=conversation_history)
        print(f"{response}")

        ai_response = response
        
        # Append the bot response to the conversation history
        session['conversation_history'].append({'sender': 'assistant', 'message': ai_response})

        return {"response": ai_response}
    
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}, 500


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
import pymupdf
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import dspy
from DSPyevaluate import *
import json
from langchain.chains import LLMChain


# Load environment variables
load_dotenv()

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

def evaluate_pitch_deck(content):
    evaluate = dspy.Predict(EvaluatePitchDeck, n=1)
    response = evaluate(pitchdeck_content=content)
    return response.evaluation_results  # This would be a dict with scores and feedback


# Function to create spider graph
def create_spider_graph(startup_name, scores):
    categories = list(scores.keys())
    values = list(scores.values())

    # Trim any non numeric characters and convert values to floats for plotting
    values = [float(re.sub(r'[^0-9.]', '', str(val))) for val in values]
    
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

# def format_feedback_to_html(feedback_items):

#     # Remove any occurrence of "\nUser:"
#     feedback_items = feedback_items.replace("\nUser:", "")

#     # Initialize the HTML list
#     html_list = """<ol class="feedback_text_items">"""
    
#     # Ensure the items are properly formatted
#     for item in feedback_items:
#         if item.strip():  # Avoid adding empty items
#             html_list += f"""<li>{item.strip()}</li><br />"""
    
#     # Close the HTML list
#     html_list += '</ol>'
    
#     return html_list

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
            falcon_lm = dspy.OpenAI(model="tiiuae/falcon-180b-chat", max_tokens=1200, api_base=AI71_BASE_URL, api_key=AI71_API_KEY)
            dspy.configure(lm=falcon_lm)

            # Evaluate the entire pitch deck
            evaluation_results = evaluate_pitch_deck(pitchdeck_text)

            print(f"""\n\n ----- START LLM OUTPUT ----- \n\n {evaluation_results} \n\n ----- END LLM OUTPUT ----- \n\n""")


            # # Generate scores and feedback
            # scores = {section.replace('_', ' ').title(): data['score'] for section, data in evaluation_results.items()}
            # feedback = {section: data['feedback'] for section, data in evaluation_results.items()}


            # Generate spider graph
            # create_spider_graph(startup_name, scores)

            # Return the results as HTML
            output_html = f"<p>Successfully processed the file for {email}.</p>"
            # output_html += f"<div><img src='/uploads/{startup_name}_spider_graph.png' alt='Spider Graph' /></div>"
            # output_html += f"""<div class='scores-container'><h3>Scores:</h3>"""
            # for section, score in scores.items():
            #     output_html += f"<div class='score-item'><span class='score-name'>{section}</span>: <span class='score-value'>{score}</span></div>"
            # output_html += "</div>"
            # output_html += f"""<div class="feedback-container">"""

            # # Format and include feedback
            # for section, feedback_items in feedback.items():
            #     section_score = scores.get(section.replace('_', ' ').title(), 0)
            #     formatted_feedback = format_feedback_to_html(feedback_items)
            #     output_html += f"""<div class="feedback-box"><h4>{section.replace('_', ' ').title()} Feedback: ({section_score}/10)</h4>{formatted_feedback}</div>"""

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

if __name__ == "__main__":
    app.run(debug=True)

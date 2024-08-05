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
    # Split the text at the first newline separator
    if '\n' in feedback_text:
        feedback_text = feedback_text.split('\n', 1)[0]
    
    # Initialize the HTML list
    html_list = f"""<div class="feedback_text_items">"""
    
    # Split the text into individual items based on "1.", "2.", "3.", "4.", and "5."
    items = re.split(r'(\d+\.)\s*', feedback_text)
    
    # Ensure the items are properly formatted
    for i in range(1, len(items), 2):
        if items[i].strip():
            html_list += f"""{items[i].strip()} {items[i + 1].strip()}<br />"""
    
    # Close the HTML list
    html_list += '</div>'
    
    return html_list


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
                score, feedback[section_name] = evaluate_section(section_name, evaluation_class, pitchdeck_text)
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
                formatted_feedback = format_feedback_to_html(section_feedback)
                output_html += f"""<div class="feedback-box"><h4>{section.replace('_', ' ').title()} Feedback: ({score}/10)</h4>{formatted_feedback}</div>"""

            return output_html

        except FileNotFoundError as e:
            return f"<p class='error'>{str(e)}</p>", 500

    return "<p class='error'>Invalid file type. Only PDF files are allowed.</p>", 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)

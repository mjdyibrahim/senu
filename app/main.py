import os

# import sys
import re
from fastapi import FastAPI, Depends, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename
from .__init__ import app
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
import openai
import pymupdf
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import dspy

from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

tracer_provider = trace_sdk.TracerProvider()
span_exporter = OTLPSpanExporter("http://localhost:6006/v1/traces")
span_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)
trace_api.set_tracer_provider(tracer_provider)

from openinference.instrumentation.dspy import DSPyInstrumentor

from app.services.DSPyevaluate import *
from app.services.DSPycomplete import TeamSectionExtractor

DSPyInstrumentor().instrument()

# Determine the absolute path to your static and templates directories
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
templates_dir = os.path.join(base_dir, "templates")
uploads_dir = os.path.abspath(os.path.join(base_dir, "../uploads"))  # Ensure absolute path

app.secret_key = os.getenv("SECRET_KEY")  # Load your secret key from .env

# Mount the static directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount the uploads directory as a static files directory
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=templates_dir)


# Load environment variables
load_dotenv()

# Access environment variables
AI71_API_KEY = os.getenv("AI71_API_KEY")
AI71_BASE_URL = os.getenv("AI71_BASE_URL")

if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir, exist_ok=True)


# If you need to add any startup events or other configurations, you can do it here
@app.on_event("startup")
async def startup_event():
    # Any startup logic here
    pass

# If you need to add any shutdown events or other configurations, you can do it here
@app.on_event("shutdown")
async def shutdown_event():
    # Any shutdown logic here
    pass

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    """Serve uploaded files"""
    file_path = os.path.join(uploads_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "txt"}


# Function to check allowed file extensions
def allowed_file(filename):
    """specifies allowed file formats"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to process PDF files
def replace_ligatures(text: str) -> str:
    """replaces lignatures"""
    ligatures = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
        "Ꜳ": "AA",
        "Æ": "AE",
        "ꜳ": "aa",
    }
    for search, replace in ligatures.items():
        text = text.replace(search, replace)
    return text


def remove_footnotes(text: str) -> str:
    """Removes footnotes"""
    footnote_pattern = r"\[\d+\]|\(\d+\)"
    return re.sub(footnote_pattern, "", text)


def data_cleaning(text: str) -> str:
    """Removes hyperlinks and non-essential characters, and changes text to lowercase"""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9 %$]", " ", text)
    return text.lower()


def process_pdf(filepath: str) -> str:
    """Function for processing individual PDFs"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    document = pymupdf.open(filepath)
    text_data = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        data = page.get_text()
        text_data += remove_footnotes(data)
    text_data = replace_ligatures(text_data)
    cleaned_text = data_cleaning(text_data)
    data_points = extract_data_points(cleaned_text)
    print(data_points)
    return cleaned_text


def extract_data_points(text: str, llm_model="tiiuae/falcon-180b-chat") -> dict:
    """"
    Extracts data points from user input using LLM

    Args:
        text (str): User input text
        llm_model (str, optional): Name of the LLM model to use. Defaults to "tiiuae/falcon-180b-chat".

    Returns:
        dict: Dictionary containing extracted data points with keys as labels and values as extracted data.
    """
    # data_points = {
    #     "users": {
    #         "username": extract_username(text),
    #         "email": extract_email(text),
    #         "password_hash": extract_password_hash(text),
    #     },
    #     "startups": {
    #         "name": extract_startup_name(text),
    #         "tagline": extract_tagline(text),
    #         "description": extract_description(text),
    #         "date_started": extract_date_started(text),
    #         "registration_type": extract_registration_type(text),
    #         "registration_country": extract_registration_country(text),
    #         "email": extract_startup_email(text),
    #         "phone": extract_phone(text),
    #         "address": extract_address(text),
    #         "owner": extract_owner(text),
    #     },
    # }
    
    # Configure DSPy (if needed)
    falcon_lm = dspy.OpenAI(model=llm_model, base_url=AI71_BASE_URL, api_key=AI71_API_KEY)
    dspy.configure(lm=falcon_lm)

    # Define prompts for extracting specific data points (e.g., team size, market size)
    prompts = {
        "team_size": "What is the size of the founding team based on the provided text?",
        "market_size": "What is the estimated size of the target market based on the text?",
        # Add more prompts for other data points you want to extract
    }

    data_points = {}
    for label, prompt in prompts.items():
    # Call LLM to extract data based on the prompt
        response = dspy.ChainOfThought(signature=TeamSectionExtractor, n=1)(pitchdeck_content=text)
    print(response)    
    data_points[label] = response

    return data_points


# Function to evaluate sections using DSPy
def evaluate_section(section_name, evaluation_class, content):
    """sends input for DSPY function"""
    evaluate = dspy.Predict(evaluation_class, n=1)
    response = evaluate(**{f"{section_name}_content": content})
    score = getattr(response, f"{section_name}_score")
    feedback = getattr(response, f"{section_name}_feedback")
    return score, feedback


# Function to create spider graph
def create_spider_graph(startup_name, scores):
    """function that creates a spider graph from collected scores"""
    categories = list(scores.keys())
    values = list(scores.values())

    # Trim any non numeric characters and values to floats for plotting
    values = [
        (
            float(re.search(r"\d+(\.\d+)?", str(val)).group())
            if re.search(r"\d+(\.\d+)?", str(val))
            else 0
        )
        for val in values
    ]

    # Adding the first value to the end to close the circular graph
    values += values[:1]

    n = len(categories)

    # Setting up the angle for each axis
    angles = [i / float(n) * 2 * np.pi for i in range(n)]
    angles += angles[:1]

    # Plot setup
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    # Draw the plot
    ax.fill(angles, values, color="green", alpha=0.3)
    ax.plot(angles, values, color="green", linewidth=2)

    # Set the category labels
    plt.xticks(angles[:-1], categories)

    # Set the scale for the radial axis
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=7)
    plt.ylim(0, 10)

    # Title of the graph
    plt.title(f"{startup_name} - Pitch Deck Scores", size=15, color="green", y=1.1)

    # Save or display the plot
    plt.savefig(
        os.path.join(uploads_dir, f"{startup_name}_spider_graph.png")
    )
    plt.close()


def format_feedback_to_html(feedback_text):
    """This function takes feedback from LLM and format it for addition to the front end"""
    # Remove any occurrence of "\nUser:"
    feedback_text = feedback_text.replace("\nUser:", "")

    # Find the position of "Falcon:" and truncate the text after it
    falcon_index = feedback_text.find("Falcon:")
    if falcon_index != -1:
        feedback_text = feedback_text[
            :falcon_index
        ].strip()  # Keep text before "Falcon:"

    # Define regex pattern to split on *, -, or digit. (1., 2., 3., etc.)
    pattern = r"\s*\*\s*|\s*\d+\.\s*|(?<![\da-zA-Z])\s*-\s*(?![\da-zA-Z])|\n-\s*"

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
    html_list += "</ol>"

    return html_list


# def load_json_structure(json_filepath):
#     """Load the startup.json structure."""
#     with open(json_filepath, "r") as f:
#         return json.load(f)
#
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
#
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
#
# def run_llm_completion(prompt):
#     """Function to run LLM completion using LangChain with Falcon LLM."""
#     falcon_lm = dspy.OpenAI(model="tiiuae/falcon-180b-chat", base_url=AI71_BASE_URL, api_key=AI71_API_KEY)
#     dspy.configure(lm=falcon_lm)
#
#     return questions


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_file(email: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Processes actions for file upload"""
    if not file or not email:
        return {"error": "No file or email provided!"}, 400

    if file.filename == "":
        return {"error": "No selected file!"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        startup_name = os.path.splitext(filename)[0]
        file_extension = os.path.splitext(filename)[1].lower()
        file_path = os.path.join(uploads_dir, filename)
        try:
            with open(file_path, "wb") as f:
                f.write(await file.read())

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not saved correctly: {file_path}")

            # Process the uploaded file
            if file_extension == ".pdf":
                pitchdeck_text = process_pdf(file_path)
            elif file_extension == ".txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    pitchdeck_text = f.read()

            # Configure DSPy
            falcon_lm = dspy.OpenAI(
                model="tiiuae/falcon-180b-chat",
                base_url=AI71_BASE_URL,
                api_key=AI71_API_KEY,
            )
            dspy.configure(lm=falcon_lm)

            # Evaluate sections
            sections = {
                "team": EvaluateTeamSection,
                "fundraising": EvaluateFundraisingSection,
                "market": EvaluateMarketSection,
                "business_model": EvaluateBusinessModelSection,
                "product": EvaluateProductSection,
                "traction": EvaluateTractionSection,
            }

            scores = {}
            feedback = {}
            for section_name, evaluation_class in sections.items():
                print(f"Evaluating section: {section_name}")  # eval
                score, feedback[section_name] = evaluate_section(
                    section_name, evaluation_class, pitchdeck_text
                )
                print(f"Score: {score}, Feedback: {feedback}")  # eval
                scores[section_name.replace("_", " ").title()] = score

            # Generate spider graph
            create_spider_graph(startup_name, scores)

            # Return the results as HTML
            output_html = f"<p>Successfully processed the file for {email}.</p>"
            output_html += f"<div><img src='/uploads/{startup_name}_spider_graph.png' alt='Spider Graph' /></div>"
            output_html += """<div class='scores-container'><h3>Scores:</h3>"""
            for section, score in scores.items():
                output_html += f"<div class='score-item'><span class='score-name'>{section}</span>: <span class='score-value'>{score}</span></div>"
            output_html += "</div>"
            output_html += """<div class="feedback-container">"""

            # Format and include feedback
            for section, section_feedback in feedback.items():
                section_score = scores.get(section.replace("_", " ").title(), 0)
                print(f"{section_score}")
                formatted_feedback = format_feedback_to_html(section_feedback)
                output_html += f"""<div class="feedback-box"><h4>{section.replace('_', ' ').title()} Feedback: ({section_score}/10)</h4>{formatted_feedback}</div>"""

            return output_html

        except FileNotFoundError as e:
            return {"error": str(e)}, 500

    return {"error": "Invalid file type. Only PDF and TXT files are allowed."}, 400

@app.get("/feedback")
async def feedback(request: Request):
    """Feedback Page"""
    return templates.TemplateResponse("feedback.html", {"request": request})


@app.get("/resources")
async def resources(request: Request):
    """Resources page"""
    return templates.TemplateResponse("resources.html", {"request": request})


@app.get("/signin")
async def signin(request: Request):
    """Signin page"""
    return templates.TemplateResponse("signin.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app.main, host="0.0.0.0", port=8000)

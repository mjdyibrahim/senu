import os
from dotenv import load_dotenv
from ai71 import AI71
import fitz 
import re

load_dotenv()

AI71_API_KEY = os.getenv("AI71_API_KEY")

client = AI71(AI71_API_KEY)

def process_pitch_deck(filename):
    # Here, you'd typically extract text from the pitch deck file
    # For simplicity, let's assume we have the extracted text as `pitch_deck_text`
    pitch_deck_text = extract_text_from_pitch_deck(filename)
    return pitch_deck_text

def generate_scorecard(pitch_deck_text):
    # Prepare the message for Falcon LLM
    messages = [
        {"role": "system", "content": "You are a business evaluation assistant."},
        {"role": "user", "content": f"Evaluate this pitch deck and provide a score from 1 to 10 for the following categories:\n\n{pitch_deck_text}\n\nCategories:\n1. Team\n2. Market\n3. Business Model\n4. Product\n5. Traction/Sales\n6. Finances/Fundraising\n7. Innovation"}
    ]

    # Send the request to Falcon LLM
    scorecard = ""
    for chunk in client.chat.completions.create(
        messages=messages,
        model="tiiuae/falcon-180B-chat",
        stream=True,
    ):
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            scorecard += delta_content

    # Extract the scores from the scorecard text (you might need to refine this part depending on the LLM output)
    scores = extract_scores_from_scorecard(scorecard)
    
    return scorecard, scores

def extract_scores_from_scorecard(scorecard_text):
    # Placeholder function to parse the scorecard text and extract scores
    # You'd need to implement the logic to extract numerical scores from the scorecard text
    scores = {
        "Team": 7,  # Example value; replace with actual extraction logic
        "Market": 6,
        "Business Model": 5,
        "Product": 8,
        "Traction": 4,
        "Fundraising": 7,
        "Innovation": 9
    }
    return scores

def extract_text_from_pitch_deck(filename):
    # Open the PDF file
    document = fitz.open(filename)
    text = ""

    # Extract text from each page
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()

    # Define sections to look for
    sections = {
        "Info": "",
        "Team": "",
        "Market": "",
        "Business Model": "",
        "Product": "",
        "Traction": "",
        "Fundraising": ""
        
    }

    # Use regular expressions to find sections
    current_section = None
    for line in text.split("\n"):
        line = line.strip()
        if line:
            # Check if the line matches a section header
            if re.match(r'^(Info|Team|Market|Business Model|Product|Traction/Sales|Finance/Fundraising)', line, re.IGNORECASE):
                current_section = line.split()[0]
                sections[current_section] = line
            elif current_section:
                sections[current_section] += " " + line

    return sections

# Example usage
filename = "uploads/pitchdeck.pdf"
extracted_sections = extract_text_from_pitch_deck(filename)
for section, content in extracted_sections.items():
    print(f"{section}:\n{content}\n")

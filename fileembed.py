from PyPDF2 import PdfReader
import re
import fitz
import os
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth
import cohere

# Define the path to the marker file
marker_file_path = "weaviate_class_created.txt"

# Load environment variables
load_dotenv()

# Access environment variables
AI71_API_KEY = os.getenv("AI71_API_KEY")
AI71_BASE_URL = os.getenv("AI71_BASE_URL")
COHERE_API_KEY = os.getenv("COHERE_APIKEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")

# Connect to Weaviate
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(api_key=WEAVIATE_API_KEY),
    headers={'X-Cohere-Api-Key': COHERE_API_KEY} 
)

# Connect to Cohere
co = cohere.Client(COHERE_API_KEY)

# 1: Data Cleaning
def replace_ligatures(text: str) -> str:
    ligatures = {
        "ﬀ": "ff",
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

def remove_footnotes(text):
    '''Removes footnotes'''
    footnote_pattern = r'\[\d+\]|\(\d+\)'
    cleaned_text = re.sub(footnote_pattern, '', text)
    return cleaned_text

def data_cleaning(text):
    '''Removes hyperlinks and non-essential characters, and changes text to lowercase'''
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r"[^a-zA-Z0-9 %$]", " ", text)
    text = text.lower()
    return text

def create_weaviate_class():
    # Check if the class already exists in Weaviate
    if not client.collections.exists("Senu"):
        # Define a data collection (class) in Weaviate
        try:
            collection = client.collections.create(
                name="Senu",
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_cohere(),
                generative_config=weaviate.classes.config.Configure.Generative.cohere()
                )

        finally:
            client.close()
        
        # Create the marker file
        with open(marker_file_path, "w") as f:
            f.write("Weaviate class created")
        print("Weaviate class 'Senu' created.")
    else:
        print("Weaviate class 'Senu' already exists.")

def process_pdf(filepath, mode="str"):
    '''Function for processing individual PDFs'''
    
    # Extract filename without extension
    filename = os.path.splitext(os.path.basename(filepath))[0]
    
    document = fitz.open(filepath)
    text_data = ""
    
    try:
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            data = page.get_text()
            data = remove_footnotes(data)
            text_data += data
            
        text_data = replace_ligatures(text_data)
        text_data = data_cleaning(text_data)
        
        # Embed text data using Cohere
        embeds = co.embed(texts=[text_data], model="multilingual-22-12").embeddings

        # Save embeddings to a single numpy array file
        all_embeddings_array = np.array(embeds)
        np.save(f"{filename}_embeddings.npy", all_embeddings_array)

        # Process embeddings for the text
        for embedding in tqdm(embeds):
            # Create a Weaviate object with the text and embedding
            object_data = {
                "text": text_data,
                "embedding": embedding
            }

            try: 
                # Add the object to the Weaviate collection
                collection = client.collections.get("Senu")
                collection.data.insert(object_data)
            finally:
                client.close
            
    finally:
        
        # Ensure the document is closed after processing
        document.close()

    return text_data, client, embeds


def main():
    # Call create_weaviate_class() to ensure the class is created before processing files
    create_weaviate_class()

    # Process each file
    file_paths = ["uploads/pitchdeck.pdf"]  # Example file paths, replace with your actual file paths
    for file_path in file_paths:
        process_pdf(file_path)

    # Ensure the Weaviate connection is closed after processing
    client.close()

if __name__ == "__main__":
    main()

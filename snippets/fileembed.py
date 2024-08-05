from PyPDF2 import PdfReader
import re
import fitz
import os
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
import weaviate
import json
from weaviate.classes.init import Auth
import weaviate.classes.config as wvcc

import cohere

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
    for idx, word in enumerate(text):
        if re.match(r'^\$\d+(,\d{3})*$', word):
            text[idx] = re.sub(r',', '', word)
    
    #removes phone numbers    
    phone_pattern = r'(\+?\d{1,4}[\s.-]?)?(\(?\d{1,4}\)?[\s.-]?)?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}'
    text = re.sub(phone_pattern, '', text).strip()

    #removes bullets
    bullet_pattern = r'^\s*(?:[\d]+[.\)\-]|\s*[-*•]+)\s*'
    text = re.sub(bullet_pattern, '', text, flags=re.MULTILINE).strip()

    #removes hyperlinks
    url_pattern = r'\bhttps?:\/\/\S+|www\.\S+|@\S+'
    text = re.sub(url_pattern, '', text).strip()
    
    #removes non alphanumeric characters
    text = re.sub(r"[^a-zA-Z0-9 %$]", " ", text)
    text = text.lower()
    
    return text

def create_weaviate_class():
    # Check if the class already exists in Weaviate
    if not client.collections.exists("senu"):
        # Define a data collection (class) in Weaviate
        try:
            collection = client.collections.create(
                name="senu",
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_cohere(),
                generative_config=weaviate.classes.config.Configure.Generative.cohere(
                    model="embed-multilingual-v3.0"
                ),
                properties=[
                        wvcc.Property(name="startup", data_type=wvcc.DataType.TEXT),
                        wvcc.Property(name="text", data_type=wvcc.DataType.TEXT),
                        wvcc.Property(name="embedding", data_type=wvcc.DataType.INT_ARRAY),
                ]
            )

        finally:
            client.close()
    
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
                "startup": filename,
                "text": text_data,
                "embedding": json.dumps(convert_embedding_to_int_array(embedding))
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

def convert_embedding_to_int_array(embedding):
            # Convert to a NumPy array
            embedding_array = np.array(embedding)
            # Convert to integers (e.g., rounding or casting)
            int_array = embedding_array.astype(int)
            # Convert to list for JSON serialization
            return int_array.tolist()

def main():
    # Call create_weaviate_class() to ensure the class is created before processing files
    create_weaviate_class()

    # Process each file
    file_paths = ["uploads/lyla.pdf"]  # Example file paths, replace with your actual file paths
    for file_path in file_paths:
        process_pdf(file_path)

    # Ensure the Weaviate connection is closed after processing
    client.close()

if __name__ == "__main__":
    main()

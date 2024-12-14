import weaviate
from weaviate.classes.init import Auth
import re
import pymupdf
import os
from unstructured.partition.pdf import partition_pdf
from pathlib import Path
import weaviate
from weaviate.embedded import EmbeddedOptions
import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

class pdfExtractor:
    def replace_ligatures(self, text: str) -> str:
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


    def remove_footnotes(self, text: str) -> str:
        """Removes footnotes"""
        footnote_pattern = r"\[\d+\]|\(\d+\)"
        return re.sub(footnote_pattern, "", text)


    def data_cleaning(self, text: str) -> str:
        """Removes hyperlinks and non-essential characters, and changes text to lowercase"""
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z0-9 %$]", " ", text)
        return text.lower()


    def process_pdf(self, filepath: str) -> str:
        """Function for processing individual PDFs"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        document = pymupdf.open(filepath)
        text_data = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            data = page.get_text()
            text_data += self.remove_footnotes(data)
        text_data = self.replace_ligatures(text_data)
        return self.data_cleaning(text_data)
    



class AbstractExtractor:
    def __init__(self):
        self.current_section = None  # Keep track of the current section being processed
        self.have_extracted_abstract = (
            False  # Keep track of whether the abstract has been extracted
        )
        self.in_abstract_section = (
            False  # Keep track of whether we're inside the Abstract section
        )
        self.texts = []  # Keep track of the extracted abstract text

    def process(self, element):
        if element.category == "Title":
            self.set_section(element.text)

            if self.current_section == "Abstract":
                self.in_abstract_section = True
                return True

            if self.in_abstract_section:
                return False

        if self.in_abstract_section and element.category == "NarrativeText":
            self.consume_abstract_text(element.text)
            return True

        return True

    def set_section(self, text):
        self.current_section = text
        logging.info(f"Current section: {self.current_section}")

    def consume_abstract_text(self, text):
        logging.info(f"Abstract part extracted: {text}")
        self.texts.append(text)

    def consume_elements(self, elements):
        for element in elements:
            should_continue = self.process(element)

            if not should_continue:
                self.have_extracted_abstract = True
                break

        if not self.have_extracted_abstract:
            logging.warning("No abstract found in the given list of objects.")

    def abstract(self):
        return "\n".join(self.texts)    


class IngestPDFs:
    def connectToWeaviate(self):
        
        '''function for connecting to weaviate client'''
        
        try:
            self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=os.getenv("WEAVIATE_URL"),
            auth_credentials=Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
            headers={
                "X-Cohere-Api-Key": os.getenv("COHERE_API_KEY")
            }
        )
        except:
            print("Error connecting to Weaviate")
            
    def defineSchema(self, schema):
        
        '''defines document schema and creates it on Weaviate'''
        
        return self.client.schema.create_class(schema)
    
    def import_pdfs(self, data_folder):
        
        '''Import pdfs about entrepreneurship from your folder'''
        data_objects = []
        
        for path in Path(data_folder).iterdir():
            if path.suffix != ".pdf":
                continue
        
            print(f"Processing {path.name}...")
        
            elements = partition_pdf(filename=path)
        
            abstract_extractor = AbstractExtractor()
            abstract_extractor.consume_elements(elements)
        
            data_object = {"source": path.name, "abstract": abstract_extractor.abstract()}
        
            data_objects.append(data_object)
        return data_objects
    
    
    def ingest_pdfs(self, batch_size, data_objects):
        
        '''Ingest pdfs into Weaviate'''

        self.client.batch.configure(batch_size)  # Configure batch
        with self.client.batch as batch:
            for data_object in data_objects:
                batch.add_data_object(data_object, "Document")
        
        print("Completed")
        
    
    def execute(self):
        self.connectToWeaviate()
        
        #define your data schema here
        self.schema = []
        self.defineSchema(self.schema)
        
        #insert your data folder filepath as a variable
        data_objects = self.import_pdfs("")
        self.ingest_pdfs(len(data_objects), data_objects)
        
        #disconnect from weaviate
        self.client.close()
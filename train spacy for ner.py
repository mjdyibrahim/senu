1# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:50:53 2024

@author: hf_qu
"""
import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import psycopg2


# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 21:34:42 2024

@author: hf_qu
"""

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

#1: Data Cleaning
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
    
    '''removes footnotes'''
    
    footnote_pattern = r'\[\d+\]|\(\d+\)'
    cleaned_text = re.sub(footnote_pattern, '', text)
    
    return cleaned_text


def data_cleaning(text):
    '''comprehensive text cleaning function'''
    
    
    #turns $250,000 to $250000
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



def process_pdf(filepath, mode="str"):
    '''Function for processing individual PDFs'''
    
    # Extract filename without extension
    filename = os.path.splitext(os.path.basename(filepath))[0]
    
    document = fitz.open(filepath)
    text_data = ""
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        data = page.get_text()
        data = remove_footnotes(data)
        text_data += data
        
    text_data = replace_ligatures(text_data)
    text_data = data_cleaning(text_data)
    return text_data


def train_spacy(text, labels, train_data):
    '''#manually add the labels and train_data for training
   ''' 
    nlp = spacy.blank("en")
    textCat = nlp.add_pipe("senu")
    for label in labels:
        textCat.add_label(label)
    
    n_iter = 100
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        losses = {}
        # Shuffle the training data
        examples = train_data.copy()
        # Create batches of training data
        batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
    
        for batch in batches:
            for text, annotations in batch:
                # Create an Example object
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                # Update the model
                nlp.update([example], sgd=optimizer, drop=0.5, losses=losses)
        
        print(f"Iteration {i} Losses: {losses}")

    nlp.to_disk("senu")
    return nlp




class data:
    def connect(self, hostname, database, username, pwd, port_id):
        self.conn, self.cur = None, None    
        try:
            self.conn = psycopg2.connect(
                ho.st = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
                )
            self.cur = self.conn.cursor()
    
        except Exception as error:
            print(error)
            
            
    def ner(self, text):
        
        '''named entity recognition'''
        
        self.model = spacy.load("senu")
        doc = self.model(text)
        
        #define data schema here
        create_script = '''CREATE TABLE IF NOT EXISTS startup
        ()
        '''
        
        self.cur.execute(create_script)
        
        #need knowledge of the data schema
        insert_script = '''INSERT INTO startup () VALUES()'''
        insert_value = []
        
        self.cur.execute(insert_script, insert_value)
        self.conn.commit()
        
    def search(self, query):
        self.cur.execute(f"SELECT {query} FROM STARTUP")
        records = self.cur.fetchall()
        return records
        
    
        
    def disconnect(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
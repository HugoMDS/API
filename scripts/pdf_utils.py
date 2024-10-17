# scripts/pdf_utils.py
import requests
import PyPDF2
from io import BytesIO

def download_pdf(url):
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si la requête a réussi
    return BytesIO(response.content)

def pdf_to_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text() + "\n"
    
    return text
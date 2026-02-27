import os

from docx import Document
from pdfminer.high_level import extract_text


def extract_file_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text(file_path)
    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()


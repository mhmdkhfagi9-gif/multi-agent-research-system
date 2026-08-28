"""
PDF reading tool. Extracts plain text from PDF files under data/documents/.
Used by the PDF sub-agent inside retrieval_agent.py.
"""

import os
from pypdf import PdfReader


def read_pdf(path: str) -> str:
    """Extracts all text from a single PDF file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text.strip()


def read_all_pdfs(directory: str) -> dict:
    """Reads every PDF in a directory. Returns {filename: text}."""
    results = {}
    if not os.path.isdir(directory):
        return results

    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(directory, filename)
            try:
                results[filename] = read_pdf(path)
            except Exception as e:
                results[filename] = f"[ERROR reading {filename}: {e}]"
    return results

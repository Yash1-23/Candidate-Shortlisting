import os
import csv
import nltk
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text



import re

def extract_metadata(text):
    """Extract metadata such as email, phone, and profile links from text."""
    # Extract email
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    email_match = re.search(email_pattern, text)
    email = email_match.group(0) if email_match else ""

    # Extract GitHub profile link
    github_pattern = r'github\.com/[\w-]+'
    github_match = re.search(github_pattern, text)
    github_link = "https://" + github_match.group(0) if github_match else ""

    # Extract phone number
    phone_pattern = r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})\b'
    phone_match = re.search(phone_pattern, text)
    phone = phone_match.group(0) if phone_match else "N/A"

    return email, phone, github_link


def generate_summary(text):
    """Generate a summary of the text."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=2)
    return " ".join(str(sentence) for sentence in summary)


def process_resume(pdf_folder):
    """Process resumes in PDF format and generate a summarized CSV."""
    header = ["File Name", "Email", "Phone", "LinkedIn Profile", "GitHub Profile", "Summary"]
    rows = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_folder, filename)
            text = extract_text_from_pdf(file_path)
            email, phone, profile_links = extract_metadata(text)
            summary = generate_summary(text)
            rows.append([filename, email, phone] + [summary] + list(profile_links))

    # Writing data to CSV
    with open("resume_summary.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    # Provide the path to the folder containing PDF resumes
    pdf_folder_path = "C:/Users/anitha/OneDrive/Desktop/DZYLO Assignment/PDF/PDF"
    process_resume(pdf_folder_path)
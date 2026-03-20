# ai/cv_parser.py
from pypdf import PdfReader
from openai import OpenAI
import json
from config import GROQ_API_KEY

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_cv_with_llm(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    prompt = f"""
Tu es un assistant expert en recrutement.
Analyse ce CV et retourne UNIQUEMENT un JSON structuré :

{{
  "name": "...",
  "email": "...",
  "school": "...",
  "specialty": "...",
  "skills": ["...", "..."],
  "experience": ["...", "..."]
}}

CV:
{text}
"""

    response = client.chat.completions.create(       
        model="llama-3.3-70b-versatile",            
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    result = response.choices[0].message.content    
    return json.loads(result)
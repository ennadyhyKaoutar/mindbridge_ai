import os
from dotenv import load_dotenv
from pathlib import Path

# ✅ Force le chemin absolu vers le .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")  # exemple: us-west1-gcp
PINECONE_INDEX_NAME = "mindbridge-talents"
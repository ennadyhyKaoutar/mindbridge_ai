from pinecone import Pinecone
from google import genai
from config import GEMINI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME

# --- Client Gemini ---
client = genai.Client(api_key=GEMINI_API_KEY)

# --- Pinecone ---
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# --- Embeddings avec Gemini ---
def get_gemini_embedding(text):
    try:
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Erreur de modèle : {e}. Tentative avec le modèle de secours...")
        response = client.models.embed_content(
            model="models/text-embedding-001",
            contents=text
        )
        return response.embeddings[0].values

def store_embedding(talent_id, embedding, metadata):
    index.upsert(vectors=[{
        "id": talent_id,
        "values": embedding,
        "metadata": metadata
    }])

def search_embedding(vector, top_k=5):
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )
    return results
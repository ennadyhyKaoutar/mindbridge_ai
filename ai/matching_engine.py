from ai.embeddings import get_gemini_embedding, store_embedding, search_embedding, index
from openai import OpenAI
from config import GROQ_API_KEY

# ✅ Groq pour la génération de raison
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

def add_talent_to_db(talent_id, cv_text, name, specialty):
    embedding = get_gemini_embedding(cv_text)
    if embedding:
        metadata = {
            "name": name,
            "specialty": specialty,
            "cv": cv_text
        }
        store_embedding(talent_id, embedding, metadata)
        print(f"✅ Talent {name} ajouté à la base.")
    else:
        print(f"❌ Impossible de générer l'embedding pour {name}.")


def find_best_talents(profile_text, top_k=3):
    """
    Cherche les top_k talents qui matchent le profil.
    Filtre par specialty si des talents de ce profil existent.
    Sinon retourne les meilleurs globalement.
    """
    query_embedding = get_gemini_embedding(profile_text)

    # ✅ 1. Essayer d'abord avec filtre par specialty
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={"specialty": {"$eq": profile_text}}  # filtre exact
    )

    # ✅ 2. Si pas assez de résultats → recherche globale sans filtre
    if len(results['matches']) < top_k:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

    top_talents = []
    for match in results['matches']:
        meta = match['metadata']

        reason_prompt = (
            f"En une phrase courte en français, explique pourquoi ce candidat "
            f"(Spécialité: {meta['specialty']}) est un bon match pour ce poste: {profile_text}. "
            f"Voici son CV: {meta['cv'][:500]}"
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": reason_prompt}],
            temperature=0.3,
        )

        top_talents.append({
            "name": meta['name'],
            "specialty": meta['specialty'],
            "score": round(match['score'] * 100, 2),
            "reason": response.choices[0].message.content.strip()
        })

    return top_talents
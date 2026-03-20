# ai/mission_decomposer.py
from openai import OpenAI
import json
from config import GROQ_API_KEY

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

def decompose_mission(mission_text: str):
    prompt = f"""
Analyse cette mission et retourne les sous-missions avec le profil requis.

Mission:
{mission_text}

Retourne UNIQUEMENT un JSON valide, sans texte avant ou après :

{{
  "subtasks": [
    {{"task": "...", "profile": "..."}}
  ]
}}
"""
    response = client.chat.completions.create(      # ← fix
        model="llama-3.3-70b-versatile",                    # ← modèle Groq
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},    # ← force JSON
    )

    result = response.choices[0].message.content
    return json.loads(result)
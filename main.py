# main.py
from ai.mission_decomposer import decompose_mission
from ai.matching_engine import add_talent_to_db, find_best_talents

# --- 1️⃣ Ajouter des talents fictifs variés ---
print("Ajout des talents dans la base...\n")

# Finance
add_talent_to_db("1", "Étudiant en finance avec expérience en modélisation financière et valorisation d'entreprise", "Ahmed", "Finance")
add_talent_to_db("2", "Expert comptable avec 5 ans d'expérience en audit financier et reporting", "Karim", "Finance")
add_talent_to_db("3", "Analyste financier spécialisé en gestion de portefeuille et analyse de risque", "Nadia", "Finance")

# Marketing
add_talent_to_db("4", "Étudiante en marketing spécialisée en études de marché et stratégie digitale", "Sara", "Marketing")
add_talent_to_db("5", "Chef de projet marketing avec expérience en campagnes publicitaires et SEO", "Leila", "Marketing")
add_talent_to_db("6", "Spécialiste en marketing international et analyse de marché européen", "Omar", "Marketing")

# Data / Tech
add_talent_to_db("7", "Analyste de données avec Python et machine learning, expérience en NLP", "Youssef", "Data")
add_talent_to_db("8", "Data scientist spécialisé en deep learning et analyse prédictive", "Mehdi", "Data")
add_talent_to_db("9", "Développeur Python full-stack avec expérience en API REST et bases de données", "Ines", "Data")

# RH
add_talent_to_db("10", "Responsable RH avec expérience en recrutement et gestion des talents", "Fatima", "RH")
add_talent_to_db("11", "Consultant RH spécialisé en formation et développement des compétences", "Adam", "RH")

# Juridique
add_talent_to_db("12", "Juriste spécialisé en droit des affaires et contrats internationaux", "Sofia", "Juridique")
add_talent_to_db("13", "Avocat avec expérience en droit du travail et conformité réglementaire", "Hamza", "Juridique")

# --- 2️⃣ Mission de test ---
mission_text = """
Nous voulons étendre notre activité en Europe.
Nous avons besoin d'une analyse de marché et d'une analyse financière.
"""

print("\nDécomposition de la mission...\n")
subtasks = decompose_mission(mission_text)

print("Sous-missions extraites :")
for s in subtasks["subtasks"]:
    print(f"- {s['task']} | Profil requis: {s['profile']}")

# --- 3️⃣ Matching ---
print("\n--- Matching Talents par sous-mission ---\n")
for subtask in subtasks["subtasks"]:
    profile_needed = subtask["profile"]
    print(f"Sous-mission : {subtask['task']}")
    print(f"Profil requis : {profile_needed}\n")

    top_talents = find_best_talents(profile_needed, top_k=3)

    for i, talent in enumerate(top_talents, start=1):
        print(f"{i}. {talent['name']} ({talent['specialty']}) - Score: {talent['score']:.2f}")
        print(f"   Raison : {talent['reason']}\n")
    print("---------------------------------------------------\n")
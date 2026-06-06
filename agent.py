from groq import Groq
import os
from dotenv import load_dotenv
from database import supabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def lire_articles(boutique_id):
    return supabase.table("articles").select("*").eq("boutique_id", boutique_id).execute().data

def lire_categories(boutique_id):
    return supabase.table("categories").select("*").eq("boutique_id", boutique_id).execute().data

def poser_question(question, historique=[], boutique_id=None):
    articles = lire_articles(boutique_id)
    categories = lire_categories(boutique_id)

    # Calculer quelques stats
    valeur_stock = sum(a["prix"] * a["quantite"] for a in articles if a["prix"] and a["quantite"])
    epuises = [a["nom"] for a in articles if a["quantite"] == 0]
    faible_stock = [a["nom"] for a in articles if a["quantite"] and 0 < a["quantite"] <= 5]

    system_prompt = f"""Tu es un assistant intelligent qui aide un commerçant à gérer son stock.

Voici les données actuelles :
- Articles : {articles}
- Catégories : {categories}
- Valeur totale du stock : {valeur_stock} FCFA
- Articles épuisés : {epuises}
- Articles avec stock faible (≤5) : {faible_stock}

Réponds toujours en français, de manière claire et concise."""

    messages = [{"role": "system", "content": system_prompt}] + historique + [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000
    )

    return response.choices[0].message.content
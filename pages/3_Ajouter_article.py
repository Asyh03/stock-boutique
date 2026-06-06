import streamlit as st
from database import supabase

if "boutique" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

boutique_id = st.session_state.boutique["id"]

st.title("➕ Ajouter un article")

# Récupérer les catégories
categories = supabase.table("categories").select("*").eq("boutique_id", boutique_id).execute().data
categories_dict = {c["nom"]: c["id"] for c in categories}

if not categories:
    st.warning("Vous n'avez pas encore de catégories. Créez-en une d'abord !")
    st.stop()

with st.form("ajouter_article"):
    nom = st.text_input("Nom de l'article *")
    description = st.text_area("Description")
    prix = st.number_input("Prix (FCFA)", min_value=0)
    quantite = st.number_input("Quantité", min_value=0)
    categorie = st.selectbox("Catégorie *", list(categories_dict.keys()))
    soumettre = st.form_submit_button("Ajouter")

    if soumettre:
        if not nom:
            st.error("Le nom est obligatoire !")
        else:
            supabase.table("articles").insert({
                "nom": nom,
                "description": description,
                "prix": prix,
                "quantite": quantite,
                "categorie_id": categories_dict[categorie],
                "boutique_id": boutique_id
            }).execute()
            st.success(f"**{nom}** ajouté avec succès ! ✅")
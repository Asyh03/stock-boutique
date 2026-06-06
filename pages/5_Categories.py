import streamlit as st
from database import supabase

if "boutique" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

boutique_id = st.session_state.boutique["id"]

st.title("🗂️ Catégories")

# Récupérer les catégories
categories = supabase.table("categories").select("*").eq("boutique_id", boutique_id).execute().data

# Afficher les catégories
st.subheader("Liste des catégories")

if categories:
    for c in categories:
        # Compter les articles par catégorie
        nb_articles = len(supabase.table("articles").select("id").eq("categorie_id", c["id"]).execute().data)

        col1, col2, col3 = st.columns([4, 2, 1])
        col1.write(f"**{c['nom']}**")
        col2.write(f"📦 {nb_articles} article(s)")

        with col3:
            if st.button("🗑️", key=f"del_{c['id']}"):
                if nb_articles > 0:
                    st.error("Impossible de supprimer une catégorie qui contient des articles !")
                else:
                    supabase.table("categories").delete().eq("id", c["id"]).execute()
                    st.success("Catégorie supprimée ✅")
                    st.rerun()
        st.divider()
else:
    st.info("Aucune catégorie enregistrée.")

# Ajouter une catégorie
st.subheader("➕ Ajouter une catégorie")

with st.form("ajouter_categorie"):
    nom = st.text_input("Nom de la catégorie *")
    soumettre = st.form_submit_button("Ajouter")

    if soumettre:
        if not nom:
            st.error("Le nom est obligatoire !")
        else:
            existant = supabase.table("categories").select("id").eq("nom", nom).eq("boutique_id", boutique_id).execute().data
            if existant:
                st.error("Cette catégorie existe déjà !")
            else:
                supabase.table("categories").insert({
                    "nom": nom,
                    "boutique_id": boutique_id
                }).execute()
                st.success(f"Catégorie **{nom}** ajoutée ! ✅")
                st.rerun()
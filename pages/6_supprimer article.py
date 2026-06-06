import streamlit as st
from database import supabase

if "boutique" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

boutique_id = st.session_state.boutique["id"]

st.title("🗑️ Supprimer un article")

# Récupérer les articles
articles = supabase.table("articles").select("*").eq("boutique_id", boutique_id).execute().data

if not articles:
    st.info("Aucun article enregistré.")
    st.stop()

# Sélectionner un article
articles_dict = {a["nom"]: a for a in articles}
choix = st.selectbox("Choisir un article à supprimer", list(articles_dict.keys()))
article = articles_dict[choix]

# Afficher les infos
st.write(f"**Nom :** {article['nom']}")
st.write(f"**Prix :** {article['prix']} FCFA")
st.write(f"**Quantité :** {article['quantite']}")
st.write(f"**Description :** {article['description'] or '—'}")

st.divider()

# Confirmation suppression
if "confirmer_suppression" not in st.session_state:
    st.session_state.confirmer_suppression = False

if st.button("🗑️ Supprimer cet article"):
    st.session_state.confirmer_suppression = True

if st.session_state.confirmer_suppression:
    st.warning(f"Es-tu sûr de vouloir supprimer **{article['nom']}** ?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Oui, supprimer"):
            supabase.table("articles").delete().eq("id", article["id"]).execute()
            st.session_state.confirmer_suppression = False
            st.success("Article supprimé ! ✅")
            st.rerun()

    with col2:
        if st.button("❌ Annuler"):
            st.session_state.confirmer_suppression = False
            st.rerun()
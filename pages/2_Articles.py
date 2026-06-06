import streamlit as st
from database import supabase

if "boutique" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

boutique_id = st.session_state.boutique["id"]

st.title("📦 Articles")

# Récupérer les données
articles = supabase.table("articles").select("*").eq("boutique_id", boutique_id).execute().data
categories = supabase.table("categories").select("*").eq("boutique_id", boutique_id).execute().data
categories_dict = {c["id"]: c["nom"] for c in categories}

# Filtre par catégorie
options = ["Toutes"] + [c["nom"] for c in categories]
filtre = st.selectbox("Filtrer par catégorie", options)

if filtre != "Toutes":
    cat_id = next(c["id"] for c in categories if c["nom"] == filtre)
    articles = [a for a in articles if a["categorie_id"] == cat_id]

# Afficher les articles
if articles:
    for a in articles:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(f"**{a['nom']}**")
        col1.caption(a["description"] or "")
        col2.write(f"💰 {a['prix']} FCFA")
        
        # Couleur selon quantité
        if a["quantite"] == 0:
            col3.error(f"Stock : {a['quantite']}")
        elif a["quantite"] <= 5:
            col3.warning(f"Stock : {a['quantite']}")
        else:
            col3.success(f"Stock : {a['quantite']}")
        
        col4.write(categories_dict.get(a["categorie_id"], "—"))
        st.divider()
else:
    st.info("Aucun article trouvé.")
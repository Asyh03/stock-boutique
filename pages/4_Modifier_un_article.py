import streamlit as st
from database import supabase

if "boutique" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

boutique_id = st.session_state.boutique["id"]

st.title("✏️ Modifier un article")

# Récupérer les données
articles = supabase.table("articles").select("*").eq("boutique_id", boutique_id).execute().data
categories = supabase.table("categories").select("*").eq("boutique_id", boutique_id).execute().data
categories_dict = {c["nom"]: c["id"] for c in categories}
categories_id_nom = {c["id"]: c["nom"] for c in categories}

if not articles:
    st.info("Aucun article enregistré.")
    st.stop()

# Sélectionner un article
articles_dict = {a["nom"]: a for a in articles}
choix = st.selectbox("Choisir un article", list(articles_dict.keys()))
article = articles_dict[choix]

st.divider()

# Onglets
onglet1, onglet2 = st.tabs(["Modifier les infos", "Mettre à jour le stock"])

# ── MODIFIER LES INFOS ──
with onglet1:
    with st.form("modifier_article"):
        nom = st.text_input("Nom *", value=article["nom"])
        description = st.text_area("Description", value=article["description"] or "")
        prix = st.number_input("Prix (FCFA)", min_value=0, value=int(article["prix"] or 0))
        
        cat_actuelle = categories_id_nom.get(article["categorie_id"], list(categories_dict.keys())[0])
        categorie = st.selectbox("Catégorie", list(categories_dict.keys()),
                                  index=list(categories_dict.keys()).index(cat_actuelle))
        
        soumettre = st.form_submit_button("Mettre à jour")

        if soumettre:
            supabase.table("articles").update({
                "nom": nom,
                "description": description,
                "prix": prix,
                "categorie_id": categories_dict[categorie]
            }).eq("id", article["id"]).execute()
            st.success("Article mis à jour ! ✅")
            st.rerun()

# ── METTRE À JOUR LE STOCK ──
with onglet2:
    st.write(f"Stock actuel : **{article['quantite']}**")
    
    with st.form("update_stock"):
        action = st.radio("Action", ["Vente (réduire le stock)", "Réapprovisionnement (augmenter le stock)"])
        quantite = st.number_input("Quantité", min_value=1)
        soumettre = st.form_submit_button("Mettre à jour le stock")

        if soumettre:
            if "Vente" in action:
                nouvelle_quantite = article["quantite"] - quantite
                if nouvelle_quantite < 0:
                    st.error("Stock insuffisant !")
                else:
                    supabase.table("articles").update({"quantite": nouvelle_quantite}).eq("id", article["id"]).execute()
                    st.success(f"Stock mis à jour : {nouvelle_quantite} restants ✅")
                    st.rerun()
            else:
                nouvelle_quantite = article["quantite"] + quantite
                supabase.table("articles").update({"quantite": nouvelle_quantite}).eq("id", article["id"]).execute()
                st.success(f"Stock mis à jour : {nouvelle_quantite} en stock ✅")
                st.rerun()
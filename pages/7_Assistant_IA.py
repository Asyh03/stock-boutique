import streamlit as st
from agent import poser_question

if "boutique" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

boutique_id = st.session_state.boutique["id"]
boutique_nom = st.session_state.boutique["nom"]

st.title("🤖 Assistant IA")
st.caption(f"Assistant de {boutique_nom}")

# Initialiser l'historique
if "historique" not in st.session_state:
    st.session_state.historique = []

# Afficher l'historique
for message in st.session_state.historique:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# Champ de saisie
question = st.chat_input("Ex: Quels articles sont épuisés ? Quelle est la valeur de mon stock ?...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            reponse = poser_question(question, st.session_state.historique, boutique_id)
            st.write(reponse)

    st.session_state.historique.append({"role": "user", "content": question})
    st.session_state.historique.append({"role": "assistant", "content": reponse})
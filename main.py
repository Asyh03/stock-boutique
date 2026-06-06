import streamlit as st

if "boutique" not in st.session_state :
    st.switch_page("pages/0_Connexion.py")

st.set_page_config(
    page_title= "Gestion de Stock",
    page_icon="🏪",
    layout="wide"
)

boutique = st.session_state.boutique

st.title(f" {boutique['nom']}")
st.write("Bienvenue sur votre espace de geston de stock .")

if st.sidebar.button("🚪Se déconnecter") :
    del st.session_state.boutique
    st.switch_page("pages/0_Connexion.py")
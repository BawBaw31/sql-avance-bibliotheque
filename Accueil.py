import streamlit as st

from db.Database import Database

db = Database()

# initialiser membre
if 'membre' not in st.session_state:
    st.session_state.membre = None

st.set_page_config(
    layout="wide",
)

if st.session_state.membre != None:
    st.title("hello " + st.session_state.membre.nom + ", you are logged in!")

else:
    st.title("Bibliothèque")

    a, b = st.columns([1, 1])

    # Login
    a.subheader("Login")

    login_nom = a.text_input('nom')

    if a.button('Se connecter'):
        membre = db.login(login_nom)
        if membre:
            st.session_state.membre = membre
            st.success("Vous êtes connecté")
            st.experimental_rerun()
        else:
            st.error("La connexion a échoué")

    # Inscription
    b.subheader("Inscription")

    inscription_nom = b.text_input('nom (obligatoire)')
    inscription_date_de_naissance = b.date_input(
        'date de naissance (obligatoire)')

    if b.button('S\'inscrire'):
        try:
            db.creer_membre(inscription_nom, inscription_date_de_naissance)
            st.success("Vous êtes inscrit")
            st.info("Vous pouvez vous connecter")
        except:
            st.error("Erreur lors de l'inscription")
            st.info("Veuillez réessayer")

import streamlit as st

from Accueil import db
from db.entities.Categories import categories
from db.entities.Livres import Livres

# initialiser membre
if 'membre' not in st.session_state:
    st.session_state.membre = None

if not st.session_state.membre:
    st.warning(
        "Vous devez vous connecter pour voir le contenu de cette page sensible! Allez à la page d'Accueil.")
    st.stop()

elif not "admin" in st.session_state.membre.roles:
    st.warning(
        "Vous devez être admin pour voir le contenu de cette page sensible! Allez à la page d'Accueil.")
    st.stop()

else:
    st.subheader("Ajouter un livre")

    isbn = st.number_input('ISBN (obligatoire)', step=1)
    titre = st.text_input('titre (obligatoire)')
    quantite_disponible = st.number_input(
        'quantité disponible (obligatoire)', step=1)
    auteur = st.text_input('auteur (obligatoire)')
    edition = st.text_input('édition (obligatoire)')
    date_parution = st.date_input('date de parution (obligatoire)')
    nom_categorie = st.selectbox('catégorie (obligatoire)', categories)

    if st.button('Ajouter'):
        try:
            livre = Livres(isbn, titre, auteur, edition, date_parution,
                           nom_categorie, quantite_disponible)
            livre.ajouter_livres(db)
            st.success("Le livre a été ajouté")
            st.session_state.livres = []
        except (Exception) as e:
            print(e)
            st.error("Erreur lors de l'ajout du livre")
            st.info("Veuillez réessayer")

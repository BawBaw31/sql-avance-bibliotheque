import streamlit as st
from db.entities.Categories import Categories
from Accueil import db

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
    # Inscription
    st.subheader("Ajouter un livre")

    ISBN = st.text_input('ISBN (obligatoire)')
    quantite_disponible = st.number_input('quantité disponible (obligatoire)', step=1)
    auteur = st.text_input('auteur (obligatoire)')
    edition = st.text_input('édition (obligatoire)')
    date_parution = st.date_input('date de parution (obligatoire)')
    nom_categorie = st.selectbox('catégorie (obligatoire)', Categories)
    
    

    if st.button('S\'inscrire'):
        try:
            db.ajouter_livre(ISBN, quantite_disponible, auteur, edition, date_parution, nom_categorie)
            st.success("Le livre a été ajouté")
        except:
            st.error("Erreur lors de l'ajout du livre")
            st.info("Veuillez réessayer")

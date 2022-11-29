import streamlit as st

from Accueil import db
from db.entities.Categories import categories
from db.entities.Livres import Livres

# initialiser membre
if 'membre' not in st.session_state:
    st.session_state.membre = None

# initialiser livres
if 'livres' not in st.session_state:
    st.session_state.livres = []

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
            st.session_state.livres.append(Livres(isbn, titre, auteur, edition,
                                                  date_parution, nom_categorie, quantite_disponible))
            st.success("Le livre est ajouté et en attente de validation")
            print(st.session_state.livres)
        except (Exception) as e:
            print(e)
            st.error("Erreur lors de l'ajout du livre")
            st.info("Veuillez réessayer")

    if st.button('Valider'):
        print(st.session_state.livres)
        if not len(st.session_state.livres):
            st.error("Pas de livre à valdier")
            st.info("Vous devez ajouter vos livres avant de valdier")
        else:
            try:
                db.ajouter_livres(st.session_state.livres)
                st.success("Le(s) livre(s) a(ont) été ajouté(s)")
                st.session_state.livres = []
            except (Exception) as e:
                print(e)
                st.error("Erreur lors de l'ajout du(des) livre(s)")
                st.info("Veuillez réessayer")

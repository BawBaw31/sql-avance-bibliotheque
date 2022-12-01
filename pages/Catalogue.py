import pandas as pd
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

else:
    st.subheader("Catalogue de livres")
    a, b, c = st.columns([1, 1, 1])

    auteur = a.text_input('Auteur', '')
    catégorie = b.selectbox('Catégorie', [''] + categories)
    annee = c.number_input('Année', step=1)

    livres = Livres.afficher_livres(db, auteur, catégorie, annee)
    df = pd.DataFrame(
        livres,
        columns=('isbn', 'titre', 'quantite_disponible', 'auteur', 'edition', 'date_parution', 'nom_categorie'))
    st.table(df)

    st.subheader("Emprunter un livre")
    isbn = st.number_input('ISBN (obligatoire)', step=1)
    quantite = st.number_input('quantité', step=1, value=1)

    if st.button('Emprunter'):
        try:
            Livres.emprunter_livres(db, st.session_state.membre, isbn, quantite)
            st.success("Le livre a été emprunté")
        except (Exception) as e:
            print(e)
            st.error("Erreur lors de l'emprunt du livre")
            st.info("Veuillez réessayer")

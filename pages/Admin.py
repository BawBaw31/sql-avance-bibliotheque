import pandas as pd
import streamlit as st

from Accueil import db
from db.entities.Categories import categories
from db.entities.Emprunts import Emprunts
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
    tab, tab1 = st.tabs(["Ajouter un livre", "Rendre un livre"])

    isbn = tab.number_input('ISBN (obligatoire)', step=1)
    titre = tab.text_input('titre (obligatoire)')
    quantite_disponible = tab.number_input(
        'quantité disponible (obligatoire)', step=1)
    auteur = tab.text_input('auteur (obligatoire)')
    edition = tab.text_input('édition (obligatoire)')
    date_parution = tab.date_input('date de parution (obligatoire)')
    nom_categorie = tab.selectbox('catégorie (obligatoire)', categories)

    if tab.button('Ajouter'):
        try:
            livre = Livres(isbn, titre, auteur, edition, date_parution,
                           nom_categorie, quantite_disponible)
            livre.ajouter_livres(db)
            tab.success("Le livre a été ajouté")
            tab.session_state.livres = []
        except (Exception) as e:
            print(e)
            tab.error("Erreur lors de l'ajout du livre")
            tab.info("Veuillez réessayer")

    emprunts = Emprunts.emprunts_encours(db)
    df = pd.DataFrame(
        emprunts,
        columns=('id', 'isbn', 'date_emprunt', 'date_rendu', 'quantite'))
    tab1.table(df)
    
    
    id = tab1.number_input('id (obligatoire)', step=1)
    if tab1.button('Rendre'):
        try:
            Emprunts.rendre_livre(id, db)
            tab1.success("Le livre a été rendu")
        except (Exception) as e:
            print(e)
            tab1.error("Erreur lors du rendu du livre")
            tab1.info("Veuillez réessayer")

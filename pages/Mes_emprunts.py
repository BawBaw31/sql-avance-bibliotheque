import streamlit as st
import pandas as pd

from Accueil import db
from db.entities.Emprunts import Emprunts

# initialiser membre
if 'membre' not in st.session_state:
    st.session_state.membre = None

if not st.session_state.membre:
    st.warning(
        "Vous devez vous connecter pour voir le contenu de cette page sensible! Allez à la page d'Accueil.")
    st.stop()

else:
    st.subheader("Mes emprunts")
    tab1, tab2 = st.tabs(["Emprunts en cours", "Historique"])

    emprunts = Emprunts.mes_emprunts(st.session_state.membre, db)
    df = pd.DataFrame(
        emprunts,
        columns=('id', 'isbn', 'date_emprunt', 'quantite'))
    tab1.table(df)

    historique = Emprunts.mon_historique(st.session_state.membre, db)
    df = pd.DataFrame(
        historique,
        columns=('id', 'isbn', 'date_emprunt', 'date_rendu', 'quantite'))
    tab2.table(df)

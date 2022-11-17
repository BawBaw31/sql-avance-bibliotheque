import streamlit as st

from db.Database import Database

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1.5, 4.5])

a.title("Bibliothèque")
import streamlit as st 
import pandas as pd


st.title("Inscription à Safe_Home")
nom = st.text_input("Nom :")

prenom = st.text_input("Prénom :")

heure = st.time_input("Sélectionnez une heure de rentré:")

rentre_en_voiture = st.radio("Je vais rentrer en voiture :", ["Oui", "Non"])

nombre_de_place = st.number_input("Nombre de place dans ma voiture :", min_value=0, max_value=6, value=0)

st.write("Je veux rentrer avec :")
choix_ma_voiture = st.checkbox("ma voiture")
choix_metro = st.checkbox("un metro")
choix_a_pied = st.checkbox("mes pieds")
choix_velo = st.checkbox("mon velo")
choix_fous = st.checkbox("m'en fous tant que je rentre")


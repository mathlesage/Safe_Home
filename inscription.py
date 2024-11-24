import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Inscription à Safe_Home")

# Champs de saisie
nom = st.text_input("Nom :")
prenom = st.text_input("Prénom :")
addresse = st.text_input("Adresse :")
heure = st.time_input("Sélectionnez une heure de rentrée :")
rentre_en_voiture = st.radio("Je vais rentrer en voiture :", ["Non", "Oui"])
nombre_de_place = st.number_input("Nombre de place dans ma voiture :", min_value=0, max_value=6, value=0)

# Options de transport
st.write("Je veux rentrer avec :")
choix_ma_voiture = st.checkbox("ma voiture")
choix_metro = st.checkbox("un métro")
choix_a_pied = st.checkbox("mes pieds")
choix_velo = st.checkbox("mon vélo")
choix_fous = st.checkbox("m'en fous tant que je rentre")

# Bouton pour sauvegarder les informations
if st.button("Enregistrer mes informations"):
    # Vérification que tous les champs obligatoires sont remplis
    if nom and prenom and addresse:
        # Création d'un dictionnaire avec les informations
        data = {
            "Nom": nom,
            "Prénom": prenom,
            "Adresse": addresse,
            "Heure de rentrée": str(heure),
            "Rentre en voiture": rentre_en_voiture,
            "Nombre de places": nombre_de_place,
            "Avec ma voiture": choix_ma_voiture,
            "Avec un métro": choix_metro,
            "À pied": choix_a_pied,
            "À vélo": choix_velo,
            "Peu importe": choix_fous,
        }
        
        # Chargement ou création du fichier CSV avec sep=";"
        try:
            df = pd.read_csv("inscriptions.csv", sep=";", encoding="utf-8")
        except FileNotFoundError:
            df = pd.DataFrame(columns=data.keys())
        
        # Ajout de la nouvelle ligne
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        
        # Sauvegarde des données dans le fichier CSV
        df.to_csv("inscriptions.csv", sep=";", index=False, encoding="utf-8")
        
        st.success("Informations enregistrées avec succès !")
    else:
        st.error("Veuillez remplir tous les champs obligatoires (Nom, Prénom, et Adresse).")

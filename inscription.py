import streamlit as st
import pandas as pd
import requests
import base64
import io
# Informations de GitHub
GITHUB_TOKEN = "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"  # Remplacez par votre token GitHub
GITHUB_REPO = "mathlesage/Safe_Home"  # Remplacez par le chemin de votre dépôt
CSV_PATH = "inscriptions.csv"  # Chemin vers le fichier CSV dans le dépôt


def get_csv_from_github():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        csv_content = base64.b64decode(content["content"]).decode("utf-8")
        sha = content["sha"]
        # Correction ici avec io.StringIO
        return pd.read_csv(io.StringIO(csv_content), sep=";"), sha
    elif response.status_code == 404:
        # Si le fichier n'existe pas encore
        return pd.DataFrame(), None
    else:
        st.error("Erreur lors de l'accès au fichier CSV sur GitHub.")
        st.stop()


# Fonction pour mettre à jour le fichier CSV sur GitHub
def update_csv_on_github(df, sha=None):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    csv_content = df.to_csv(sep=";", index=False, encoding="utf-8")
    data = {
        "message": "Mise à jour du fichier inscriptions.csv",
        "content": base64.b64encode(csv_content.encode("utf-8")).decode("utf-8"),
        "branch": "main",  # Remplacez par la branche de votre dépôt
    }
    if sha:
        data["sha"] = sha  # Ajoute le SHA du fichier existant pour le mettre à jour
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        st.success("Informations enregistrées avec succès sur GitHub !")
    else:
        st.error("Erreur lors de la mise à jour du fichier CSV sur GitHub.")
        st.stop()

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
        # Récupération du fichier CSV existant depuis GitHub
        df, sha = get_csv_from_github()

        # Création d'un dictionnaire avec les informations
        new_data = {
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

        # Ajout de la nouvelle ligne
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        # Mise à jour du fichier CSV sur GitHub
        update_csv_on_github(df, sha)
    else:
        st.error("Veuillez remplir tous les champs obligatoires (Nom, Prénom, et Adresse).")

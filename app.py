import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API de Google depuis les variables d'environnement
api_key = os.getenv("GOOGLE_API_KEY")

# Configurer l'API Google generative AI avec la clé API
genai.configure(api_key=api_key)

# Définir le prompt pour le modèle de génération de contenu
prompt = """Tu es un spécialiste en résumé de vidéos YouTube. 
Tu vas prendre le texte de la transcription et résumer l'ensemble 
de la vidéo, en fournissant les points importants en 250 mots. 
ATTENTION, le résumé doit être en français. 
Donne moi le résumé du texte donné ici : """

# Fonction pour obtenir l'ID de la vidéo à partir de l'URL YouTube
def get_video_id(youtube_url):
    try:
        # Extraire l'ID de la vidéo de l'URL
        video_id = youtube_url.split("=")[1]
        return video_id
    except IndexError:
        # Gérer les erreurs d'URL invalide
        raise ValueError("URL YouTube invalide.")

# Fonction pour extraire la transcription de la vidéo à partir de l'ID de la vidéo
def extract_transcript(video_id):
    try:
        # Utiliser l'API YouTube Transcript pour obtenir la transcription
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Convertir la transcription en texte
        transcript_text = " ".join([item['text'] for item in transcript_list])
        return transcript_text
    except Exception as e:
        # Gérer les erreurs d'extraction de la transcription
        raise RuntimeError(f"Erreur lors de l'extraction de la transcription : {e}")

# Fonction pour extraire les détails de la transcription à partir de l'URL YouTube
def extract_transcript_details(youtube_video_url):
    try:
        # Obtenir l'ID de la vidéo
        video_id = get_video_id(youtube_video_url)
        # Extraire la transcription
        transcript_text = extract_transcript(video_id)
        return transcript_text
    except ValueError as ve:
        # Afficher une erreur pour une URL invalide
        st.error(f"Erreur d'URL : {ve}")
    except RuntimeError as re:
        # Afficher une erreur pour une erreur d'extraction
        st.error(f"Erreur de transcription : {re}")
    except Exception as e:
        # Afficher une erreur pour toute autre erreur
        st.error(f"Erreur inattendue : {e}")

# Fonction pour générer le contenu résumé avec Google Gemini
def generate_gemini_content(transcript_text, prompt):
    # Combiner le prompt et la transcription
    full_prompt = prompt + transcript_text
    # Utiliser le modèle pour générer le contenu
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(full_prompt)
    return response.text

# Interface utilisateur avec Streamlit
st.title("Convertisseur de transcription YouTube en notes détaillées")

# Champ de saisie pour l'URL de la vidéo YouTube
youtube_link = st.text_input("Entrez le lien de la vidéo YouTube :")

if youtube_link:
    # Obtenir l'ID de la vidéo et afficher l'image miniature
    video_id = get_video_id(youtube_link)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Obtenir les notes détaillées"):
    try:
        # Extraire la transcription de la vidéo
        transcript_text = extract_transcript_details(youtube_link)

        if transcript_text:
            # Générer les notes détaillées avec Google Gemini
            summary = generate_gemini_content(transcript_text, prompt)

            # Afficher les notes détaillées
            st.markdown("## Notes détaillées :")
            st.write(summary)
    except Exception as e:
        # Afficher une erreur en cas de problème
        st.error(f"Erreur : {e}")

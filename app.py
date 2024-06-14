import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API Google generative AI
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Définition du prompt pour le modèle de génération de contenu
prompt = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important points in 250 words.
Please provide the summary of the text given here: """

# Fonctions auxiliaires
def get_video_id(youtube_url):
    try:
        video_id = youtube_url.split("=")[1]
        return video_id
    except IndexError:
        raise ValueError("URL YouTube invalide.")

def extract_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript_list])
        return transcript_text
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'extraction de la transcription : {e}")

def extract_transcript_details(youtube_video_url):
    try:
        # Récupération de l'ID de la vidéo
        video_id = get_video_id(youtube_video_url)
        
        # Extraction de la transcription
        transcript_text = extract_transcript(video_id)
        
        return transcript_text
    
    except ValueError as ve:
        st.error(f"Erreur d'URL : {ve}")
    except RuntimeError as re:
        st.error(f"Erreur de transcription : {re}")
    except Exception as e:
        st.error(f"Erreur inattendue : {e}")

def generate_gemini_content(transcript_text, prompt):
    # Combinaison du prompt et de la transcription
    full_prompt = prompt + transcript_text
    
    # Utilisation du modèle pour générer le contenu
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(full_prompt)
    
    return response.text

# Interface utilisateur avec Streamlit
st.title("Convertisseur de transcription YouTube en notes détaillées")

# Champ de saisie pour l'URL de la vidéo YouTube
youtube_link = st.text_input("Entrez le lien de la vidéo YouTube :")

if youtube_link:
    video_id = get_video_id(youtube_link)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Obtenir les notes détaillées"):
    try:
        # Extraction de la transcription
        transcript_text = extract_transcript_details(youtube_link)

        if transcript_text:
            # Génération des notes détaillées avec Google Gemini
            summary = generate_gemini_content(transcript_text, prompt)

            # Affichage des notes détaillées
            st.markdown("## Notes détaillées :")
            st.write(summary)
    except Exception as e:
        st.error(f"Erreur : {e}")

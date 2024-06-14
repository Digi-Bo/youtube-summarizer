

## 1 - Présentation du projet

**Nom du projet :** Transcripteur de vidéos YouTube

**Objectif :** Extraire automatiquement le texte des vidéos YouTube

Le projet "Transcripteur de vidéos YouTube" vise à simplifier le processus d'extraction de texte à partir de vidéos YouTube. En fournissant simplement le lien d'une vidéo, l'application sera capable de récupérer automatiquement la transcription complète. Cette fonctionnalité est particulièrement utile pour les créateurs de contenu, les chercheurs et toute personne souhaitant analyser le contenu des vidéos de manière textuelle. 

Dans cette documentation, nous allons détailler chaque étape du développement de ce projet, des configurations initiales à l'implémentation des fonctionnalités clés, en passant par l'intégration d'interfaces utilisateur conviviales.



## 2 - Configuration initiale

### Création de l'environnement

* **Utilisation de Conda pour créer un nouvel environnement avec Python 3.12 :**
  Pour commencer, nous allons utiliser Conda pour créer un environnement isolé afin d'assurer que toutes les dépendances sont gérées de manière propre. Cela peut être fait avec la commande suivante :

```
conda create -p venv python==3.12 -y
```
le ```-p``` signifie que l'environnement est personnalisé et est associé au dossier de travail


### Activer l'environement
  
Comme l'environement est stocké dans le dossier, il faut l'indiquer quand on active l'environnement
```
conda activate /Users/fanchdaniel/mes_documents/dev/gen-ai-gemini/youtube-summarizer/venv
```





* **Création des fichiers nécessaires : .env, requirements.txt, app.py :**
  Une fois l'environnement créé, nous allons créer les fichiers nécessaires pour le projet :
  - `.env` : Contiendra les variables d'environnement, notamment la clé API de Google.
  - `requirements.txt` : Liste des bibliothèques Python nécessaires.
  - `app.py` : Le script principal de l'application.

**Installation des bibliothèques**

* **Installation des bibliothèques via pip :**
  Nous allons installer les bibliothèques nécessaires en utilisant pip. Les bibliothèques à installer incluent :
  - `YouTube transcript API` : Pour extraire les transcriptions des vidéos YouTube.
  - `Streamlit` : Pour créer l'interface utilisateur.
  - `Google generative AI` : Pour utiliser les capacités de génération de contenu de Google Gemini.
  - `python-dotenv` : Pour charger les variables d'environnement.
  - `pathlib` : Pour manipuler les chemins de fichiers de manière portable.


* **Installation des bibliothèques dans le fichier `requirements.txt` pour les installer en une seule commande :**
  
```txt
youtube-transcript-api
streamlit
google-generativeai
python-dotenv
pathlib
```
Puis exécuter :
```bash
pip install -r requirements.txt
```





## 3 - Configuration des variables d'environnement

**Définition de la clé API Google dans le fichier `.env`**

Pour sécuriser et gérer facilement les clés API et autres variables sensibles, nous utilisons un fichier `.env`. Ce fichier contient les variables d'environnement nécessaires au bon fonctionnement de l'application. Voici comment définir la clé API Google dans ce fichier :

1. Créez un fichier nommé `.env` à la racine de votre projet.
2. Ajoutez la clé API Google dans ce fichier sous la forme suivante :
   ```env
   GOOGLE_API_KEY=VotreCléAPIGoogleIci
   ```

**Chargement des variables d'environnement dans le code**

Pour utiliser les variables définies dans le fichier `.env` au sein de notre application, nous utilisons la bibliothèque `python-dotenv`. Voici comment charger ces variables dans le script principal `app.py` :

1. Importez la bibliothèque `dotenv` et chargez les variables d'environnement au début de votre script :
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # Charge toutes les variables d'environnement à partir du fichier .env
   ```

2. Accédez à la clé API Google dans votre code en utilisant `os.getenv` :
   ```python
   api_key = os.getenv("GOOGLE_API_KEY")
   ```

3. Configurez l'API Google generative AI avec cette clé :
   ```python
   import google.generativeai as genai

   genai.configure(api_key=api_key)
   ```



## 4 - Extraction de la transcription YouTube

**Utilisation de YouTube transcript API**

* **Récupération de l'ID de la vidéo à partir de l'URL YouTube :**
  La première étape pour extraire la transcription d'une vidéo YouTube est de récupérer l'ID de la vidéo à partir de l'URL fournie. Voici un exemple de code pour accomplir cela :
  ```python
  def get_video_id(youtube_url):
      try:
          video_id = youtube_url.split("=")[1]
          return video_id
      except IndexError:
          raise ValueError("URL YouTube invalide.")
  ```

* **Extraction de la transcription sous forme de texte :**
  Une fois l'ID de la vidéo obtenu, nous utilisons `YouTubeTranscriptApi` pour extraire la transcription de la vidéo. Voici comment procéder :
  ```python
  from youtube_transcript_api import YouTubeTranscriptApi

  def extract_transcript(video_id):
      try:
          transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
          transcript_text = " ".join([item['text'] for item in transcript_list])
          return transcript_text
      except Exception as e:
          raise RuntimeError(f"Erreur lors de l'extraction de la transcription : {e}")
  ```

**Gestion des exceptions pour les vidéos privées ou non accessibles**

Pour gérer les erreurs potentielles, telles que les vidéos privées ou non accessibles, nous ajoutons des blocs try-except pour capturer et gérer ces exceptions de manière appropriée. Voici un exemple complet de la fonction avec gestion des exceptions :

```python
def extract_transcript_details(youtube_video_url):
    try:
        # Récupération de l'ID de la vidéo
        video_id = get_video_id(youtube_video_url)
        
        # Extraction de la transcription
        transcript_text = extract_transcript(video_id)
        
        return transcript_text
    
    except ValueError as ve:
        print(f"Erreur d'URL : {ve}")
    except RuntimeError as re:
        print(f"Erreur de transcription : {re}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
```



## 5 - Implémentation de la génération de contenu avec Google Gemini

**Configuration de l'API Google generative AI**

Avant de pouvoir utiliser l'API Google generative AI, nous devons la configurer en utilisant la clé API chargée à partir du fichier `.env`. Voici comment procéder :

```python
import google.generativeai as genai

# Configuration de l'API avec la clé API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
```

**Création de la fonction pour générer le contenu**

* **Définition du prompt pour le modèle de génération de contenu :**
  Nous devons définir un prompt clair et précis pour le modèle afin d'obtenir un résumé efficace de la transcription de la vidéo YouTube. Voici un exemple de prompt :

  ```python
  prompt = """You are a YouTube video summarizer. You will take the transcript text
  and summarize the entire video, providing the important points in 250 words. 
  Please provide the summary of the text given here: """
  ```

* **Intégration de la transcription dans le prompt :**
  La transcription extraite doit être intégrée dans le prompt pour permettre au modèle de générer le résumé. Voici comment structurer la fonction :

  ```python
  def generate_gemini_content(transcript_text, prompt):
      # Combinaison du prompt et de la transcription
      full_prompt = prompt + transcript_text
      
      # Utilisation du modèle pour générer le contenu
      model = genai.GenerativeModel("gemini-pro")
      response = model.generate_content(full_prompt)
      
      return response.text
  ```

* **Récupération et affichage de la réponse du modèle :**
  Une fois le contenu généré, nous devons récupérer la réponse et l'afficher. Voici un exemple d'intégration complète dans l'application Streamlit :

  ```python
  import streamlit as st
  from dotenv import load_dotenv
  import os

  load_dotenv()  # Charger les variables d'environnement

  # Titre de l'application Streamlit
  st.title("YouTube Transcript to Detailed Notes Converter")

  # Saisie de l'URL de la vidéo YouTube
  youtube_link = st.text_input("Enter YouTube Video Link:")

  if youtube_link:
      video_id = get_video_id(youtube_link)
      st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

  if st.button("Get Detailed Notes"):
      try:
          # Extraction de la transcription
          transcript_text = extract_transcript_details(youtube_link)

          # Génération du contenu avec Google Gemini
          summary = generate_gemini_content(transcript_text, prompt)

          # Affichage du résumé
          st.markdown("## Detailed Notes:")
          st.write(summary)
      except Exception as e:
          st.error(f"Erreur : {e}")
  ```


## 6 - Interface utilisateur avec Streamlit

**Création d'une interface Streamlit**

* **Titre et champ de saisie pour l'URL de la vidéo YouTube :**
  La première étape consiste à créer une interface simple et intuitive où l'utilisateur peut entrer l'URL de la vidéo YouTube. Voici un exemple de code pour configurer cela dans Streamlit :

  ```python
  import streamlit as st

  # Titre de l'application
  st.title("Convertisseur de transcription YouTube en notes détaillées")

  # Champ de saisie pour l'URL de la vidéo YouTube
  youtube_link = st.text_input("Entrez le lien de la vidéo YouTube :")
  ```

* **Affichage de l'image miniature de la vidéo :**
  Après avoir saisi l'URL de la vidéo, nous pouvons afficher l'image miniature de la vidéo pour confirmation visuelle :

  ```python
  if youtube_link:
      video_id = get_video_id(youtube_link)
      st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
  ```

**Bouton pour obtenir les notes détaillées**

* **Extraction de la transcription lors du clic sur le bouton :**
  Nous ajoutons un bouton qui, lorsqu'il est cliqué, déclenche l'extraction de la transcription de la vidéo YouTube :

  ```python
  if st.button("Obtenir les notes détaillées"):
      try:
          # Extraction de la transcription
          transcript_text = extract_transcript_details(youtube_link)

          # Génération des notes détaillées avec Google Gemini
          summary = generate_gemini_content(transcript_text, prompt)

          # Affichage des notes détaillées
          st.markdown("## Notes détaillées :")
          st.write(summary)
      except Exception as e:
          st.error(f"Erreur : {e}")
  ```

Cette interface utilisateur Streamlit permet aux utilisateurs de saisir l'URL d'une vidéo YouTube, de voir l'image miniature de la vidéo et d'obtenir un résumé détaillé de la transcription de la vidéo en quelques clics seulement. Le code complet pour l'interface utilisateur avec Streamlit est le suivant :

```python
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
```



### Conclusion : Résumé des fonctionnalités développées

Le projet "Transcripteur de vidéos YouTube" offre une solution complète pour l'extraction automatique et la génération de résumés de transcriptions de vidéos YouTube. Voici un résumé des fonctionnalités développées :

* **Création de l'environnement :**
  - Utilisation de Conda pour créer un environnement isolé avec Python 3.12
  - Création des fichiers nécessaires (.env, requirements.txt, app.py) pour organiser le projet.

* **Configuration des variables d'environnement :**
  - Définition de la clé API Google dans le fichier `.env` pour sécuriser les informations sensibles.
  - Chargement des variables d'environnement dans le code à l'aide de `python-dotenv`.

* **Extraction de la transcription YouTube :**
  - Utilisation de `YouTube transcript API` pour récupérer l'ID de la vidéo à partir de l'URL YouTube.
  - Extraction de la transcription sous forme de texte.
  - Gestion des exceptions pour les vidéos privées ou non accessibles, assurant une expérience utilisateur robuste.

* **Implémentation de la génération de contenu avec Google Gemini :**
  - Configuration de l'API Google generative AI.
  - Création d'une fonction pour générer du contenu, incluant la définition du prompt, l'intégration de la transcription, et la récupération de la réponse du modèle.

* **Interface utilisateur avec Streamlit :**
  - Création d'une interface intuitive avec un titre et un champ de saisie pour l'URL de la vidéo YouTube.
  - Affichage de l'image miniature de la vidéo pour confirmation visuelle.
  - Bouton pour obtenir les notes détaillées, déclenchant l'extraction de la transcription, la génération de contenu, et l'affichage des notes détaillées dans l'application Streamlit.

Ces fonctionnalités permettent aux utilisateurs de transformer efficacement les vidéos YouTube en notes détaillées et résumées, facilitant ainsi l'analyse et la compréhension du contenu vidéo. Le projet combine des techniques avancées d'extraction de données et de génération de contenu, offrant une solution puissante et conviviale.





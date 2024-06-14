

## 1 - Présentation du projet

**Nom du projet :** Transcripteur de vidéos YouTube avec traduction en français

**Objectif :** Extraire automatiquement le texte des vidéos YouTube

Le projet "Transcripteur de vidéos YouTube" vise à simplifier le processus d'extraction de texte à partir de vidéos YouTube. En fournissant simplement le lien d'une vidéo, l'application sera capable de récupérer automatiquement la transcription complète. Cette fonctionnalité est particulièrement utile pour les créateurs de contenu, les chercheurs et toute personne souhaitant analyser le contenu des vidéos de manière textuelle. 

Dans cette documentation, nous allons détailler chaque étape du développement de ce projet, des configurations initiales à l'implémentation des fonctionnalités clés, en passant par l'intégration d'interfaces utilisateur conviviales.


**Pour démarrer l'application en local :**

```
streamlit run app.py
```

**Fermer l'app streamlit :**
```
ctrl + c
```


### Résumé des fonctionnalités développées

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
conda activate /Users/chemin_d_acces_vers_le_dossier/youtube-summarizer/venv
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
  prompt =  """Tu es un spécialiste en résumé de vidéos YouTube.  Tu vas prendre le texte de la transcription et résumer l'ensemble de la vidéo, en fournissant les points importants en 250 mots. Donne moi le résumé du texte donné ici : """
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
  st.title("Convertisseur de transcription YouTube en notes détaillées")

  # Saisie de l'URL de la vidéo YouTube
  youtube_link = st.text_input("Entrez le lien de la vidéo YouTube :")

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

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API de Google depuis les variables d'environnement
api_key = os.getenv("GOOGLE_API_KEY")

# Configurer l'API Google generative AI avec la clé API
genai.configure(api_key=api_key)

# Définir le prompt pour le modèle de génération de contenu
prompt = """Tu es un spécialiste en résumé de vidéos YouTube. Tu vas prendre le texte de la transcription et résumer l'ensemble de la vidéo, en fournissant les points importants en 250 mots. Donne moi le résumé du texte donné ici : """

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
```

### Explications étape par étape

1. **Importer les bibliothèques nécessaires :**
   - `streamlit` pour l'interface utilisateur.
   - `dotenv` pour charger les variables d'environnement.
   - `os` pour accéder aux variables d'environnement.
   - `google.generativeai` pour utiliser l'API Google generative AI.
   - `youtube_transcript_api` pour extraire les transcriptions des vidéos YouTube.

2. **Charger les variables d'environnement :**
   - Utilisez `load_dotenv()` pour charger les variables d'environnement depuis le fichier `.env`.

3. **Configurer l'API Google generative AI :**
   - Récupérez la clé API de Google depuis les variables d'environnement.
   - Configurez l'API avec la clé récupérée.

4. **Définir le prompt :**
   - Définissez un prompt qui sera utilisé pour générer le contenu résumé à partir de la transcription.

5. **Fonction `get_video_id` :**
   - Extrait l'ID de la vidéo de l'URL YouTube.
   - Gère les erreurs d'URL invalide.

6. **Fonction `extract_transcript` :**
   - Utilise l'API YouTube Transcript pour obtenir la transcription de la vidéo.
   - Convertit la transcription en un texte continu.
   - Gère les erreurs d'extraction.

7. **Fonction `extract_transcript_details` :**
   - Combine les fonctions précédentes pour extraire les détails de la transcription à partir de l'URL YouTube.
   - Gère différentes erreurs et affiche des messages appropriés.

8. **Fonction `generate_gemini_content` :**
   - Combine le prompt et la transcription.
   - Utilise le modèle Google generative AI pour générer un résumé du contenu.

9. **Interface utilisateur avec Streamlit :**
   - Affiche un titre et un champ de saisie pour l'URL de la vidéo YouTube.
   - Affiche l'image miniature de la vidéo.
   - Génère et affiche les notes détaillées lors du clic sur le bouton.




















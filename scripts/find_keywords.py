import requests
from bs4 import BeautifulSoup
import re

# Définir les mots-clés à rechercher
keywords = [
    "entreprise familiale", "histoire", "fondé", "créé", "anniversaire",
    "génération", "héritage", "tradition", "valeurs familiales", "passation"
]

# Fonction pour analyser une page web
def analyze_page(url):
    found_keywords = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire le contenu texte des balises HTML
            texts = soup.get_text(separator=' ')
            
            # Rechercher les mots-clés dans le texte
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', texts, re.IGNORECASE):
                    found_keywords.append(keyword)
    
    except Exception as e:
        print(f"Failed to analyze {url}: {str(e)}")
    
    return found_keywords
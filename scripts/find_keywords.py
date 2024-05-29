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

# Fonction pour analyser des URLs à partir d'un fichier CSV
def analyze_urls_from_csv(file_stream):
    import csv
    import io

    results = {}
    stream = io.StringIO(file_stream.read().decode("UTF8"), newline=None)
    csv_reader = csv.reader(stream)
    
    urls = [row[0] for idx, row in enumerate(csv_reader) if idx != 0]  # Ignorer l'en-tête

    # Analyser chaque URL et stocker les résultats
    for url in urls:
        keywords_found = analyze_page(url)
        if keywords_found:
            results[url] = {"status": "oui", "keywords": keywords_found}
        else:
            results[url] = {"status": "non", "keywords": []}

    return results

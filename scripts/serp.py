from bs4 import BeautifulSoup
import requests
import json

def scrape_google(query):
    # Préparer l'URL de recherche
    query = query.replace(' ', '+')
    url = f'https://www.google.com/search?q={query}'
    
    # Définir les en-têtes pour la requête
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    # Envoyer la requête HTTP
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"HTTP Error {response.status_code}"}
    
    # Parse le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouver tous les résultats de recherche
    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else None
        link = g.find('a')['href'] if g.find('a') else None
        description = g.find('span', class_='aCOpRe').text if g.find('span', 'aCOpRe') else None
        if title and link:
            results.append({'title': title, 'link': link, 'description': description})
    
    return {"query": query, "results": results}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing query parameter"}))
        sys.exit(1)
    
    query = sys.argv[1]
    results = scrape_google(query)
    print(json.dumps(results))

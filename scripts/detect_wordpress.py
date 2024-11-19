import requests
from bs4 import BeautifulSoup

def is_wordpress_site(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        if meta_generator and 'wordpress' in meta_generator.get('content', '').lower():
            return True
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            if 'wp-includes' in script['src'] or 'wp-content' in script['src']:
                return True
        links = soup.find_all('link', href=True)
        for link in links:
            if 'wp-includes' in link['href'] or 'wp-content' in link['href']:
                return True
    except requests.RequestException:
        return False
    return False

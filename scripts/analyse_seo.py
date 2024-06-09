import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def seo_audit(url, content):
    soup = BeautifulSoup(content, 'html.parser')

    # Extraire le domaine de l'URL
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Vérifications des balises
    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')
    h3_tags = soup.find_all('h3')
    h4_tags = soup.find_all('h4')
    h5_tags = soup.find_all('h5')
    h6_tags = soup.find_all('h6')
    title_tag = soup.find('title')
    description_tag = soup.find('meta', attrs={'name': 'description'})
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    links = soup.find_all('a')
    internal_links = [link for link in links if link.get('href', '').startswith('/') or link.get('href', '').startswith(domain)]
    external_links = [link for link in links if link.get('href', '') and not link.get('href', '').startswith('/') and not link.get('href', '').startswith(domain)]
    images = soup.find_all('img')
    word_count = len(content.split())

    # Erreurs
    errors = {
        'erreur': [],
        'avertissement': [],
        'avis': []
    }

    if len(h1_tags) > 1:
        errors['erreur'].append('multiple_h1')
    if len(h1_tags) == 0:
        errors['erreur'].append('missing_h1')
    if len(h2_tags) > 0 and len(h1_tags) == 0:
        errors['erreur'].append('h2_without_h1')
    if word_count < 200:
        errors['erreur'].append('low_word_count')
    if title_tag is None:
        errors['erreur'].append('missing_title')
    if len(links) == 0:
        errors['erreur'].append('no_links')

    if len(h2_tags) == 0:
        errors['avertissement'].append('missing_h2')
    if len(h3_tags) > 0 and len(h2_tags) == 0:
        errors['avertissement'].append('h3_without_h2')
    if title_tag and len(title_tag.text) > 70:
        errors['avertissement'].append('title_too_long')
    if description_tag is None:
        errors['avertissement'].append('missing_description')
    if description_tag and len(description_tag.get('content', '')) > 160:
        errors['avertissement'].append('description_too_long')
    if canonical_tag is None:
        errors['avertissement'].append('missing_canonical')
    if len(internal_links) == 0:
        errors['avertissement'].append('no_internal_links')

    if len(h3_tags) == 0:
        errors['avis'].append('missing_h3')
    if len(h4_tags) > 0 and len(h3_tags) == 0:
        errors['avis'].append('h4_without_h3')
    if len(h5_tags) > 0 and len(h4_tags) == 0:
        errors['avis'].append('h5_without_h4')
    if len(h6_tags) > 0 and len(h5_tags) == 0:
        errors['avis'].append('h6_without_h5')
    if title_tag and len(title_tag.text) < 20:
        errors['avis'].append('title_too_short')
    if description_tag and len(description_tag.get('content', '')) < 50:
        errors['avis'].append('description_too_short')
    if len(url) > 70:
        errors['avis'].append('url_too_long')
    if canonical_tag and len(canonical_tag.get('href', '')) > 70:
        errors['avis'].append('canonical_too_long')
    if len(images) == 0:
        errors['avis'].append('no_images')
    if any(img.get('alt') is None for img in images):
        errors['avis'].append('missing_alt')
    if any(img.get('alt') == '' for img in images):
        errors['avis'].append('empty_alt')
    if len(external_links) == 0:
        errors['avis'].append('no_external_links')

    return errors

def analyze_and_report(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        errors = seo_audit(url, content)
        if not any(errors.values()):
            return {"errors": ["aucune erreur n'a été détectée"]}
        return {"errors": errors}
    except requests.RequestException as e:
        return {"errors": [f"Request error: {str(e)}"]}

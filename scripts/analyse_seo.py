import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def seo_audit(url, content):
    soup = BeautifulSoup(content, 'lxml')

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
    multiple_h1 = len(h1_tags) > 1
    missing_h1 = len(h1_tags) == 0
    h2_without_h1 = len(h2_tags) > 0 and len(h1_tags) == 0
    low_word_count = word_count < 200
    missing_title = title_tag is None
    no_links = len(links) == 0

    # Avertissements
    missing_h2 = len(h2_tags) == 0
    h3_without_h2 = len(h3_tags) > 0 and len(h2_tags) == 0
    title_too_long = title_tag and len(title_tag.text) > 70
    missing_description = description_tag is None
    description_too_long = description_tag and len(description_tag.get('content', '')) > 160
    missing_canonical = canonical_tag is None
    no_internal_links = len(internal_links) == 0

    # Avis
    missing_h3 = len(h3_tags) == 0
    h4_without_h3 = len(h4_tags) > 0 and len(h3_tags) == 0
    h5_without_h4 = len(h5_tags) > 0 and len(h4_tags) == 0
    h6_without_h5 = len(h6_tags) > 0 and len(h5_tags) == 0
    title_too_short = title_tag and len(title_tag.text) < 20
    description_too_short = description_tag and len(description_tag.get('content', '')) < 50
    url_too_long = len(url) > 70
    canonical_too_long = canonical_tag and len(canonical_tag.get('href', '')) > 70
    no_images = len(images) == 0
    missing_alt = any(img.get('alt') is None for img in images)
    empty_alt = any(img.get('alt') == '' for img in images)
    no_external_links = len(external_links) == 0

    errors = {
        'multiple_h1': multiple_h1,
        'missing_h1': missing_h1,
        'h2_without_h1': h2_without_h1,
        'low_word_count': low_word_count,
        'missing_title': missing_title,
        'no_links': no_links,
        'missing_h2': missing_h2,
        'h3_without_h2': h3_without_h2,
        'title_too_long': title_too_long,
        'missing_description': missing_description,
        'description_too_long': description_too_long,
        'missing_canonical': missing_canonical,
        'no_internal_links': no_internal_links,
        'missing_h3': missing_h3,
        'h4_without_h3': h4_without_h3,
        'h5_without_h4': h5_without_h4,
        'h6_without_h5': h6_without_h5,
        'title_too_short': title_too_short,
        'description_too_short': description_too_short,
        'url_too_long': url_too_long,
        'canonical_too_long': canonical_too_long,
        'no_images': no_images,
        'missing_alt': missing_alt,
        'empty_alt': empty_alt,
        'no_external_links': no_external_links
    }

    # Retourner uniquement les erreurs
    return {key: value for key, value in errors.items() if value}

def analyze_and_report(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        errors = seo_audit(url, content)
        if not errors:
            return {"errors": ["aucune erreur n'a été détectée"]}
        return {"errors": errors}
    except requests.RequestException as e:
        return {"errors": [f"Request error: {str(e)}"]}

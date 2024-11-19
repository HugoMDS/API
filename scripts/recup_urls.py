import requests
import re
import csv
from xml.etree import ElementTree as ET
from io import StringIO

def get_sitemaps_from_robots(robots_url):
    try:
        response = requests.get(robots_url, timeout=5)
        response.raise_for_status()
        sitemaps = re.findall(r'Sitemap\s*:\s*(https?://\S+)', response.text, re.IGNORECASE)
        return sitemaps
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération du fichier robots.txt: {e}")
        return []

def get_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url, timeout=5)
        response.raise_for_status()
        urls = []
        sitemaps = []
        tree = ET.fromstring(response.content)
        for elem in tree:
            if elem.tag.endswith('url'):
                for subelem in elem:
                    if subelem.tag.endswith('loc'):
                        urls.append(subelem.text)
            elif elem.tag.endswith('sitemap'):
                for subelem in elem:
                    if subelem.tag.endswith('loc'):
                        sitemaps.append(subelem.text)
        return urls, sitemaps
    except (requests.RequestException, ET.ParseError) as e:
        print(f"Erreur lors de la récupération ou de l'analyse du sitemap: {e}")
        return [], []

def fetch_all_urls(domain):
    robots_url = f"https://{domain}/robots.txt"
    sitemaps = get_sitemaps_from_robots(robots_url)
    if not sitemaps:
        sitemaps.append(f"https://{domain}/sitemap.xml")
    all_urls = set()
    while sitemaps:
        sitemap = sitemaps.pop()
        urls, nested_sitemaps = get_urls_from_sitemap(sitemap)
        all_urls.update(urls)
        sitemaps.extend(nested_sitemaps)
    return sorted(all_urls)

def generate_csv(urls):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['URL'])
    for url in urls:
        writer.writerow([url])
    return output.getvalue()

def recup_urls(domain):
    all_urls = fetch_all_urls(domain)
    csv_data = generate_csv(all_urls)
    return csv_data

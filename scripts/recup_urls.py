import requests
import re
import csv
from xml.etree import ElementTree as ET
from io import StringIO

def get_sitemaps_from_robots(robots_url):
    response = requests.get(robots_url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération du fichier robots.txt: {response.status_code}")
        return []
    
    sitemaps = re.findall(r'Sitemap\s*:\s*(https?://\S+)', response.text, re.IGNORECASE)
    return sitemaps

def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération du sitemap: {response.status_code}")
        return [], []
    
    urls = []
    sitemaps = []
    
    try:
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
    except ET.ParseError as e:
        print(f"Erreur lors de l'analyse du sitemap: {e}")
    
    return urls, sitemaps

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

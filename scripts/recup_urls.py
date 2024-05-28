import requests
from bs4 import BeautifulSoup
import csv
import base64
from io import StringIO, BytesIO

def fetch_sitemap_urls(domain):
    robots_url = f"https://{domain}/robots.txt"
    sitemap_url = f"https://{domain}/sitemap.xml"
    try:
        response = requests.get(robots_url)
        response.raise_for_status()
        sitemap_urls = []
        for line in response.text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_urls.append(line.split(":")[1].strip())
        if not sitemap_urls:
            sitemap_urls.append(sitemap_url)
        return sitemap_urls
    except requests.RequestException:
        return [sitemap_url]

def fetch_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')  # Utiliser le parser html.parser
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls
    except requests.RequestException:
        return []

def generate_csv(urls):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["URL"])
    for url in urls:
        writer.writerow([url])
    return output.getvalue()

def encode_to_base64(data):
    binary = BytesIO()
    binary.write(data.encode('utf-8'))
    binary.seek(0)
    return base64.b64encode(binary.read()).decode('utf-8')

def recup_urls(domain):
    sitemap_urls = fetch_sitemap_urls(domain)
    all_urls = []
    for sitemap_url in sitemap_urls:
        all_urls.extend(fetch_urls_from_sitemap(sitemap_url))
    csv_data = generate_csv(all_urls)
    encoded_csv = encode_to_base64(csv_data)
    return {"csv_data": encoded_csv}

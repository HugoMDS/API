import requests
from bs4 import BeautifulSoup
import csv
from io import StringIO

def fetch_sitemap_urls(domain):
    robots_url = f"https://{domain}/robots.txt"
    sitemap_url = f"https://{domain}/sitemap.xml"
    print(f"Fetching sitemap URLs from {robots_url} and {sitemap_url}")
    try:
        response = requests.get(robots_url)
        response.raise_for_status()
        sitemap_urls = []
        for line in response.text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_urls.append(line.split(":")[1].strip())
        if not sitemap_urls:
            sitemap_urls.append(sitemap_url)
        print(f"Found sitemap URLs: {sitemap_urls}")
        return sitemap_urls
    except requests.RequestException as e:
        print(f"Error fetching sitemap URLs: {e}")
        return [sitemap_url]

def fetch_urls_from_sitemap(sitemap_url):
    print(f"Fetching URLs from sitemap {sitemap_url}")
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = [loc.text for loc in soup.find_all('loc')]
        print(f"Found URLs: {urls}")
        return urls
    except requests.RequestException as e:
        print(f"Error fetching URLs from sitemap: {sitemap_url}, error: {e}")
        return []

def fetch_all_urls(domain):
    sitemap_urls = fetch_sitemap_urls(domain)
    all_urls = []
    for sitemap_url in sitemap_urls:
        urls = fetch_urls_from_sitemap(sitemap_url)
        for url in urls:
            if url.endswith('.xml'):
                all_urls.extend(fetch_urls_from_sitemap(url))
            else:
                all_urls.append(url)
    print(f"All fetched URLs: {all_urls}")
    return all_urls

def generate_csv(urls):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["URL"])
    for url in urls:
        writer.writerow([url])
    return output.getvalue()

def recup_urls(domain):
    all_urls = fetch_all_urls(domain)
    csv_data = generate_csv(all_urls)
    return csv_data

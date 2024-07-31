from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def verifier_disponibilite(ndd):
    # Configuration des options du navigateur
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécution en mode headless (sans interface graphique)
    chrome_options.add_argument("--disable-gpu")  # Nécessaire pour le mode headless sur Windows
    chrome_options.add_argument("--no-sandbox")  # Nécessaire pour le mode headless sur certaines configurations

    # Initialisation du navigateur
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = f"https://who.is/whois/{ndd}"
        driver.get(url)

        # Attendre le chargement de la page
        time.sleep(5)  # Ajustez ce délai si nécessaire

        # Vérifier le contenu de la page pour déterminer la disponibilité
        if "is available!" in driver.page_source:
            return {"status": "available", "domain": ndd}
        elif "is already registered" in driver.page_source:
            return {"status": "registered", "domain": ndd}
        else:
            return {"status": "unknown", "domain": ndd}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Fermer le navigateur
        driver.quit()

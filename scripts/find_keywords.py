import requests
from bs4 import BeautifulSoup
import re

# Définir les mots-clés par catégorie
keywords = {
    "QVT": [
        "Bien-être au travail", "Santé au travail", "Équilibre vie professionnelle-vie personnelle", 
        "Motivation des employés", "Conditions de travail", "Engagement des employés", 
        "Satisfaction au travail", "Stress au travail", "Burnout", "Prévention des risques", 
        "Ambiance de travail", "Cohésion d’équipe", "Télétravail", "Management bienveillant", 
        "Reconnaissance au travail", "Ergonomie", "Santé mentale", "Rémunération équitable", 
        "Développement personnel", "Formation professionnelle", "Communication interne", 
        "Flexibilité des horaires", "Inclusion et diversité", "Autonomie au travail", "Climat social", 
        "Politiques RH", "Sécurité au travail", "Convivialité", "Responsabilité sociale de l’entreprise (RSE)", 
        "Développement durable", "Leadership participatif", "Innovation managériale", "Gestion du temps", 
        "Feedback constructif", "Espace de travail collaboratif", "Culture d’entreprise", "Valeurs d’entreprise", 
        "Évaluation des performances", "Gestion des talents", "Plan de carrière", "Accès aux services de santé", 
        "Médiation en entreprise", "Indicateurs de bien-être", "Programme de bien-être", 
        "Comité social et économique (CSE)", "Aménagement du temps de travail", "Partage des bonnes pratiques", 
        "Accompagnement professionnel", "Politique d’égalité", "Droit à la déconnexion"
    ],
    "certifications": [
        "Happy at Work", "Great Place to Work", "Top Employers", "Best Workplaces", 
        "ISO 45001 (Système de management de la santé et de la sécurité au travail)", 
        "ISO 45001", "ISO 9001 (Système de management de la qualité, incluant des aspects de la QVT)", 
        "ISO 9001", "OHSAS 18001", "OHSAS 18001 (Système de management de la santé et de la sécurité au travail, remplacé par ISO 45001)",
        "Label Lucie (Responsabilité sociétale des entreprises)", "Label Diversité (Promotion de la diversité et de l’égalité des chances)",
        "Label Egalité Professionnelle", "Label HappyIndex® / AtWork", "Label Entreprise où il fait bon travailler", "Label Responsible Care",
        "Label Worklife Balance (Équilibre vie professionnelle et vie personnelle)", "Label Employeur Responsable",
        "Label Sustainable HR (Ressources humaines durables)", "Certificat Workplace Wellness", "Certificat Healthy Workplaces",
        "Certificat Ergonomic Excellence", "Label Bien-être au Travail", "Label Humanité au Travail",
        "Label Santé et Qualité de Vie au Travail (SQVT)", "Certification MASE (Manuel d’Amélioration Sécurité des Entreprises)",
        "Label TOAST (Transparence, Ouverture, Authenticité, Soutien, et Transformation)",
        "Label « Relations fournisseurs et achats responsables »", "ISO", "Label"
    ],
    "marque_employeur": [
        "entreprise familiale", "marque employeur", "histoire", "fondé", "créé", "anniversaire",
        "génération", "héritage", "tradition", "valeurs familiales", "passation"
    ]
}

# Fonction pour analyser une page web
def analyze_page(url):
    found_keywords = []
    category_status = {"QVT": "non", "certifications": "non", "marque_employeur": "non"}
    general_status = "non"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire le contenu texte des balises HTML
            texts = soup.get_text(separator=' ')
            
            # Rechercher les mots-clés dans le texte par catégorie
            for category, words in keywords.items():
                category_keywords = []
                for keyword in words:
                    if re.search(r'\b' + re.escape(keyword) + r'\b', texts, re.IGNORECASE):
                        category_keywords.append(keyword)
                if category_keywords:
                    found_keywords.append({"category": category, "status": "oui", "keywords": category_keywords})
                    category_status[category] = "oui"
                else:
                    found_keywords.append({"category": category, "status": "non", "keywords": []})
            
            # Vérifier si au moins un des tableaux n'est pas vide pour le statut général
            if any(category_status[category] == "oui" for category in category_status):
                general_status = "oui"
    
    except Exception as e:
        print(f"Failed to analyze {url}: {str(e)}")
    
    return {"keywords": found_keywords, "category_status": category_status, "general_status": general_status}
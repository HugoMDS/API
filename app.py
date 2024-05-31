from flask import Flask, jsonify, request
import logging
from io import BytesIO
from scripts.recup_urls import recup_urls
from scripts.analyse_seo import analyze_and_report
from scripts.serp import scrape_google
from scripts.find_keywords import analyze_page
from scripts.detect_wordpress import is_wordpress_site
from scripts.pdf_utils import pdf_to_text

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return "Bienvenue à mon API Flask!"

@app.route('/api/check_wordpress', methods=['GET'])
def check_wordpress():
    app.logger.debug("check_wordpress route accessed")
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing query parameter 'url'"}), 400
    wordpress_status = is_wordpress_site(url)
    return jsonify({"wordpress": str(wordpress_status).lower()}), 200

@app.route('/api/recup_urls', methods=['GET'])
def get_urls():
    app.logger.debug("recup_urls route accessed")
    domain = request.args.get('domaine')
    if not domain:
        return jsonify({"error": "Missing query parameter 'domaine'"}), 400
    csv_data = recup_urls(domain)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=urls.csv'}
    )

@app.route('/api/analyse_seo', methods=['GET'])
def analyze_url():
    app.logger.debug("analyse_seo route accessed")
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing query parameter 'url'"}), 400
    result = analyze_and_report(url)
    return jsonify(result)

@app.route('/api/search', methods=['GET'])
def search_google():
    app.logger.debug("search_google route accessed")
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter 'query'"}), 400
    results = scrape_google(query)
    return jsonify(results)

@app.route('/api/find_keywords', methods=['GET'])
def find_keywords():
    app.logger.debug("find_keywords route accessed")
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing query parameter 'url'"}), 400

    try:
        keywords_found = analyze_page(url)
        if keywords_found:
            result = {"status": "oui", "keywords": keywords_found}
        else:
            result = {"status": "non", "keywords": []}
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pdf_to_text', methods=['POST'])
def api_pdf_to_text():
    if 'file' in request.files:
        file = request.files['file']
        try:
            pdf_file = BytesIO(file.read())
            text = pdf_to_text(pdf_file)
            return jsonify({"text": text}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.content_type == 'application/octet-stream':
        try:
            pdf_file = BytesIO(request.data)
            text = pdf_to_text(pdf_file)
            return jsonify({"text": text}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Missing 'file' in form-data or binary data in request body"}), 400

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

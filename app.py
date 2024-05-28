from flask import Flask, jsonify, request, Response
import logging
from scripts.recup_urls import recup_urls
from scripts.analyse_seo import process_csv
from scripts.serp import scrape_google

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return "Bienvenue à mon API Flask!"

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

@app.route('/api/analyse', methods=['POST'])
def analyze_csv():
    app.logger.debug("analyzs_csv route accessed")
    if 'csv_file' not in request.files:
        return jsonify({"error": "Missing file parameter 'csv_file'"}), 400
    file = request.files['csv_file']
    input_csv = file.read().decode('utf-8')
    result = process_csv(input_csv)
    return jsonify(result)

@app.route('/api/search', methods=['GET'])
def search_google():
    app.logger.debug("search_google route accessed")
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter 'query'"}), 400
    results = scrape_google(query)
    return jsonify(results)

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, jsonify, request
import logging
import json
from scripts.recup_urls import recup_urls
from scripts.test import process_csv

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return "Bienvenue à mon API Flask!"

@app.route('/api/search', methods=['GET'])
def get_urls():
    app.logger.debug("recup_urls route accessed")
    domain = request.args.get('domaine')
    if not domain:
        return jsonify({"error": "Missing query parameter 'domaine'"}), 400
    result = recup_urls(domain)
    return jsonify(result)

@app.route('/api/recup_urls', methods=['GET'])
def get_urls():
    app.logger.debug("recup_urls route accessed")
    domain = request.args.get('domaine')
    if not domain:
        return jsonify({"error": "Missing query parameter 'domaine'"}), 400
    result = recup_urls(domain)
    return jsonify(result)

@app.route('/api/analyse_seo', methods=['POST'])
def analyze_csv():
    app.logger.debug("test route accessed")
    if 'csv_file' not in request.files:
        return jsonify({"error": "Missing file parameter 'csv_file'"}), 400
    file = request.files['csv_file']
    input_csv = file.read().decode('utf-8')
    result = process_csv(input_csv)
    return jsonify(result)

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

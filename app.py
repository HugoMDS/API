from flask import Flask, jsonify, request
import logging
import json
from scripts.serp import scrape_google

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return "Bienvenue à mon API Flask!"

@app.route('/api/search', methods=['GET'])
def run_search():
    app.logger.debug("Search route accessed")
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    results = scrape_google(query)
    return jsonify(results)

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

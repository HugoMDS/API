from flask import Flask, jsonify, request
import logging
import subprocess
import json

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
    result = subprocess.run(['python3', 'scripts/serp.py', query], capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500
    response_data = json.loads(result.stdout)
    return jsonify(response_data)

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

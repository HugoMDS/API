from flask import Flask, jsonify, request, send_file
import logging
import subprocess
import json
import sys
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Fonction pour installer les dépendances
def install_dependencies():
    try:
        with open('/tmp/install_log.txt', 'w') as f:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=f, stderr=f)
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], stdout=f, stderr=f)
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

# Appeler la fonction pour installer les dépendances
install_dependencies()

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
    result = subprocess.run([sys.executable, 'scripts/serp.py', query], capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500
    response_data = json.loads(result.stdout)
    return jsonify(response_data)

@app.route('/logs')
def get_logs():
    try:
        return send_file('/tmp/install_log.txt')
    except FileNotFoundError:
        return "Log file not found", 404

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

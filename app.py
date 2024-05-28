from flask import Flask, jsonify
import logging
import subprocess

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return "Bienvenue à mon API Flask!"

@app.route('/api/script1', methods=['GET'])
def run_script1():
    app.logger.debug("Script 1 route accessed")
    result = subprocess.run(['python3', 'scripts/script1.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

@app.route('/api/script2', methods=['GET'])
def run_script2():
    app.logger.debug("Script 2 route accessed")
    result = subprocess.run(['python3', 'scripts/script2.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

@app.route('/api/script3', methods=['GET'])
def run_script3():
    app.logger.debug("Script 3 route accessed")
    result = subprocess.run(['python3', 'scripts/script3.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

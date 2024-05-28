from flask import Flask, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return "Bienvenue à mon API Flask!"

@app.route('/api/data', methods=['GET'])
def get_data():
    app.logger.debug("Data route accessed")
    data = {
        "message": "Voici vos données",
        "data": [1, 2, 3, 4, 5]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

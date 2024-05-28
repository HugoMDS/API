from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue à mon API Flask!"

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Voici vos données",
        "data": [1, 2, 3, 4, 5]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Commentaire pour forcer un redéploiement
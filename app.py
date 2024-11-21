from flask import Flask, jsonify, request, Response
import logging
from io import BytesIO
from scripts.recup_urls import recup_urls
from scripts.analyse_seo import analyze_and_report
from scripts.serp import scrape_google
from scripts.detect_wordpress import is_wordpress_site
from scripts.pdf_utils import pdf_to_text
from scripts.hasard import choose_random_word
from scripts.ics_converter import text_to_ics  # Import the new script
from scripts.process_audio import compress_audio
from scripts.slice_audio import slice_audio
from scripts.generate_pdf import generate_pdf_from_html

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

@app.route('/api/random_word', methods=['GET'])
def random_word():
    app.logger.debug("random_word route accessed")
    chosen_word = choose_random_word()
    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                h1 {{
                    font-size: 10vw;
                    color: {chosen_word};
                }}
            </style>
        </head>
        <body>
            <h1>{chosen_word}</h1>
        </body>
    </html>
    """
    return html_content, 200

@app.route('/api/text_to_ics', methods=['POST'])
def text_to_ics_api():
    app.logger.debug("text_to_ics route accessed")
    ics_text = request.data.decode('utf-8')
    if not ics_text:
        return jsonify({"error": "Missing ICS text in request body"}), 400
    
    ics_data = text_to_ics(ics_text)
    response = Response(
        ics_data,
        mimetype='application/octet-stream',
        headers={'Content-Disposition': 'attachment;filename=calendar.ics'}
    )
    return response, 200

# Endpoint pour compresser un fichier audio
@app.route('/compress_audio', methods=['POST'])
def handle_compress_audio():
    return compress_audio()


@app.route('/slice_audio', methods=['POST'])
def handle_slice_audio():
    return slice_audio()

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        # Récupérer le HTML envoyé dans la requête
        data = request.get_json()
        if 'html' not in data:
            return jsonify({"error": "HTML content is required"}), 400

        html_content = data['html']

        # Générer le PDF
        pdf_buffer = generate_pdf_from_html(html_content)

        # Retourner le PDF directement
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name="generated.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.logger.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5000)

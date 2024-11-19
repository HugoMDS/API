from flask import request, jsonify
from pydub import AudioSegment
import io

def slice_audio():
    """
    Endpoint pour découper un fichier audio.
    """
    try:
        # Vérifie si un fichier a été envoyé
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400

        file = request.files['file']

        # Vérifie si les paramètres start_time et end_time sont présents
        if 'start_time' not in request.form or 'end_time' not in request.form:
            return jsonify({"error": "Paramètres start_time et end_time requis"}), 400

        # Récupère les paramètres
        start_time = int(request.form['start_time'])  # En millisecondes
        end_time = int(request.form['end_time'])  # En millisecondes

        # Vérifie si le fichier a un nom valide
        if file.filename == '':
            return jsonify({"error": "Nom de fichier manquant"}), 400

        # Charger l'audio avec Pydub
        audio = AudioSegment.from_file(file.stream)

        # Vérifie que les temps sont valides
        if start_time < 0 or end_time > len(audio):
            return jsonify({"error": "Les temps start_time et end_time doivent être dans la plage de l'audio"}), 400

        # Découpe l'audio
        sliced_audio = audio[start_time:end_time]

        # Exporter la partie découpée
        sliced_audio_data = io.BytesIO()
        sliced_audio.export(sliced_audio_data, format="mp3")
        sliced_audio_data.seek(0)

        return jsonify({
            "message": "Audio découpé avec succès",
            "sliced_duration_ms": len(sliced_audio)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

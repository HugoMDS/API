from flask import request, jsonify
from pydub import AudioSegment
import io

def compress_audio():
    """
    Endpoint pour compresser un fichier audio.
    """
    try:
        # Vérifie si un fichier a été envoyé
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400

        file = request.files['file']

        # Vérifie si le fichier a un nom valide
        if file.filename == '':
            return jsonify({"error": "Nom de fichier manquant"}), 400

        # Charger le fichier audio dans pydub
        audio = AudioSegment.from_file(file.stream)

        # Compression de l'audio à un bitrate réduit (ex. 64kbps)
        compressed_audio = io.BytesIO()
        audio.export(compressed_audio, format="mp3", bitrate="64k")
        compressed_audio.seek(0)

        # Retourne les informations sur le fichier compressé
        return jsonify({
            "message": "Audio compressé avec succès",
            "file_size_bytes": len(compressed_audio.getvalue())
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import csv
import base64
from io import StringIO, BytesIO
import json

def analyze_csv(input_csv):
    input_data = StringIO(input_csv)
    reader = csv.DictReader(input_data)
    
    analyzed_data = []
    for row in reader:
        # Ajoutez ici votre logique d'analyse
        row['analyzed'] = "yes"  # Exemple d'ajout d'une colonne
        analyzed_data.append(row)
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=reader.fieldnames + ['analyzed'])
    writer.writeheader()
    for row in analyzed_data:
        writer.writerow(row)
    return output.getvalue()

def encode_to_base64(data):
    binary = BytesIO()
    binary.write(data.encode('utf-8'))
    binary.seek(0)
    return base64.b64encode(binary.read()).decode('utf-8')

def process_csv(input_csv):
    analyzed_csv = analyze_csv(input_csv)
    encoded_csv = encode_to_base64(analyzed_csv)
    return {"csv_data": encoded_csv}

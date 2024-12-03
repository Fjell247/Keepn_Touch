import random
import json
from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# Google Drive API-Setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = r"C:\Users\fjell\Desktop\Python\Keepn_Touch\Skripte\keepntouch-1a62cb9a0021.json"  # Dein Service Account Key

# Google Drive-Dienst erstellen
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# ID der Google Drive-Datei (die JSON-Datei)
file_id = '16MGBkcIBITFXvI8TBquLn8VKFesVoLgm'

def download_json(file_id):
    """Lädt die JSON-Datei von Google Drive herunter und gibt den Inhalt zurück."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return json.load(fh)

def get_random_names(contact_list, num_names=3):
    """Wählt zufällig eine bestimmte Anzahl von Namen aus der Liste."""
    return random.sample(contact_list, num_names)

@app.route('/get_random_names', methods=['GET'])
def get_random_names_from_drive():
    """API-Endpunkt, der zufällige Namen aus der JSON-Datei zurückgibt."""
    contacts = download_json(file_id)
    
    # Anpassen der Verarbeitung der JSON-Daten, da es sich um eine Liste handelt
    contact_names = [contact['name'] for contact in contacts]  # Kontakte direkt aus der Liste extrahieren
    
    random_names = get_random_names(contact_names, 3)  # Wähle 3 zufällige Namen
    return jsonify(random_names)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



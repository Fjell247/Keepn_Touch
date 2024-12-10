import random
import json
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os
# Flask-App konfigurieren, um HTML-Datei im gleichen Ordner zu nutzen
app = Flask(__name__, template_folder='.')

CORS(app)



def load_contacts():
    """Lädt die Kontakte aus der JSON-Datei relativ zum Skript."""
    # Pfad relativ zu diesem Skript
    file_path = os.path.join(os.path.dirname(__file__),  "chosen_contacts.json")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_random_names(contact_list, num_names=3):
    """Wählt zufällig eine bestimmte Anzahl von Namen aus der Liste."""
    return random.sample(contact_list, num_names)

@app.route('/')
def index():
    """Zeigt die HTML-Datei an."""
    return render_template('handy_widget_frontend.html')

@app.route('/get_random_names', methods=['GET'])
def get_random_names_from_file():
    """API-Endpunkt, der zufällige Namen aus der JSON-Datei zurückgibt."""
    contacts = load_contacts()  # Kontakte laden
    contact_names = [contact['name'] for contact in contacts]  # Nur die Namen extrahieren
    random_names = get_random_names(contact_names, 3)  # Wähle 3 zufällige Namen
    return jsonify(random_names)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

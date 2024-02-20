import os
import requests
import frontmatter
import json
from collections import defaultdict
from tqdm import tqdm
from time import sleep


def get_location_data(lat, lon):
    try:
        print(f"API-Anfrage für Koordinaten: {lat}, {lon}")
        response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}")
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            location_info = {
                'tourism': address.get('tourism', 'Unbekannt'),
                'road': address.get('road', 'Unbekannt'),
                'postcode': address.get('postcode', 'Unbekannt'),
                'country': address.get('country', 'Unbekannt'),
                'country_code': address.get('country_code', 'Unbekannt'),
                'town': address.get('town', address.get('city', 'Unbekannt'))
            }
            return data['address']['country'], location_info
        else:
            print(f"API-Fehler: {response.status_code}, Antwort: {response.text}")
            return None, None
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten für {lat}, {lon}: {e}")
        return None, None

def get_md_files(content_dir):
    md_files = []
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                md_files.append(path)
    return md_files


def main():
    content_dir = 'content/plaetze'
    md_files = get_md_files(content_dir)  # Sammeln aller MD-Dateien
    stats = defaultdict(lambda: {"Besuche": 0, "Orte": [], "country_code": ""})

    print(f"Starte Verarbeitung im Verzeichnis: {content_dir}")
    # Verwende tqdm über die gesamte Liste der MD-Dateien
    for path in tqdm(md_files, desc="Verarbeite Dateien"):
        post = frontmatter.load(path)
        file = os.path.basename(path)

        if 'coordinates' in post.metadata:
            lat = post.metadata['coordinates']['latitude']
            lon = post.metadata['coordinates']['longitude']
            country, location_info = get_location_data(lat, lon)

            if country:
                stats[country]["Besuche"] += 1
                stats[country]["Orte"].append({
                    "Ort": location_info['tourism'],
                    "Strasse": location_info['road'],
                    "Stadt": location_info['town'],
                    "PLZ": location_info['postcode'],
                    "Land": location_info['country'],
                    "Dateiname": file
                })
                if stats[country]["country_code"] == "":
                    stats[country]["country_code"] = location_info['country_code']

    with open('data/stats.json', 'w') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

    print("Statistiken erfolgreich erstellt.")

if __name__ == "__main__":
    main()

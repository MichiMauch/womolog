import requests
import re
from pathlib import Path
import json
from tqdm import tqdm  # Importieren von tqdm für den Fortschrittsbalken

# Funktion zur Berechnung der Distanz mit der OSRM-API
def calculate_distance(start_latitude, start_longitude, end_latitude, end_longitude):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_longitude},{start_latitude};{end_longitude},{end_latitude}?overview=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        distance = data['routes'][0]['distance'] / 1000  # Umwandlung von Metern in Kilometer
        return distance
    else:
        print("Fehler bei der Anfrage:", response.status_code)
        return None

# Funktion zum Extrahieren von Koordinaten und Datum (Jahr)
def extract_information(md_content):
    coordinates_pattern = re.compile(r'coordinates:\s*\n\s*latitude: ([\d.-]+)\s*\n\s*longitude: ([\d.-]+)')
    date_pattern = re.compile(r'date: (\d{4})-\d{2}-\d{2}')

    coordinates_match = coordinates_pattern.search(md_content)
    date_match = date_pattern.search(md_content)

    latitude, longitude = (float(coordinates_match.group(1)), float(coordinates_match.group(2))) if coordinates_match else (None, None)
    year = int(date_match.group(1)) if date_match else "Unbekanntes Jahr"

    return latitude, longitude, year

# Festgelegte Startkoordinaten
start_latitude = 47.33887
start_longitude = 8.05032

# Verzeichnispfade
md_directory_path = '/Users/michaelmauch/Documents/hugo/mauch.rocks/content/plaetze'
output_json_path = '/Users/michaelmauch/Documents/hugo/mauch.rocks/data/distance.json'

results = []

md_files = list(Path(md_directory_path).rglob('*.md'))
# Verwendung von tqdm für den Fortschrittsbalken
for md_file in tqdm(md_files, desc="Verarbeite Markdown-Dateien"):
    with open(md_file, 'r', encoding='utf-8') as file:
        md_content = file.read()
        latitude, longitude, year = extract_information(md_content)
        if latitude is not None and longitude is not None:
            distance = calculate_distance(start_latitude, start_longitude, latitude, longitude)
            if distance is not None:
                results.append({
                    'file_name': md_file.name,  # Speichern des Dateinamens
                    'year': year,
                    'distance_km': distance
                })

# Speichern der Ergebnisse in einer JSON-Datei
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, indent=4)

print(f"Die Daten wurden erfolgreich in {output_json_path} gespeichert.")

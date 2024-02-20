import json
from pathlib import Path

# Pfade definieren
json_path = '/Users/michaelmauch/Documents/hugo/mauch.rocks/data/distance.json'
md_directory_path = '/Users/michaelmauch/Documents/hugo/mauch.rocks/content/plaetze'

# JSON-Daten laden
with open(json_path, 'r', encoding='utf-8') as json_file:
    distances = json.load(json_file)

# Markdown-Dateien durchlaufen
for md_file in Path(md_directory_path).rglob('*.md'):
    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.readlines()

    frontmatter_end_index = None
    for index, line in enumerate(content):
        if line.strip() == '---':
            frontmatter_end_index = index
            break

    # Prüfen, ob die Datei in den JSON-Daten erwähnt wird
    for entry in distances:
        if md_file.name == entry['file_name']:
            # Entfernen aller bestehenden distance_km: Einträge nach dem Frontmatter
            if frontmatter_end_index is not None:
                content = [line for line in content if not line.strip().startswith('distance_km:') or content.index(line) <= frontmatter_end_index]
            
            # Finden, wo die Koordinaten beginnen
            coordinates_index = None
            for index, line in enumerate(content):
                if line.startswith('coordinates:'):
                    coordinates_index = index
                    break

            if coordinates_index is not None:
                distance_line = f"distance_km: {entry['distance_km']}\n"
                # Einfügen der Kilometerangabe direkt vor den Koordinaten
                content.insert(coordinates_index, distance_line)

                # Datei mit aktualisierten Inhalten schreiben
                with open(md_file, 'w', encoding='utf-8') as file:
                    file.writelines(content)

                print(f"Kilometerangabe wurde zu {md_file.name} hinzugefügt.")
            break  # Da die Datei gefunden und bearbeitet wurde, brechen wir die Schleife ab

print("Kilometerangaben wurden aktualisiert.")

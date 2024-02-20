#!/bin/bash

# Frage den Benutzer, ob das Python-Skript ausgeführt werden soll
read -p "Möchtest du 'python3 generate_stats.py' ausführen? (j/n) " answer

# Überprüfe die Benutzereingabe
if [[ $answer = j ]]; then
    # Führe das Python-Skript aus
    python3 static/generate_stats.py

    # Überprüfe, ob das Python-Skript erfolgreich war
    if [ $? -ne 0 ]; then
        echo "Das Python-Skript ist fehlgeschlagen. Skript wird beendet."
        exit 1
    fi
fi

# Frage den Benutzer, ob die Kilometer aktualisiert werden sollen
read -p "Möchtest du die Kilometer aktualisieren? (j/n) " km_answer

if [[ $km_answer = j ]]; then
    # Führe das Python-Skript aus, um das JSON-File zu erstellen
    python3 static/calculate_routing.py

    # Überprüfe, ob das Python-Skript erfolgreich war
    if [ $? -ne 0 ]; then
        echo "Das Python-Skript zur Berechnung der Kilometer ist fehlgeschlagen. Skript wird beendet."
        exit 1
    fi

    # Führe das Python-Skript aus, um die MD-Files zu aktualisieren
    python3 static/import_km.py

    # Überprüfe, ob das Python-Skript erfolgreich war
    if [ $? -ne 0 ]; then
        echo "Das Python-Skript zum Importieren der Kilometer in die MD-Files ist fehlgeschlagen. Skript wird beendet."
        exit 1
    fi
fi

# Frage nach einem Kommentar für den Commit
echo "Bitte gib einen Kommentar für den Commit ein:"
read commitMessage

# Füge alle Änderungen hinzu, erstelle einen Commit mit dem eingegebenen Kommentar und pushe
git add .
git commit -m "$commitMessage"
git push origin main

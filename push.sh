#!/bin/bash

# Frage den Benutzer, ob das Python-Skript ausgeführt werden soll
read -p "Do you want to update the stats? (j/n) " answer

# Überprüfe die Benutzereingabe
if [[ $answer = j ]]; then
    # Führe das Python-Skript aus
    python3 generate_stats.py

    # Überprüfe, ob das Python-Skript erfolgreich war
    if [ $? -ne 0 ]; then
        echo "Das Python-Skript ist fehlgeschlagen. Skript wird beendet."
        exit 1
    fi
fi

# Füge alle Änderungen hinzu, erstelle einen Commit und pushe
git add .
git commit -m "es gibt news"
git push origin main

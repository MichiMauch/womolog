import pandas as pd
import requests

# Lade die vorhandene CSV-Datei
csv_file = "capitals-corrdinates.csv"
df = pd.read_csv(csv_file)

# Entferne die Spalte 'Population'
df = df.drop('Population', axis=1)

# API-URL für Länderinformationen
api_url = "http://www.geognos.com/api/en/countries/info/all.json"

# Lade Daten von der API und handle mögliche Fehler
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Überprüfe, ob die Anfrage erfolgreich war
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Fehler bei der Anfrage an die API: {e}")
    data = {}  # Setze data auf ein leeres Dictionary, um weitere Fehler zu verhindern

# Funktionen zum Extrahieren verschiedener Ländercodes
def get_country_code(country_name, code_type):
    if isinstance(country_name, str):
        for iso2, country_data in data.get('Results', {}).items():
            if isinstance(country_data, dict) and 'Name' in country_data and country_data['Name'] == country_name:
                return country_data.get('CountryCodes', {}).get(code_type, None)
    return None

# Füge neue Spalten für verschiedene Codes hinzu
df['ISO2'] = df['Country'].apply(lambda x: get_country_code(x, 'iso2'))
df['ISO3'] = df['Country'].apply(lambda x: get_country_code(x, 'iso3'))
df['TLD'] = df['Country'].apply(lambda x: get_country_code(x, 'tld'))
df['FIPS'] = df['Country'].apply(lambda x: get_country_code(x, 'fips'))
df['ISON'] = df['Country'].apply(lambda x: get_country_code(x, 'isoN'))

# Speichere das erweiterte DataFrame in eine neue CSV-Datei
erweiterte_csv = "erweiterte_datei.csv"
df.to_csv(erweiterte_csv, index=False)

print("Die CSV-Datei wurde erfolgreich erweitert und gespeichert.")

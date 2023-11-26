import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Pfad zur Quelldatei
csv_file = "erweiterte_datei.csv"

# Lade die vorhandene CSV-Datei
df = pd.read_csv(csv_file)

# Konvertiere das DataFrame in ein GeoDataFrame
gdf = gpd.GeoDataFrame(
    df, geometry=[Point(xy) for xy in zip(df.Longitude, df.Latitude)]
)

# Speichere das GeoDataFrame als GeoJSON
geojson_file = "meineDaten.geojson"
gdf.to_file(geojson_file, driver="GeoJSON")

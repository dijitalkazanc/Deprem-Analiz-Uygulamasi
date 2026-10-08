import requests
import pandas as pd
import datetime

# USGS API endpoint
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Parametreler: Belirli tarih aralığı ve büyüklük gibi kriterler
params = {
    "format": "geojson",
    "starttime": "2022-01-01",  # Başlangıç tarihi
    "endtime": datetime.datetime.now().strftime("%Y-%m-%d"),  # Bitiş tarihi (bugünün tarihi)
    "minlatitude": 37.0,  # Kahramanmaraş'ın enlemi ve çevresi
    "maxlatitude": 38.0,
    "minlongitude": 36.0,  # Kahramanmaraş'ın boylamı ve çevresi
    "maxlongitude": 37.5,
    "minmagnitude": 2,  # 3.0 ve üzeri depremler
    "limit": 100  # Çekilecek maksimum veri sayısı (1000 veri)
}

# API'yi sorgulama
response = requests.get(url, params=params)

# JSON verisini al
data = response.json()

# Verileri işleyip bir DataFrame'e dönüştür
df = pd.json_normalize(data["features"])

# İlgili sütunları seçme ve bir kopya oluşturma (Büyüklük, Yer, Zaman, Koordinatlar ve Derinlik)
df_selected = df[['properties.mag', 'properties.place', 'properties.time', 'geometry.coordinates']].copy()

# Zaman sütununu formatlama (milliseconds'ten datetime'a çevirme)
df_selected['properties.time'] = pd.to_datetime(df_selected['properties.time'], unit='ms')

# Derinliği (depth) geometry.coordinates'in üçüncü öğesi olarak alıyoruz (long, lat, depth şeklinde)
df_selected['depth'] = df_selected['geometry.coordinates'].apply(lambda x: x[2])

# Yeni bir DataFrame oluşturma: Zaman, Derinlik, Büyüklük
df_final = df_selected[['properties.time', 'depth', 'properties.mag']].copy()

# Sütun isimlerini daha okunabilir hale getirme
df_final.columns = ['Zaman', 'Derinlik (km)', 'Büyüklük']

# Verileri görüntüleme
print(df_final.head())

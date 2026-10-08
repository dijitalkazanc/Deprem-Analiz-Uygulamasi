import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import time

def depremleri_cek_koeri(url="http://www.koeri.boun.edu.tr/scripts/lst8.asp"):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    pre = soup.find('pre')
    lines = pre.text.strip().splitlines()

    depremler = []
    for line in lines:
        parts = line.split()
        if len(parts) < 7 or parts[0].startswith('----------') or parts[0].startswith('Date'):
            continue

        try:
            tarih = parts[0]
            saat = parts[1]
            lat = parts[2]
            lon = parts[3]
            derinlik = parts[4]
            mag = parts[5]
            yer = ' '.join(parts[6:])
            
            # İl ismini () içinden alalım
            il_eslesme = re.search(r'\(([^()]+)\)', yer)
            if il_eslesme:
                il = il_eslesme.group(1).strip().title()  # Örn: "BALIKESIR" → "Balikesir"
            else:
                il = "Bilinmeyen"

            depremler.append({
                "tarih": f"{tarih} {saat}",
                "enlem": lat,
                "boylam": lon,
                "derinlik": derinlik,
                "buyukluk": mag,
                "yer": yer,
                "il": il
            })
        except Exception as e:
            print(f"Hata oluştu: {e}")
            continue

    return depremler

def kaydet_csv(depremler):
    alanlar = ["tarih", "enlem", "boylam", "derinlik", "buyukluk", "yer", "il"]

    # Ana dosya
    with open("tum_depremler.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=alanlar)
        writer.writeheader()
        writer.writerows(depremler)

    # İl bazlı klasör
    os.makedirs("il_bazli", exist_ok=True)
    iller = {}

    for dep in depremler:
        il = dep["il"]
        # Dosya adında geçersiz karakterleri temizle
        il_temiz = re.sub(r'[<>:"/\\|?*]', '_', il)
        iller.setdefault(il_temiz, []).append(dep)

    for il, liste in iller.items():
        dosya_adi = f"il_bazli/{il}.csv"
        with open(dosya_adi, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=alanlar)
            writer.writeheader()
            writer.writerows(liste)

    print(f"Toplam {len(depremler)} kayıt işlendi. {len(iller)} il için CSV oluşturuldu.")

# Çalıştır
def calistir():
    depremler = depremleri_cek_koeri()
    kaydet_csv(depremler)

if __name__ == "__main__":
    calistir()

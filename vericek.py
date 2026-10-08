import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import unicodedata


def depremleri_cek_koeri(url="http://www.koeri.boun.edu.tr/scripts/lst8.asp"):
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
    except Exception as e:
        print("Siteye bağlanılamadı:", e)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    pre = soup.find('pre')

    if not pre:
        print("Veri bulunamadı.")
        return []

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

            # İl ismini parantez içinden al
            il_eslesme = re.search(r'\(([^()]+)\)', yer)

            if il_eslesme:
                il = il_eslesme.group(1).strip().title()
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
            print("Satır işlenirken hata:", e)
            continue

    return depremler


# DOSYA ADI GÜVENLİ HALE GETİRME
def dosya_adi_duzelt(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r'[\\/*?:"<>|]', "_", text)
    text = text.strip()
    return text


def kaydet_csv(depremler):
    if not depremler:
        print("Kaydedilecek veri yok.")
        return

    alanlar = ["tarih", "enlem", "boylam", "derinlik", "buyukluk", "yer", "il"]

    # Tüm depremler tek dosya
    with open("tum_depremler.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=alanlar)
        writer.writeheader()
        writer.writerows(depremler)

    # İl bazlı klasör oluştur
    os.makedirs("il_bazli", exist_ok=True)

    iller = {}
    for dep in depremler:
        il = dep["il"]
        iller.setdefault(il, []).append(dep)

    for il, liste in iller.items():
        temiz_il = dosya_adi_duzelt(il)
        dosya_adi = os.path.join("il_bazli", f"{temiz_il}.csv")

        with open(dosya_adi, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=alanlar)
            writer.writeheader()
            writer.writerows(liste)

    print(f"Toplam {len(depremler)} kayıt işlendi. {len(iller)} il için CSV oluşturuldu.")


def calistir():
    depremler = depremleri_cek_koeri()
    kaydet_csv(depremler)


if __name__ == "__main__":
    calistir()

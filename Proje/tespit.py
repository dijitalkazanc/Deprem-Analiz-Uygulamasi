import os
import csv
from datetime import datetime, timedelta
import time

def potansiyel_tehlikeli_ilceler(kontrol_klasor="il_bazli"):
    simdi = datetime.now()
    bir_gun_once = simdi - timedelta(days=1)

    kritik_iller = []

    for dosya in os.listdir(kontrol_klasor):
        if not dosya.endswith(".csv"):
            continue

        dosya_yolu = os.path.join(kontrol_klasor, dosya)
        il_adi = os.path.splitext(dosya)[0]

        kucuk_deprem_sayisi = 0
        buyuk_deprem_var = False

        with open(dosya_yolu, newline='', encoding="iso-8859-9") as f:
            reader = csv.reader(f)

            # İlk 3 satırı atla
            for _ in range(3):
                next(reader, None)

            for satir in reader:
                try:
                    if "Tarih" in satir[0]:
                        continue  # Gereksiz başlık satırı varsa atla

                    tarih_str = satir[0].strip()
                    tarih_dt = datetime.strptime(tarih_str, "%Y.%m.%d %H:%M:%S")

                    if tarih_dt >= bir_gun_once:
                        buyukluk_str = satir[5].split()[0].replace(",", ".").strip()
                        if buyukluk_str == "-.-":
                            continue

                        buyukluk = float(buyukluk_str)

                        if buyukluk >= 6.0:
                            buyuk_deprem_var = True
                            
                        elif buyukluk <= 5.0:
                            kucuk_deprem_sayisi += 1
                            

                except Exception as e:
                    print(f"Hata (dosya: {dosya}): {e}")
                    continue

##        # Eğer 6+ deprem yok ve 30'dan fazla 5'ten küçük deprem varsa
##        if not buyuk_deprem_var and kucuk_deprem_sayisi > 30:
##            kritik_iller.append((il_adi, kucuk_deprem_sayisi))
        # SADECE 30'dan fazla 5'ten küçük deprem varsa
        if kucuk_deprem_sayisi > 25:
            kritik_iller.append((il_adi, kucuk_deprem_sayisi))
            

    # Raporlama
    if kritik_iller:
        print("\n⚠️  DİKKAT: Potansiyel stres birikimi görülen iller (6+ deprem yok, ama 25'dan fazla M<5 deprem var):\n")
        for il, adet in kritik_iller:
            print(f"- {il}: {adet} adet M<5 deprem (24 saatte)")
    else:
        print("🔍 Uyarı eşiğine uyan hiçbir il bulunamadı.")

# Fonksiyonu çalıştır
def calistir():
    potansiyel_tehlikeli_ilceler()

if __name__ == "__main__":
    calistir()


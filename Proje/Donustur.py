import pandas as pd

# Excel dosyasının yolu
excel_file_path = 'hamveri.xlsx'  # veya .xls

# Excel dosyasını oku
df = pd.read_excel(excel_file_path)

# CSV olarak kaydet (virgül ile ayrılmış)
csv_file_path = 'dosya_adı.csv'
df.to_csv(csv_file_path, index=False, sep=',', encoding='utf-8')

print(f"Excel dosyası başarıyla CSV'ye dönüştürüldü: {csv_file_path}")

import sqlite3
import os

db_path = 'sofor_guvenlik.db'
print(f"Veritabanı güncelleniyor: {os.path.abspath(db_path)}")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Şoförleri ve atayacağımız plakaları belirleyelim
plakalar = {
    'ahmet': '34 ABC 001',
    'mehmet': '06 XYZ 999',
    'fatma': '35 DEF 777',
    'can': '34 CAN 34'
}

for kadi, plaka in plakalar.items():
    cur.execute("UPDATE soforler SET arac_plaka = ? WHERE kullanici_adi = ?", (plaka, kadi))
    print(f"Şoför '{kadi}' için plaka '{plaka}' olarak güncellendi.")

conn.commit()
conn.close()
print("Tüm şoförlerin plakaları başarıyla dolduruldu!")

import sqlite3
import os

db_path = 'sofor_guvenlik.db'
print(f"Veritabanı kontrol ediliyor: {os.path.abspath(db_path)}")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. soforler tablosuna profil_resmi ekle
try:
    cur.execute("ALTER TABLE soforler ADD COLUMN profil_resmi TEXT")
    conn.commit()
    print("soforler tablosuna 'profil_resmi' sütunu eklendi.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("soforler tablosunda 'profil_resmi' sütunu zaten mevcut.")
    else:
        print(f"Hata (soforler): {e}")

# 2. yolcular tablosuna profil_resmi ekle
try:
    cur.execute("ALTER TABLE yolcular ADD COLUMN profil_resmi TEXT")
    conn.commit()
    print("yolcular tablosuna 'profil_resmi' sütunu eklendi.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("yolcular tablosunda 'profil_resmi' sütunu zaten mevcut.")
    else:
        print(f"Hata (yolcular): {e}")

conn.close()
print("Veritabanı güncelleme işlemi tamamlandı.")

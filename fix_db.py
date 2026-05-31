import sqlite3
import os

db_path = os.environ.get("DATABASE_PATH", 'sofor_guvenlik.db')
print(f"Checking database at: {os.path.abspath(db_path)}")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    # Sifre_plain sutununu ekle
    cur.execute("ALTER TABLE soforler ADD COLUMN sifre_plain TEXT")
    conn.commit()
    print("Sutun eklendi.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Sutun zaten mevcut.")
    else:
        print(f"Hata: {e}")

# Mevcut soforleri guncelle
cur.execute("UPDATE soforler SET sifre_plain = 'sifre123' WHERE kullanici_adi = 'ahmet'")
cur.execute("UPDATE soforler SET sifre_plain = 'sifre456' WHERE kullanici_adi = 'mehmet'")
cur.execute("UPDATE soforler SET sifre_plain = 'sifre789' WHERE kullanici_adi = 'fatma'")

# Yeni sofor Can'i ekle eger yoksa
try:
    import hashlib
    def sifreyi_hashle(sifre):
        return hashlib.sha256(sifre.encode()).hexdigest()
    
    cur.execute("INSERT OR IGNORE INTO soforler (ad, soyad, kullanici_adi, arac_plaka, sifre_hash, sifre_plain) VALUES (?, ?, ?, ?, ?, ?)",
                ("Can", "Yildiz", "can", "34 CAN 34", sifreyi_hashle("can123"), "can123"))
    print("Can Yildiz eklendi.")
except Exception as e:
    print(f"Sofor ekleme hatasi: {e}")

conn.commit()
conn.close()
print("Tamamlandi.")

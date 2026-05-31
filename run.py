import hashlib
import os
import sqlite3

from app import create_app, db
from app.models import Sofor, Alarm, SesLog, VardiyaSesKaydi, YolcuYorum, AracKonum


def _sha256(text: str) -> str:
    """SHA-256 ile şifre hash'i üretir (uygulama genelinde kullanılan yöntem)."""
    return hashlib.sha256(text.encode()).hexdigest()


def update_soforler_schema():
    """Eski DB şemasını yeni yapıya günceller (migration yardımcısı)."""
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sofor_guvenlik.db')
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(soforler)")
    columns = [col[1] for col in cur.fetchall()]

    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='soforler'")
    table_sql = cur.fetchone()

    has_unique_plaka = False
    if table_sql:
        sql_str = table_sql[0]
        if "UNIQUE" in sql_str and "arac_plaka" in sql_str:
            has_unique_plaka = True
        elif "NOT NULL" in sql_str and "arac_plaka" in sql_str:
            has_unique_plaka = True

    needs_email = 'email' not in columns or 'reset_token' not in columns or 'profil_resmi' not in columns

    if has_unique_plaka or needs_email:
        try:
            print("[MİGRASYON] soforler tablosu güncelleniyor...")
            cur.execute("ALTER TABLE soforler RENAME TO soforler_old")
            cur.execute("""
                CREATE TABLE soforler (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad            TEXT NOT NULL,
                    soyad         TEXT NOT NULL,
                    kullanici_adi TEXT NOT NULL UNIQUE,
                    email         TEXT UNIQUE,
                    arac_plaka    TEXT DEFAULT '',
                    sifre_hash    TEXT NOT NULL,
                    sifre_plain   TEXT,
                    reset_token   TEXT,
                    reset_token_expiry TEXT,
                    profil_resmi  TEXT
                )
            """)
            email_col = "email" if 'email' in columns else "NULL"
            reset_token_col = "reset_token" if 'reset_token' in columns else "NULL"
            reset_token_expiry_col = "reset_token_expiry" if 'reset_token_expiry' in columns else "NULL"
            profil_resmi_col = "profil_resmi" if 'profil_resmi' in columns else "NULL"
            cur.execute(f"""
                INSERT INTO soforler (id, ad, soyad, kullanici_adi, email, arac_plaka, sifre_hash, sifre_plain, reset_token, reset_token_expiry, profil_resmi)
                SELECT id, ad, soyad, kullanici_adi, {email_col}, COALESCE(arac_plaka, ''), sifre_hash, sifre_plain,
                       {reset_token_col}, {reset_token_expiry_col}, {profil_resmi_col}
                FROM soforler_old
            """)
            cur.execute("DROP TABLE soforler_old")
            conn.commit()
            print("[MİGRASYON BAŞARILI] soforler tablosu güncellendi.")
        except Exception as e:
            print(f"[MİGRASYON HATA] {e}")
            conn.rollback()
    conn.close()


def seed_demo_users(flask_app):
    """
    Demo kullanıcıları oluşturur.
    docker-compose up ile temiz bir ortamda bile hoca sisteme giriş yapabilsin diye
    her çalışmada kontrol eder; kullanıcı zaten varsa INSERT etmez.
    """
    with flask_app.app_context():
        # Tablolar yoksa oluştur
        db.create_all()

        demo_soforler = [
            {"ad": "Ahmet", "soyad": "Yılmaz", "kullanici_adi": "ahmet",
             "email": "ahmet@trustfleet.local", "arac_plaka": "34 ABC 001",
             "sifre": "sifre123"},
            {"ad": "Mehmet", "soyad": "Kaya", "kullanici_adi": "mehmet",
             "email": "mehmet@trustfleet.local", "arac_plaka": "06 XYZ 999",
             "sifre": "sifre456"},
            {"ad": "Admin", "soyad": "Merkez", "kullanici_adi": "admin",
             "email": "admin@trustfleet.local", "arac_plaka": "",
             "sifre": "admin123"},
        ]

        for s in demo_soforler:
            mevcut = db.session.scalar(
                db.select(Sofor).filter_by(kullanici_adi=s["kullanici_adi"])
            )
            if not mevcut:
                yeni = Sofor(
                    ad=s["ad"],
                    soyad=s["soyad"],
                    kullanici_adi=s["kullanici_adi"],
                    email=s["email"],
                    arac_plaka=s["arac_plaka"],
                    sifre_hash=_sha256(s["sifre"]),
                    # sifre_plain: Admin paneli "personel kartı" özelliği için saklanıyor.
                    # Gerçek üretim ortamında bu alan kaldırılmalıdır.
                    sifre_plain=s["sifre"],
                )
                db.session.add(yeni)
                print(f"[SEED] Demo şoför oluşturuldu: {s['kullanici_adi']}")

        db.session.commit()
        print("[SEED] Demo kullanıcı kontrolü tamamlandı.")


# ── Uygulama başlatma ─────────────────────────────────────────────────────────

update_soforler_schema()

app = create_app()
seed_demo_users(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Sofor': Sofor,
        'Alarm': Alarm,
        'SesLog': SesLog,
        'VardiyaSesKaydi': VardiyaSesKaydi,
        'YolcuYorum': YolcuYorum,
        'AracKonum': AracKonum,
    }


if __name__ == '__main__':
    print("TrustFleet — Sürüş Güvenlik Sunucusu başlatılıyor...")
    app.run(host='0.0.0.0', port=5000, debug=False)


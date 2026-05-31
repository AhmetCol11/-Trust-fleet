"""
=============================================================
 DOSYA: database.py
 AMAÇ : Veritabanı işlemlerini yöneten katman (Database Layer)
-------------------------------------------------------------
 📚 ÖĞRENME NOTU – Modüler Programlama Nedir?
 Büyük projeleri tek bir dosyaya yazmak yerine sorumluluklarına
 göre dosyalara bölmek iyi bir yazılım pratiğidir.
 Buna "Separation of Concerns" (Sorumlulukların Ayrılması) denir.
 Bu dosya YALNIZCA veritabanı işlemlerini yönetir.
 app.py ise YALNIZCA arayüzü yönetir.
=============================================================
"""

import sqlite3  # Python'la birlikte gelen, kurulum gerektirmeyen hafif veritabanı kütüphanesi
import hashlib  # Şifreleri düz metin saklamak güvensizdir; bu kütüphane şifreleri şifreler
import os


# ─────────────────────────────────────────────────────────────
# 📚 ÖĞRENME NOTU – SABİT DEĞİŞKEN (Constant)
# Veritabanı dosyasının adını bir değişkene atamak büyük avantaj sağlar:
# Dosya adını değiştirmek istersen tek bir yerden değiştirirsin.
# Büyük harfle yazılan değişkenler Python'da "sabit" anlamına gelir (convention).
# ─────────────────────────────────────────────────────────────
DB_DOSYASI = os.environ.get("DATABASE_PATH", "sofor_guvenlik.db")


# ─────────────────────────────────────────────────────────────
# YARDIMCI FONKSİYON: Şifre Hashleme
# ─────────────────────────────────────────────────────────────
def sifreyi_hashle(sifre: str) -> str:
    """
    📚 ÖĞRENME NOTU – Neden şifreyi hashlemeliyiz?
    Şifreyi veritabanına düz metin ('1234') olarak kaydetmek tehlikelidir.
    Biri veritabanını ele geçirirse tüm şifreleri görür.
    Hashlemek: '1234' → 'a665a4592...' gibi geri döndürülemez bir metne çevirir.
    SHA-256, endüstri standardı bir hash algoritmasıdır.
    """
    return hashlib.sha256(sifre.encode()).hexdigest()


# ─────────────────────────────────────────────────────────────
# FONKSİYON 1: Veritabanını ve Tabloları Oluştur
# ─────────────────────────────────────────────────────────────
def init_db():
    """
    Uygulama ilk çalıştığında bu fonksiyon çağrılır.
    Eğer tablolar yoksa oluşturur; varsa dokunmaz (IF NOT EXISTS sayesinde).

    📚 ÖĞRENME NOTU – sqlite3.connect() ne yapar?
    - 'sofor_guvenlik.db' adlı bir dosya oluşturur (veya açar).
    - Bu dosya projenin bulunduğu klasörde görünür, taşınabilir ve hafiftir.
    - conn = bağlantı nesnesi, cur = cursor (SQL komutlarını çalıştırır).
    """
    conn = sqlite3.connect(DB_DOSYASI)
    cur = conn.cursor()

    # ── TABLO 1: soforler ──────────────────────────────────
    # 📚 ÖĞRENME NOTU – SQL Veri Tipleri:
    #   INTEGER PRIMARY KEY AUTOINCREMENT → Her kayıda otomatik artan benzersiz numara
    #   TEXT                              → Metin (string) veri tipi
    #   UNIQUE                            → Bu sütunda aynı değer iki kez girilemesin
    cur.execute("""
        CREATE TABLE IF NOT EXISTS soforler (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            ad            TEXT NOT NULL,
            soyad         TEXT NOT NULL,
            kullanici_adi TEXT NOT NULL UNIQUE,
            arac_plaka    TEXT NOT NULL UNIQUE,
            sifre_hash    TEXT NOT NULL,
            sifre_plain   TEXT
        )
    """)

    # ── TABLO 2: alarmlar ─────────────────────────────────
    # 📚 ÖĞRENME NOTU – FOREIGN KEY (Yabancı Anahtar) Nedir?
    # sofor_id sütunu, soforler tablosunun id sütununa bağlıdır.
    # Bu ilişki sayesinde "bu alarm hangi şöföre ait?" sorusu cevaplanabilir.
    # Bu kavram Varlık-İlişki (ER) Diyagramlarının temelidir.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alarmlar (
            alarm_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            sofor_id    INTEGER NOT NULL,
            tarih_saat  TEXT NOT NULL,
            durum_bilgi TEXT,
            alarm_tipi  TEXT NOT NULL,
            FOREIGN KEY (sofor_id) REFERENCES soforler(id)
        )
    """)

    # ── TABLO 3: ses_loglari ──────────────────────────────
    # 📚 ÖĞRENME NOTU – Geçmiş Kayıtlarını Neden Ayrı Tutarız?
    # Alarmlar tablosu sadece "Acil Durumları" tutmalıdır.
    # Şoförün "İyiyim" gibi uyumlu cevaplarını loglamak için ayrı bir
    # tablo açmak veritabanının şişmesini engeller ve analizleri kolaylaştırır.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ses_loglari (
            log_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            sofor_id    INTEGER NOT NULL,
            tarih_saat  TEXT NOT NULL,
            metin       TEXT NOT NULL,
            analiz_sonucu TEXT,
            analiz_detay  TEXT,
            FOREIGN KEY (sofor_id) REFERENCES soforler(id)
        )
    """)

    # Geriye dönük uyumluluk için sütun ekleme kontrolü (eğer veritabanı zaten varsa)
    try:
        cur.execute("ALTER TABLE ses_loglari ADD COLUMN analiz_sonucu TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE ses_loglari ADD COLUMN analiz_detay TEXT")
    except sqlite3.OperationalError:
        pass


    # ── TABLO 4: vardiya_ses_kayitlari ────────────────────
    # Vardiya başı ve sonu ses kayıtlarını + analiz sonucunu saklar
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vardiya_ses_kayitlari (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            sofor_id        INTEGER NOT NULL,
            baslangic_metni TEXT,
            bitis_metni     TEXT,
            analiz_sonucu   TEXT NOT NULL,
            analiz_detay    TEXT,
            tarih_saat      TEXT NOT NULL,
            FOREIGN KEY (sofor_id) REFERENCES soforler(id)
        )
    """)

    # ── TABLO 5: yolcu_yorumlari ──────────────────────────
    # Yolcuların şoför ve araç hakkında bıraktığı geri bildirimler
    cur.execute("""
        CREATE TABLE IF NOT EXISTS yolcu_yorumlari (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            sofor_id      INTEGER NOT NULL,
            puan          INTEGER NOT NULL,
            etiketler     TEXT,
            serbest_yorum TEXT,
            tarih_saat    TEXT NOT NULL,
            FOREIGN KEY (sofor_id) REFERENCES soforler(id)
        )
    """)

    # ── TABLO 6: arac_konumlari ──────────────────────────
    # Araçların canlı GPS konumlarını saklar
    cur.execute("""
        CREATE TABLE IF NOT EXISTS arac_konumlari (
            sofor_id      INTEGER PRIMARY KEY,
            enlem         REAL NOT NULL,
            boylam        REAL NOT NULL,
            son_guncelleme TEXT NOT NULL,
            FOREIGN KEY (sofor_id) REFERENCES soforler(id)
        )
    """)

    conn.commit()   # Değişiklikleri diske kaydet
    conn.close()    # Bağlantıyı düzgünce kapat (kaynak sızıntısını önler)
    print("[OK] Veritabani basariyla hazirlandi.")


# ─────────────────────────────────────────────────────────────
# FONKSİYON 2: Şoför Ekle (Kayıt / Test Verisi için)
# ─────────────────────────────────────────────────────────────
def sofor_ekle(ad: str, soyad: str, kullanici_adi: str, plaka: str, sifre: str):
    """
    Veritabanına yeni bir şoför kaydı ekler.

    📚 ÖĞRENME NOTU – Parametre İşaretçisi (?)
    SQL sorgusuna değerleri doğrudan f-string ile yazmak tehlikelidir:
      ❌ f"INSERT INTO soforler VALUES ('{ad}'...)"   → SQL Injection açığı
      ✅ "INSERT INTO soforler VALUES (?...)", (ad,)  → Güvenli yöntem
    Soru işaretleri, Python tuple içindeki değerlerle güvenli biçimde eşleştirilir.
    """
    conn = sqlite3.connect(DB_DOSYASI)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO soforler (ad, soyad, kullanici_adi, arac_plaka, sifre_hash, sifre_plain) VALUES (?, ?, ?, ?, ?, ?)",
            (ad, soyad, kullanici_adi, plaka, sifreyi_hashle(sifre), sifre)
        )
        conn.commit()
        print(f"[OK] Sofor eklendi: {ad} {soyad} | Kullanıcı: {kullanici_adi} | Plaka: {plaka}")
    except sqlite3.IntegrityError:
        # UNIQUE kisitlamasi ihlali: Ayni plaka veya kullanici adi zaten kayitli demektir
        print(f"[UYARI] Kullanıcı adı '{kullanici_adi}' veya plaka '{plaka}' zaten sisteme kayıtlı.")
    finally:
        conn.close()  # Hata olsa da olmasa da bağlantıyı her zaman kapat


# ─────────────────────────────────────────────────────────────
# FONKSİYON 3: Giriş Doğrulama
# ─────────────────────────────────────────────────────────────
def sofor_dogrula(kullanici_adi: str, sifre: str):
    """
    Girilen kullanıcı adı ve şifre, veritabanıyla eşleşiyorsa şöför bilgilerini döner.
    Eşleşmiyorsa None döner.

    📚 ÖĞRENME NOTU – fetchone() ne yapar?
    - Sorgu sonucundan tek bir satır getirir.
    - Kayıt yoksa None (boş) döner.
    - Bunu kullanarak "giriş başarılı mı?" kontrolü yapabiliriz.

    📚 ÖĞRENME NOTU – conn.row_factory = sqlite3.Row
    Normalde SQLite sonuçlar tuple döner: (1, 'Ali', 'Yılmaz', ...)
    row_factory ayarı ile sözlük gibi erişim sağlanır: sofor['ad']
    Bu kod okunurluğunu büyük ölçüde artırır.
    """
    conn = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row   # Sonuçlara isimle erişimi etkinleştir
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM soforler WHERE kullanici_adi = ? AND sifre_hash = ?",
        (kullanici_adi, sifreyi_hashle(sifre))
    )
    sofor = cur.fetchone()
    conn.close()
    return sofor  # dict-benzeri nesne veya None


# ─────────────────────────────────────────────────────────────
# FONKSİYON 3b: Sadece Plaka ile Şöför Bul (Şifresiz Giriş)
# ─────────────────────────────────────────────────────────────
def sofor_plaka_ile_bul(plaka: str):
    """
    Yalnızca araç plakasıyla veritabanında şöför arar ve bulursa döner.
    Şifre kontrolü yapılmaz — bu uygulama için plaka yeterli kimlik kanıtıdır.

    📚 ÖĞRENME NOTU – Neden ayrı bir fonksiyon?
    sofor_dogrula() şifre de kontrol eder. Biz artık şifre istemediğimiz için
    yeni, daha sade bir fonksiyon yazdık. Bu sayede sofor_dogrula() bozulmadan
    kalır (ileride tekrar gerekirse kullanılabilir).
    Eski kodu silmek yerine yeni fonksiyon eklemek, iyi bir yazılım pratiğidir.
    """
    conn = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row  # Sonuçlara isimle erişimi etkinleştir
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM soforler WHERE arac_plaka = ?",
        (plaka,)   # Tek elemanlı tuple: virgül önemli!
    )
    sofor = cur.fetchone()
    conn.close()
    return sofor  # dict-benzeri nesne veya None


# ─────────────────────────────────────────────────────────────
# FONKSİYON 4: Alarm Oluştur (Panik Butonu / Yanıt Yok / Tehlike)
# ─────────────────────────────────────────────────────────────
def alarm_olustur(sofor_id: int, durum_bilgi: str = "ACİL DURUM - PANİK BUTONU BASILDI", alarm_tipi: str = "BUTON"):
    """
    Acil durum anında alarmlar tablosuna yeni kayıt ekler.
    "alarm_tipi" değişkeni sayesinde alarmın nereden tetiklendiği anlaşılır (Buton, Ses, Yanıtsız).
    """
    from datetime import datetime
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_DOSYASI)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alarmlar (sofor_id, tarih_saat, durum_bilgi, alarm_tipi) VALUES (?, ?, ?, ?)",
        (sofor_id, simdi, durum_bilgi, alarm_tipi)
    )
    conn.commit()
    conn.close()
    print(f"[ALARM] Alarm kaydedildi! Sofor ID: {sofor_id} | Zaman: {simdi} | Tipi: {alarm_tipi}")
    return simdi  


# ─────────────────────────────────────────────────────────────
# FONKSİYON 4b: Uyumlu Ses Kaydını Ekle
# ─────────────────────────────────────────────────────────────
def ses_logu_ekle(sofor_id: int, metin: str, analiz_sonucu: str = None, analiz_detay: str = None):
    """
    Şoförün "Nasılsınız?" sorusuna verdiği normal/sağlıklı yanıtları kaydeder.
    """
    from datetime import datetime
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_DOSYASI)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ses_loglari (sofor_id, tarih_saat, metin, analiz_sonucu, analiz_detay) VALUES (?, ?, ?, ?, ?)",
        (sofor_id, simdi, metin, analiz_sonucu, analiz_detay)
    )
    conn.commit()
    conn.close()



# ─────────────────────────────────────────────────────────────
# FONKSİYON 5: Tüm Alarmları Getir (Admin Paneli için)
# ─────────────────────────────────────────────────────────────
def tum_alarmlari_getir(sofor_id=None):
    """
    Admin panelindeki filtrelemeyi desteklemek için isteğe bağlı sofor_id alır.
    None verilirse tüm alarmları, ID verilirse sadece o şoförün alarmlarını getirir.
    """
    conn = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
        SELECT
            a.alarm_id,
            a.sofor_id,
            s.ad || ' ' || s.soyad  AS sofor_adi,
            s.arac_plaka,
            a.tarih_saat,
            a.alarm_tipi,
            a.durum_bilgi
        FROM alarmlar a
        INNER JOIN soforler s ON a.sofor_id = s.id
    """
    params = ()

    if sofor_id is not None:
        query += " WHERE a.sofor_id = ?"
        params = (sofor_id,)

    query += " ORDER BY a.alarm_id DESC"

    cur.execute(query, params)
    alarmlar = cur.fetchall()
    conn.close()
    return [dict(row) for row in alarmlar]


# ─────────────────────────────────────────────────────────────
# FONKSİYON 6: Tüm Ses Geçmişini Getir (Admin Paneli için)
# ─────────────────────────────────────────────────────────────
def tum_ses_loglarini_getir(sofor_id=None):
    """
    Filtrelemeye izin verecek şekilde şoförlerin ses yanıt (iyiyim) geçmişini çeker.
    """
    conn = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
        SELECT
            l.log_id,
            l.sofor_id,
            s.ad || ' ' || s.soyad  AS sofor_adi,
            l.tarih_saat,
            l.metin,
            l.analiz_sonucu,
            l.analiz_detay
        FROM ses_loglari l
        INNER JOIN soforler s ON l.sofor_id = s.id
    """
    params = ()
    
    if sofor_id is not None:
        query += " WHERE l.sofor_id = ?"
        params = (sofor_id,)

    query += " ORDER BY l.log_id DESC"

    cur.execute(query, params)
    loglar = cur.fetchall()
    conn.close()
    return [dict(row) for row in loglar]



# ─────────────────────────────────────────────────────────────
# FONKSİYON 7: Yorgunluk Analizi (Kural Tabanlı Algoritma)
# ─────────────────────────────────────────────────────────────
def yorgunluk_analizi_yap(baslangic_metni: str, bitis_metni: str, baslangic_suresi: float = 1.0, bitis_suresi: float = 1.0):
    """
    Vardiya başı ve sonu ses kayıtlarını karşılaştırarak yorgunluk analizi yapar.

    📚 ÖĞRENME NOTU – Konuşma Hızı (Ses Yorgunluğu) Analizi
    Makine öğrenmesi yerine, şoförün ses yorgunluğunu ölçmek için
    "Konuşma Hızı (Words Per Second)" kullanılır.
    İnsanlar yorulduklarında daha yavaş ve kesik kesik konuşurlar.
    Ayrıca tehlikeli anahtar kelimelere de bakılır.
    """
    yorgunluk_kelimeleri = [
        "yoruldum", "yorgun", "çok yoruldum", "bitik", "halsiz",
        "uyku", "uyuyakaldım", "uyukluyorum", "gözlerim kapanıyor",
        "baş ağrısı", "başım ağrıyor", "baş dönüyor",
        "mola istiyorum", "kötüyüm", "iyi değilim",
        "zor", "dayanamıyorum", "argın"
    ]

    bas_kelime  = len(baslangic_metni.split()) if baslangic_metni else 0
    bit_kelime  = len(bitis_metni.split())     if bitis_metni     else 0

    # Ses yorgunluğunu bulmak için saniyede kaç kelime konuştuğunu hesaplıyoruz
    bas_hiz = bas_kelime / baslangic_suresi if baslangic_suresi > 0 else 0
    bit_hiz = bit_kelime / bitis_suresi if bitis_suresi > 0 else 0

    tehlikeli   = any(k in bitis_metni.lower() for k in yorgunluk_kelimeleri)
    cok_kisa    = bit_kelime < 2
    
    # 1. Oransal Düşüş: Hız %25 veya daha fazla düştüyse
    oransal_yorgunluk = (bas_hiz > 0.5) and (bit_hiz < (bas_hiz * 0.75))
    
    # 2. Mutlak Yavaşlık: Genel konuşma hızı 0.8 kelime/saniyenin altındaysa (çok yavaş ve kesik kesik)
    mutlak_yorgunluk = (bit_hiz > 0) and (bit_hiz < 0.9)
    
    ses_yorgunlugu = oransal_yorgunluk or mutlak_yorgunluk

    if tehlikeli:
        return "KÖTÜ", f"⚠️ Tehlike ifadesi algılandı: '{bitis_metni[:60]}'"
    elif oransal_yorgunluk:
        return "KÖTÜ", f"⚠️ Konuşma hızınızda belirgin bir düşüş var ({bas_hiz:.1f} ➜ {bit_hiz:.1f} kelime/sn). Bu yorgunluk belirtisidir."
    elif mutlak_yorgunluk:
        return "KÖTÜ", f"⚠️ Konuşma hızınız çok yavaş ({bit_hiz:.1f} kelime/sn). Dikkat eksikliği ve yorgunluk riski yüksek."
    elif cok_kisa:
        return "KÖTÜ", f"⚠️ Vardiya sonu yanıtı çok kısa ({bit_kelime} kelime) — yorgunluk şüphesi."
    else:
        return "İYİ",  f"✅ Şoför dinç. Ses ritmi ve konuşma hızı normal (Başlangıç: {bas_hiz:.1f}, Bitiş: {bit_hiz:.1f} kelime/sn)."


# ─────────────────────────────────────────────────────────────
# FONKSİYON 7b: Periyodik Kontrol Yorgunluk & Risk Analiz Motoru
# ─────────────────────────────────────────────────────────────
def periyodik_yorgunluk_analizi_yap(sofor_id: int, metin: str):
    """
    10 dakikada bir yapılan periyodik asistan görüşmelerini,
    vardiya başlangıcı ve önceki periyodik kontrollerle kıyaslayarak analiz eder.
    """
    import re
    
    # 1. Metni ayrıştır ve temizle ("Soru 1: ... | Soru 2: ...")
    m = re.search(r"Soru 1:\s*(.*?)\s*\|\s*Soru 2:\s*(.*)", metin)
    if m:
        clean_text = m.group(1).strip() + " " + m.group(2).strip()
    else:
        clean_text = metin.strip()
        
    periyodik_kelime_sayisi = len(clean_text.split())
    
    # 2. Kelime bazlı yorgunluk / risk tespiti
    yorgunluk_kelimeleri = [
        "yoruldum", "yorgun", "çok yoruldum", "bitik", "halsiz",
        "uyku", "uyuyakaldım", "uyukluyorum", "gözlerim kapanıyor",
        "baş ağrısı", "başım ağrıyor", "baş dönüyor",
        "mola istiyorum", "kötüyüm", "iyi değilim",
        "zor", "dayanamıyorum", "argın", "halsizim", "bitkinim", "uykum"
    ]
    tehlikeli = any(k in clean_text.lower() for k in yorgunluk_kelimeleri)
    
    durum = "İYİ"
    detaylar = []
    detaylar.append("🔍 <b>PERİYODİK DURUM ANALİZ RAPORU</b>")
    detaylar.append(f"• Mevcut Periyodik Beyan: <i>\"{clean_text}\"</i> ({periyodik_kelime_sayisi} kelime)")
    
    if tehlikeli:
        durum = "KÖTÜ"
        detaylar.append("⚠️ <b>Risk Tespiti:</b> Konuşmada yorgunluk veya risk belirten anahtar kelimeler algılandı.")
        
    # 3. Vardiya Başlangıcı ile Karşılaştır
    conn = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute(
        "SELECT baslangic_metni FROM vardiya_ses_kayitlari WHERE sofor_id = ? ORDER BY id DESC LIMIT 1",
        (sofor_id,)
    )
    son_shift = cur.fetchone()
    
    if son_shift and son_shift["baslangic_metni"]:
        baslangic_metni = son_shift["baslangic_metni"]
        baslangic_kelime_sayisi = len(baslangic_metni.split())
        if baslangic_kelime_sayisi >= 3:
            oran = periyodik_kelime_sayisi / baslangic_kelime_sayisi
            detaylar.append(f"• Vardiya Giriş Raporu: <i>\"{baslangic_metni}\"</i> ({baslangic_kelime_sayisi} kelime) | Oran: <b>%{oran*100:.0f}</b>")
            if oran < 0.5:
                durum = "RİSKLİ"
                detaylar.append("⚠️ <b>Vardiya Girişine Göre Düşüş:</b> Konuşma uzunluğu vardiya başlangıcına kıyasla %50'den fazla azaldı! Odaklanma veya yorgunluk şüphesi.")
                
    # 4. Önceki Periyodik Kontrollerle Karşılaştır
    cur.execute(
        "SELECT metin FROM ses_loglari WHERE sofor_id = ? ORDER BY log_id DESC LIMIT 3",
        (sofor_id,)
    )
    gecmis_loglar = cur.fetchall()
    conn.close()
    
    prev_word_counts = []
    for log in gecmis_loglar:
        prev_metin = log["metin"]
        m_prev = re.search(r"Soru 1:\s*(.*?)\s*\|\s*Soru 2:\s*(.*)", prev_metin)
        prev_text = m_prev.group(1).strip() + " " + m_prev.group(2).strip() if m_prev else prev_metin.strip()
        prev_word_counts.append(len(prev_text.split()))
        
    if prev_word_counts:
        avg_prev = sum(prev_word_counts) / len(prev_word_counts)
        detaylar.append(f"• Önceki Periyodik Kayıtların Ortalama Kelime Sayısı: <b>{avg_prev:.1f}</b>")
        if avg_prev >= 3 and periyodik_kelime_sayisi < avg_prev * 0.5:
            # Eğer durum zaten KÖTÜ (keyword bulgusu) değilse, RİSKLİ yap
            if durum != "KÖTÜ":
                durum = "RİSKLİ"
            detaylar.append("📉 <b>Periyodik Düşüş Eğilimi:</b> Konuşma uzunluğu önceki periyodik kontrollere kıyasla %50'den fazla düştü! Enerji düşüklüğü ve uykusuzluk riski.")
            
    if durum == "İYİ":
        detaylar.append("✅ <b>Durum Stabil:</b> Şoförün konuşma ritmi ve uzunluğu standart seviyede. Yorgunluk saptanmadı.")
        
    return durum, "<br>".join(detaylar)


# ─────────────────────────────────────────────────────────────

# FONKSİYON 8: Vardiya Ses Kaydını Veritabanına Ekle
# ─────────────────────────────────────────────────────────────
def vardiya_ses_kaydet(sofor_id: int, baslangic_metni: str, bitis_metni: str,
                       analiz_sonucu: str, analiz_detay: str):
    """Vardiya başı/sonu ses metinlerini ve analiz sonucunu kaydeder."""
    from datetime import datetime
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_DOSYASI)
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO vardiya_ses_kayitlari
           (sofor_id, baslangic_metni, bitis_metni, analiz_sonucu, analiz_detay, tarih_saat)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (sofor_id, baslangic_metni, bitis_metni, analiz_sonucu, analiz_detay, simdi)
    )
    conn.commit()
    conn.close()
    print(f"[VARDİYA] Analiz kaydedildi: {analiz_sonucu} | Sofor ID: {sofor_id}")


# ─────────────────────────────────────────────────────────────
# FONKSİYON 9: Vardiya Kayıtlarını Getir (Admin için)
# ─────────────────────────────────────────────────────────────
def vardiya_kayitlarini_getir(sofor_id=None):
    """Admin paneli için vardiya ses analizi kayıtlarını getirir."""
    conn  = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cur   = conn.cursor()
    query = """
        SELECT
            v.id,
            v.sofor_id,
            s.ad || ' ' || s.soyad AS sofor_adi,
            s.arac_plaka,
            v.baslangic_metni,
            v.bitis_metni,
            v.analiz_sonucu,
            v.analiz_detay,
            v.tarih_saat
        FROM vardiya_ses_kayitlari v
        INNER JOIN soforler s ON v.sofor_id = s.id
    """
    params = ()
    if sofor_id is not None:
        query  += " WHERE v.sofor_id = ?"
        params  = (sofor_id,)
    query += " ORDER BY v.id DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────
# FONKSİYON 10: Yolcu Yorumu Ekle
# ─────────────────────────────────────────────────────────────
def yolcu_yorumu_ekle(sofor_id: int, puan: int, etiketler: str, serbest_yorum: str):
    """Yolcunun bıraktığı geri bildirimi veritabanına kaydeder."""
    from datetime import datetime
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn  = sqlite3.connect(DB_DOSYASI)
    cur   = conn.cursor()
    cur.execute(
        """INSERT INTO yolcu_yorumlari
           (sofor_id, puan, etiketler, serbest_yorum, tarih_saat)
           VALUES (?, ?, ?, ?, ?)""",
        (sofor_id, puan, etiketler, serbest_yorum, simdi)
    )
    conn.commit()
    conn.close()
    print(f"[YORUM] Yolcu yorumu eklendi | Sofor ID: {sofor_id} | Puan: {puan}")


# ─────────────────────────────────────────────────────────────
# FONKSİYON 11: Yolcu Yorumlarını Getir (Admin için)
# ─────────────────────────────────────────────────────────────
def yolcu_yorumlarini_getir(sofor_id=None):
    """Admin paneli için yolcu geri bildirimlerini getirir."""
    conn  = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cur   = conn.cursor()
    query = """
        SELECT
            y.id,
            y.sofor_id,
            s.ad || ' ' || s.soyad AS sofor_adi,
            s.arac_plaka,
            y.puan,
            y.etiketler,
            y.serbest_yorum,
            y.tarih_saat
        FROM yolcu_yorumlari y
        INNER JOIN soforler s ON y.sofor_id = s.id
    """
    params = ()
    if sofor_id is not None:
        query  += " WHERE y.sofor_id = ?"
        params  = (sofor_id,)
    query += " ORDER BY y.id DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────
# FONKSİYON 12: GPS Konumu Güncelle
# ─────────────────────────────────────────────────────────────
def konum_guncelle(sofor_id: int, enlem: float, boylam: float):
    """Şoförün anlık GPS konumunu veritabanına kaydeder/günceller."""
    from datetime import datetime
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn  = sqlite3.connect(DB_DOSYASI)
    cur   = conn.cursor()
    cur.execute(
        """INSERT OR REPLACE INTO arac_konumlari
           (sofor_id, enlem, boylam, son_guncelleme)
           VALUES (?, ?, ?, ?)""",
        (sofor_id, enlem, boylam, simdi)
    )
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────────
# FONKSİYON 13: Tüm Canlı Konumları Getir (Admin Haritası)
# ─────────────────────────────────────────────────────────────
def tum_konumlari_getir():
    """Haritada göstermek üzere aktif araçların son konumlarını çeker."""
    conn  = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cur   = conn.cursor()
    cur.execute("""
        SELECT
            k.sofor_id,
            s.ad || ' ' || s.soyad AS sofor_adi,
            s.arac_plaka,
            s.kullanici_adi AS kadi,
            s.sifre_plain AS sifre,
            k.enlem,
            k.boylam,
            k.son_guncelleme
        FROM arac_konumlari k
        INNER JOIN soforler s ON k.sofor_id = s.id
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def tum_soforleri_getir():
    """Tüm kayıtlı şoförleri giriş bilgileriyle birlikte getirir."""
    conn  = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cur   = conn.cursor()
    cur.execute("SELECT id as sofor_id, ad || ' ' || soyad as sofor_adi, kullanici_adi as kadi, arac_plaka as plaka, sifre_plain as sifre FROM soforler")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────
# 📚 ÖĞRENME NOTU – if __name__ == "__main__" Bloğu
# Bu blok YALNIZCA bu dosya doğrudan çalıştırıldığında çalışır.
# Örneğin: python database.py → çalışır
# Fakat app.py import ettiğinde → çalışmaz
# Bu yapı modülleri hem bağımsız test edilebilir hem de import edilebilir kılar.
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("--- Veritabani kurulum ve test basliyor ---")
    init_db()

    sofor_ekle("Ahmet", "Yilmaz", "ahmet", "34 ABC 001", "sifre123")
    sofor_ekle("Mehmet", "Kaya", "mehmet", "06 XYZ 999", "sifre456")
    sofor_ekle("Fatma",  "Demir", "fatma", "35 DEF 777", "sifre789")
    sofor_ekle("Can",  "Yıldız", "can", "34 CAN 34", "can123")

    print("\n--- Giris dogrulama testi ---")
    sofor = sofor_dogrula("ahmet", "sifre123")
    if sofor:
        print(f"[OK] Giris basarili: {sofor['ad']} {sofor['soyad']}")
    else:
        print("[HATA] Giris basarisiz!")

    print("\n--- Alarm olusturma testi ---")
    alarm_olustur(sofor_id=1)

    print("\n--- Tum alarmlar ---")
    for alarm in tum_alarmlari_getir():
        print(alarm)

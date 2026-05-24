"""
=============================================================
 DOSYA: app.py
 AMAÇ : Streamlit ile kullanıcı arayüzü (Frontend Layer)
-------------------------------------------------------------
 📚 ÖĞRENME NOTU – Streamlit Nedir?
 Streamlit, Python kodu yazarak web arayüzü oluşturmana izin veren
 bir kütüphanedir. HTML, CSS veya JavaScript bilmene gerek yok!
 Her st.button(), st.text_input() gibi fonksiyon çağrısı otomatik
 olarak ekranda bir bileşen (component) oluşturur.

 Çalıştırmak için terminale yaz:
   streamlit run app.py
=============================================================
"""

import streamlit as st  # Web arayüzü kütüphanesi
import pandas as pd      # Tabloları güzel göstermek için (DataFrame)

# Kendi yazdığımız database modülünü import ediyoruz
# 📚 Böylece veritabanı fonksiyonlarını burada tekrar yazmak zorunda kalmıyoruz
import database as db


# ─────────────────────────────────────────────────────────────
# SAYFA AYARLARI
# ─────────────────────────────────────────────────────────────
# 📚 ÖĞRENME NOTU – st.set_page_config()
# Bu fonksiyon sayfanın tarayıcı sekmesindeki başlığını,
# ikonunu ve düzenini ayarlar. Her zaman kodun EN BAŞINDA çağrılmalıdır.
st.set_page_config(
    page_title="Şoför Güvenlik Sistemi",
    page_icon="🚨",
    layout="centered"
)


# ─────────────────────────────────────────────────────────────
# UYGULAMA BAŞLANGICI: Veritabanını Hazırla
# ─────────────────────────────────────────────────────────────
# 📚 ÖĞRENME NOTU – Neden burada çağırıyoruz?
# app.py her çalıştığında (ve her sayfa yenilendiğinde) bu satır çalışır.
# init_db() içindeki "IF NOT EXISTS" sayesinde tablolar zaten varsa
# tekrar oluşturulmaz; yani bu çağrı güvenlidir.
db.init_db()

# Test şoförlerini ekle (sadece kayıt yoksa ekler, varsa atlar)
db.sofor_ekle("Ahmet",  "Yılmaz", "ahmet", "34 ABC 001", "sifre123")
db.sofor_ekle("Mehmet", "Kaya",   "mehmet", "06 XYZ 999", "sifre456")
db.sofor_ekle("Fatma",  "Demir",  "fatma", "35 DEF 777", "sifre789")
db.sofor_ekle("Ali",    "Yıldız", "ali", "06 GBT 111", "sifre111")
db.sofor_ekle("Ayşe",   "Çelik",  "ayse", "34 MNO 222", "sifre222")
db.sofor_ekle("Mustafa","Şahin",  "mustafa", "16 BUR 333", "sifre333")
db.sofor_ekle("Zeynep", "Koç",    "zeynep", "35 IZM 444", "sifre444")
db.sofor_ekle("Hasan",  "Turan",  "hasan", "01 ADA 555", "sifre555")


# ─────────────────────────────────────────────────────────────
# SESSION STATE KURULUMU
# ─────────────────────────────────────────────────────────────
# 📚 ÖĞRENME NOTU – st.session_state Nedir?
# Streamlit'in en önemli özelliklerinden biridir.
# Normalde bir butona tıkladığında Streamlit tüm sayfayı baştan çalıştırır.
# Bu da "giriş yaptım" bilgisinin kaybolması demektir.
# session_state, sayfa yenilenmeleri arasında bilgiyi HAFIZADA tutar.
# Tıpkı bir web uygulamasındaki "oturum" (session) gibi çalışır.

if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False  # Kullanıcı giriş yapmadı

if "aktif_sofor" not in st.session_state:
    st.session_state.aktif_sofor = None    # Giriş yapan şöförün verisi yok


# ═══════════════════════════════════════════════════════════════
# EKRAN 1: GİRİŞ EKRANI (LOGIN)
# Kullanıcı giriş yapmamışsa bu ekran gösterilir
# ═══════════════════════════════════════════════════════════════
def giris_ekrani():
    """
    📚 ÖĞRENME NOTU – st.tabs() ile Sekmeli Arayüz
    st.tabs() birden fazla içeriği sekmeler halinde gösterir.
    Kullanıcı sekmeye tıklayınca yalnızca o sekmenin içeriği görünür.
    Bu sayede şoför ve admin girişlerini tamamen birbirinden ayırıyoruz.
    """
    st.title("🚌 Şoför Güvenlik Sistemi")
    st.markdown("---")

    # 📚 st.tabs() → 3 sekmeye ayırdık: Yolcu, Şoför, Admin
    sekme_yolcu, sekme_sofor, sekme_admin = st.tabs(["💺 Yolcu Girişi", "🚗 Şoför Girişi", "🔐 Admin Girişi"])

    # ── SEKME 1: YOLCU GİRİŞİ (Eski Şoför Paneli) ───────────
    with sekme_yolcu:
        st.subheader("Yolcu Girişi")
        st.caption("Seyahat ettiğiniz otobüsü sadece plaka ile takip edin ve acil durum bildirin.")
        st.markdown(" ")

        yolcu_plaka = st.text_input(
            label="Araç Plakası",
            placeholder="Örn: 34 ABC 001",
            key="yolcu_plaka_input",
            help="Kayıtlı araç plakasını büyük harfle girin"
        )

        if st.button("Giriş Yap", use_container_width=True, type="primary", key="yolcu_giris_btn"):
            if not yolcu_plaka.strip():
                st.warning("⚠️ Lütfen araç plakasını girin.")
            else:
                sofor = db.sofor_plaka_ile_bul(yolcu_plaka.strip())
                if sofor:
                    st.session_state.giris_yapildi = True
                    st.session_state.aktif_sofor = dict(sofor)
                    st.session_state.aktif_sofor["rol"] = "yolcu"
                    st.rerun()
                else:
                    st.error("❌ Bu plaka sistemde kayıtlı değil!")

        # Yardımcı bilgi kutusu
        with st.expander("ℹ️ Kayıtlı Otobüs Plakaları"):
            st.markdown("""
            | Plaka | Şoför Adı |
            |-------|-----------|
            | 34 ABC 001 | Ahmet Yılmaz |
            | 06 XYZ 999 | Mehmet Kaya |
            | 35 DEF 777 | Fatma Demir |
            | 06 GBT 111 | Ali Yıldız |
            | 34 MNO 222 | Ayşe Çelik |
            | 16 BUR 333 | Mustafa Şahin |
            | 35 IZM 444 | Zeynep Koç |
            | 01 ADA 555 | Hasan Turan |
            """)

    # ── SEKME 2: ŞOFÖR GİRİŞİ ───────────────────────────────
    with sekme_sofor:
        st.subheader("Şoför Girişi")
        st.caption("Güvenli sürüş için kimlik doğrulama gereklidir.")
        st.markdown(" ")

        # Şoför için Kullanıcı Adı + Şifre
        sofor_kadi = st.text_input(label="Kullanıcı Adı", placeholder="Örn: ahmet", key="sofor_login_kadi")
        sofor_sifre = st.text_input(label="Şifre", type="password", placeholder="••••••••", key="sofor_login_sifre")

        if st.button("Şoför Paneline Gir", use_container_width=True, type="primary", key="sofor_auth_btn"):
            if not sofor_kadi.strip() or not sofor_sifre.strip():
                st.warning("⚠️ Kullanıcı adı ve şifreyi doldurun.")
            else:
                sofor = db.sofor_dogrula(sofor_kadi.strip().lower(), sofor_sifre.strip())
                if sofor:
                    st.session_state.giris_yapildi = True
                    st.session_state.aktif_sofor = dict(sofor)
                    st.session_state.aktif_sofor["rol"] = "sofor"
                    # Döngü mantığı için temizlik yapalım
                    st.session_state.anket_asamasi = 0
                    st.session_state.son_tetiklenme = None
                    st.rerun()
                else:
                    st.error("❌ Kullanıcı adı veya şifre hatalı!")
        
        with st.expander("ℹ️ Şoför Giriş Bilgileri"):
            st.markdown("""
            **Tüm Kayıtlı Şoför Hesapları:**
            
            | Kullanıcı Adı | Şifre | Şoför Adı |
            |--------------|-------|-----------|
            | `ahmet` | `sifre123` | Ahmet Yılmaz |
            | `mehmet` | `sifre456` | Mehmet Kaya |
            | `fatma` | `sifre789` | Fatma Demir |
            | `ali` | `sifre111` | Ali Yıldız |
            | `ayse` | `sifre222` | Ayşe Çelik |
            | `mustafa` | `sifre333` | Mustafa Şahin |
            | `zeynep` | `sifre444` | Zeynep Koç |
            | `hasan` | `sifre555` | Hasan Turan |
            """)

    # ── SEKME 3: ADMİN GİRİŞİ ───────────────────────────────
    with sekme_admin:
        st.subheader("Admin / Merkez Girişi")
        st.caption("Bu panel yalnızca yetkili merkez personeline aittir.")
        st.markdown(" ")

        # Admin için kullanıcı adı + şifre alanları
        # 📚 Her input'a farklı key= verilmesi önemli!
        # Aynı sayfada iki input aynı ismi taşıyamazsa çakışma çıkar.
        admin_kullanici = st.text_input(
            label="Kullanıcı Adı",
            placeholder="admin",
            key="admin_kullanici_input"
        )
        admin_sifre = st.text_input(
            label="Şifre",
            type="password",
            placeholder="••••••••",
            key="admin_sifre_input"
        )

        if st.button("Admin Olarak Giriş Yap", use_container_width=True, type="primary", key="admin_giris_btn"):
            if not admin_kullanici.strip() or not admin_sifre.strip():
                st.warning("⚠️ Kullanıcı adı ve şifreyi doldurun.")
            # 📚 ÖĞRENME NOTU: Gerçek projede admin bilgileri de veritabanında olur.
            # Bu prototipin sade tutulması için sabit değer kontrolü yeterlidir.
            elif admin_kullanici.strip() == "admin" and admin_sifre == "admin123":
                st.session_state.giris_yapildi = True
                st.session_state.aktif_sofor = {"rol": "admin"}
                st.rerun()
            else:
                st.error("❌ Kullanıcı adı veya şifre hatalı!")

        with st.expander("ℹ️ Admin Giriş Bilgisi"):
            st.markdown("""
            **Kullanıcı Adı:** `admin`  
            **Şifre:** `admin123`
            """)


# ═══════════════════════════════════════════════════════════════
# EKRAN 2: YOLCU PANELİ (Eski Şoför Paneli)
# ═══════════════════════════════════════════════════════════════
def yolcu_paneli():
    """
    Yalnızca plaka ile giriş yapan yolcu/gözlemci paneli.
    Sadece basit panik butonuna sahiptir, ses analizi vb. içermez.
    """
    sofor = st.session_state.aktif_sofor
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title("🛡️ Yolcu Acil Durum Paneli")
        st.subheader(f" Aktif Araç : {sofor['arac_plaka']}")
    with col2:
        if st.button("🚪 Çıkış Yap", use_container_width=True):
            st.session_state.giris_yapildi = False
            st.session_state.aktif_sofor = None
            st.rerun()

    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(label="👤 Şoför Adı", value=f"{sofor['ad']} {sofor['soyad']}")
    with col_b:
        st.metric(label="🚌 Araç Plakası", value=sofor['arac_plaka'])
    with col_c:
        st.metric(label="🆔 Şoför ID", value=sofor['id'])

    st.markdown("---")
    st.markdown("## 🚨 Acil Durum")
    
    st.markdown("""
    <style>
        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #CC0000;
            color: white;
            font-size: 28px;
            font-weight: bold;
            height: 120px;
            border-radius: 16px;
            border: 4px solid #990000;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("🚨 PANİK BUTONU 🚨", type="primary", use_container_width=True):
        alarm_zamani = db.alarm_olustur(
            sofor_id=sofor['id'],
            durum_bilgi=f"ACİL DURUM | Plaka: {sofor['arac_plaka']} | Yolcu Tarafından PANİK Butonu Basıldı",
            alarm_tipi="YOLCU_PANIK"
        )
        st.success(f"✅ Alarm Merkeze İletildi! (Zaman: {alarm_zamani})")

    st.markdown(" ") # Boşluk
    if st.button("🚌 Fazla Yolcu / Kalabalık Şikayeti Bildir", use_container_width=True):
        alarm_zamani = db.alarm_olustur(
            sofor_id=sofor['id'],
            durum_bilgi=f"ŞİKAYET | Plaka: {sofor['arac_plaka']} | Otobüse Kapasite Üstü (Aşırı) Yolcu Alındı",
            alarm_tipi="FAZLA_YOLCU"
        )
        st.warning(f"⚠️ Şikayetiniz merkeze iletilmiştir. Teşekkür ederiz! ({alarm_zamani})")

    st.markdown("---")
    st.markdown("## ⭐ Sürüş Geri Bildirimi")
    st.caption("Görüşleriniz hizmet kalitemizi artırmak için önemlidir.")

    with st.form("yolcu_yorum_formu"):
        puan = st.slider("Genel Değerlendirme Puanınız", 1, 5, 5, help="1: Çok Kötü, 5: Çok İyi")
        
        etiket_secenekleri = ["Sakin Sürüş", "Hızlı Kullanım", "Kaba Davranış", "Kibar Şoför", "Araç Temiz", "Araç Bakımsız", "Fazla Yolcu (Ayakta)"]
        secilen_etiketler = st.multiselect("Etiketler (Birden fazla seçebilirsiniz)", etiket_secenekleri)
        
        serbest_yorum = st.text_area("Eklemek istedikleriniz (İsteğe bağlı)", placeholder="Şoför çok nazikti, ancak araç biraz soğuktu...")
        
        gonder_btn = st.form_submit_button("Geri Bildirimi Gönder", type="primary")
        
        if gonder_btn:
            etiketler_str = ", ".join(secilen_etiketler)
            db.yolcu_yorumu_ekle(sofor['id'], puan, etiketler_str, serbest_yorum)
            st.success("✅ Geri bildiriminiz başarıyla kaydedildi. Teşekkür ederiz!")


# ═══════════════════════════════════════════════════════════════
# EKRAN 3: ŞOFÖR GÜVENLİK PANELİ (STATE MACHINE MANTIKLI)
# ═══════════════════════════════════════════════════════════════
import time

def sesli_sor(metin):
    """Metni sese çevirir ve Streamlit üzerinde otomatik çalar."""
    from gtts import gTTS
    import base64
    import tempfile
    try:
        tts = gTTS(text=metin, lang='tr')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            with open(fp.name, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f'''
                    <audio autoplay="true">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    '''
                st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.warning("Sesli okuma modülü çalıştırılamadı.")

def sofor_paneli():
    sofor = st.session_state.aktif_sofor
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title("🛡️ Sürüş Güvenlik Paneli (Şoför)")
        st.subheader(f" Hoşgeldin {sofor['ad']} {sofor['soyad']}")
    with col2:
        if st.button("🚪 Çıkış Yap", use_container_width=True, key="sofor_logout"):
            st.session_state.giris_yapildi = False
            st.session_state.aktif_sofor = None
            st.rerun()

    st.markdown("---")
    
    # ── OTOMATİK KONTROL MANTIĞI (10 DAKİKADA BİR) ──
    if "son_otomatik_kontrol" not in st.session_state:
        st.session_state.son_otomatik_kontrol = time.time()

    simdi = time.time()
    # 10 dakika = 600 saniye.
    if (simdi - st.session_state.son_otomatik_kontrol) > 600:
        if st.session_state.anket_asamasi == 0:
            st.session_state.anket_asamasi = "otomatik_dinleme"
            st.session_state.son_tetiklenme = simdi
            st.session_state.son_otomatik_kontrol = simdi
            st.rerun()

    # ── KONUM BİLGİSİ ──
    konumlar = ["Bilinmiyor", "Ana Kampüs", "Şehir Merkezi", "Otogar", "AŞTİ"]
    secilen_konum = st.selectbox("📍 Mevcut Konumunuz:", konumlar)
    
    # Seçilen konuma göre sanal GPS koordinatları belirle ve veritabanına kaydet
    konum_koordinatlari = {
        "Ana Kampüs": (39.9382, 32.8223),
        "Şehir Merkezi": (39.9208, 32.8541),
        "Otogar": (39.9180, 32.8120),
        "AŞTİ": (39.9180, 32.8120)
    }
    
    if secilen_konum in konum_koordinatlari:
        enlem, boylam = konum_koordinatlari[secilen_konum]
        db.konum_guncelle(sofor['id'], enlem, boylam)

    # Asıl Panik Butonu
    if st.button("🚨 MANUEL PANİK BUTONU 🚨", use_container_width=True):
        alarm_zamani = db.alarm_olustur(
            sofor_id=sofor['id'],
            durum_bilgi=f"ACİL DURUM | Konum: {secilen_konum}",
            alarm_tipi="MANUEL_BUTON"
        )
        st.success(f"✅ Merkeze iletildi! ({alarm_zamani})")

    st.markdown("---")
    st.markdown("### 🎙️ Vardiya Ses Analizi (Yorgunluk Takibi)")
    st.info("Vardiya başında ve sonunda ses kaydı vererek yorgunluk durumunuzu ölçün.")
    
    if "vardiya_basi_metin" not in st.session_state:
        st.session_state.vardiya_basi_metin = None
    if "vardiya_basi_sure" not in st.session_state:
        st.session_state.vardiya_basi_sure = 1.0

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("🟢 Vardiya Başı Ses Kaydı Al", use_container_width=True):
            sesli_sor("Vardiyanıza hoş geldiniz. Nasılsınız? Kendinizi nasıl hissediyorsunuz?")
            st.info("⌛ Bot konuşuyor, lütfen bekleyin...")
            time.sleep(5) # Botun cümlesini bitirmesi için süre tanıyoruz
            st.info("🎤 Dinleniyor... (Lütfen konuşun)")
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            recognizer.pause_threshold = 2.5 # Kullanıcının duraksamalarını tolere et (Daha uzun bekle)
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    # phrase_time_limit KALDIRILDI: Cümle bitene kadar bekler
                    audio_data = recognizer.listen(source, timeout=12, phrase_time_limit=None)
                text = recognizer.recognize_google(audio_data, language="tr-TR").lower()
                st.session_state.vardiya_basi_metin = text
                
                # Sesi saniye cinsinden hesapla
                ham_sure = len(audio_data.frame_data) / (audio_data.sample_width * audio_data.sample_rate)
                # Sessizlik payını çıkararak net konuşma süresini buluyoruz
                sure = max(1.0, ham_sure - recognizer.pause_threshold)
                st.session_state.vardiya_basi_sure = sure
                
                st.success(f"✅ Başlangıç kaydedildi: *{text}* (Net Süre: {sure:.1f} sn)")
            except sr.UnknownValueError:
                st.error("Hata: Sesiniz duyuldu fakat anlaşılamadı (Kelimeler seçilemedi). Lütfen daha net konuşun.")
            except sr.WaitTimeoutError:
                st.error("Hata: Hiç ses duyulmadı (Zaman aşımı). Mikrofonunuzu kontrol edin.")
            except sr.RequestError as e:
                st.error(f"Hata: Google Ses API'sine ulaşılamadı. İnternet bağlantınızı kontrol edin. Detay: {e}")
            except Exception as e:
                st.error(f"Beklenmeyen bir hata oluştu: {e}")

    with col_v2:
        if st.button("🔴 Vardiya Sonu Analizi Yap", use_container_width=True):
            if not st.session_state.vardiya_basi_metin:
                st.warning("⚠️ Önce Vardiya Başı kaydı almalısınız!")
            else:
                sesli_sor("Vardiyanız bitti. Geçmiş olsun. Şu an kendinizi nasıl hissediyorsunuz?")
                st.info("⌛ Bot konuşuyor, lütfen bekleyin...")
                time.sleep(5)
                st.info("🎤 Dinleniyor... (Lütfen konuşun)")
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                recognizer.pause_threshold = 2.5
                try:
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        # Cümle bitene kadar bekler
                        audio_data = recognizer.listen(source, timeout=12, phrase_time_limit=None)
                    bitis_metni = recognizer.recognize_google(audio_data, language="tr-TR").lower()
                    
                    # Sesi saniye cinsinden hesapla
                    ham_suresi = len(audio_data.frame_data) / (audio_data.sample_width * audio_data.sample_rate)
                    bitis_suresi = max(1.0, ham_suresi - recognizer.pause_threshold)
                    
                    st.write(f"🗣️ Bitiş Cümlesi: *{bitis_metni}* (Net Süre: {bitis_suresi:.1f} sn)")
                    
                    # Analizi çalıştır (Konuşma Hızı analizi dahil)
                    durum, detay = db.yorgunluk_analizi_yap(
                        st.session_state.vardiya_basi_metin, 
                        bitis_metni, 
                        st.session_state.vardiya_basi_sure, 
                        bitis_suresi
                    )
                    
                    if durum == "KÖTÜ":
                        st.error(f"🚨 Analiz Sonucu: KÖTÜ\n\nDetay: {detay}")
                    else:
                        st.success(f"✅ Analiz Sonucu: İYİ\n\nDetay: {detay}")
                        
                    db.vardiya_ses_kaydet(sofor['id'], st.session_state.vardiya_basi_metin, bitis_metni, durum, detay)
                    
                    # Sıfırla
                    st.session_state.vardiya_basi_metin = None
                    st.session_state.vardiya_basi_sure = 1.0
                except sr.UnknownValueError:
                    st.error("Hata: Sesiniz duyuldu fakat anlaşılamadı (Kelimeler seçilemedi). Lütfen daha net konuşun.")
                except sr.WaitTimeoutError:
                    st.error("Hata: Hiç ses duyulmadı (Zaman aşımı). Mikrofonunuzu kontrol edin.")
                except sr.RequestError as e:
                    st.error(f"Hata: Google Ses API'sine ulaşılamadı. İnternet bağlantınızı kontrol edin. Detay: {e}")
                except Exception as e:
                    st.error(f"Beklenmeyen bir hata oluştu: {e}")

    st.markdown("---")
    st.markdown("### 🎙️ Akıllı Ses Asistanı (Yorgunluk & Tepki Kontrolü)")

    # 📚 ÖĞRENME NOTU - STATE MACHINE (DURUM MAKİNESİ)
    # Streamlit senkron(sıralı) çalışır, eğer time.sleep() yazarsak tüm ekran donar.
    # O yüzden session_state kullanarak ne aşamada olduğumuzu hatırlıyoruz 
    # ve arayüzü st.rerun() ile yenileyerek asenkron gibi gösteriyoruz.

    if "anket_asamasi" not in st.session_state:
        st.session_state.anket_asamasi = 0  # 0: Kapalı, "otomatik_dinleme": Ses dinleniyor, 2: Yanıtsızlık Alarmı
        st.session_state.son_tetiklenme = None

    if st.session_state.anket_asamasi == 0:
        if st.button("▶️ Mikrofon Kontrolünü Başlat", type="primary"):
            st.session_state.anket_asamasi = "otomatik_dinleme"
            st.session_state.son_tetiklenme = time.time()
            st.session_state.son_otomatik_kontrol = time.time()
            st.rerun()
    
    elif st.session_state.anket_asamasi == "otomatik_dinleme":
        # Bot sesli sorusunu burada soruyor, böylece sayfa yenilenmesi sesi kesmiyor
        sesli_sor("Sayın şoförümüz, nasılsınız? Bir sorun var mı?")
        st.info("🔄 Otomatik Kontrol Aktif - Bot konuşuyor, lütfen bekleyin...")
        time.sleep(6) # Botun konuşması için yeterli süre
        
        # Şoförün sesini otomatik dinle (Buton gerektirmez)
        st.info("🎤 Dinleniyor... (Lütfen yanıt verin)")
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 2.5 # Duraksamalarda hemen kesmesin
        
        hata_mesaji = None
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                # Cümle bitene kadar bekler (phrase_time_limit=None)
                audio_data = recognizer.listen(source, timeout=12, phrase_time_limit=None)
            text = recognizer.recognize_google(audio_data, language="tr-TR").lower()
            
            st.write(f"🗣️ Algılanan Cümle: *{text}*")
            
            durum, detay = db.periyodik_yorgunluk_analizi_yap(sofor['id'], text)
            clean_detay = detay.replace('<br>', '\n')
            if durum in ["KÖTÜ", "RİSKLİ"]:
                db.alarm_olustur(sofor['id'], f"SESLİ TEHLİKE ({durum}) | Metin: {text}", "SES_ANALİZ")
                db.ses_logu_ekle(sofor['id'], text, durum, detay)
                st.error(f"🚨 Tehlike/Risk Saptandı ({durum}). Alarm Geçildi!\n\nDetay: {clean_detay}")
            else:
                db.ses_logu_ekle(sofor['id'], text, durum, detay)
                st.success(f"✅ Uyumlu yanıt merkeze kaydedildi.\n\nDetay: {clean_detay}")

                
            # Başarılı yanıt sonrası döngüyü kapat
            st.session_state.anket_asamasi = 0
            time.sleep(3)
            st.rerun()
            
        except sr.UnknownValueError:
            hata_mesaji = "Sesiniz duyuldu fakat anlaşılamadı (Kelimeler seçilemedi)."
        except sr.WaitTimeoutError:
            hata_mesaji = "Hiç ses duyulmadı (Zaman aşımı)."
        except sr.RequestError as e:
            hata_mesaji = f"Google API Bağlantı Hatası: {e}"
        except Exception as e:
            hata_mesaji = f"Beklenmeyen hata: {e}"
            
        if hata_mesaji:
            st.warning(f"⚠️ {hata_mesaji} Döngü aşama 2'ye (Kritik) geçiyor.")
            st.session_state.anket_asamasi = 2
            st.session_state.son_tetiklenme = time.time()
            time.sleep(4)
            st.rerun()

    elif st.session_state.anket_asamasi == 2:
        # KRİTİK ALARM MANTIĞI (Yanıt alınamadı)
        db.alarm_olustur(sofor['id'], "KRİTİK: Şoförden Yanıt Alınamadı!", "YANITSIZLIK_ALARM")
        st.session_state.anket_asamasi = 0
        st.error("🚨 Yanıt Alınamadı! Sisteme KRİTİK ALARM Gönderildi!")
        time.sleep(3)
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# EKRAN 4: ADMİN PANELİ
# ═══════════════════════════════════════════════════════════════
def admin_paneli():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📡 Merkez Kontrol Paneli")
    with col2:
        if st.button("🚪 Çıkış Yap", use_container_width=True):
            st.session_state.giris_yapildi = False
            st.session_state.aktif_sofor = None
            st.rerun()
    st.markdown("---")

    import sqlite3
    # ── ALARM TABLOSU VE ŞOFÖR FİLTRESİ ──
    # Benzersiz şoför listesini çekelim ki menüden seçilebilsin
    conn = sqlite3.connect(db.DB_DOSYASI)
    cur = conn.cursor()
    cur.execute("SELECT id, ad, soyad FROM soforler")
    soforler_listesi = cur.fetchall()
    conn.close()

    secenekler = {"Tümü": None}
    for s_id, ad, soyad in soforler_listesi:
        secenekler[f"{ad} {soyad} (ID:{s_id})"] = s_id

    secilen_sofor_metni = st.selectbox("🔍 Verileri Şoföre Göre Filtrele:", list(secenekler.keys()))
    hedef_id = secenekler[secilen_sofor_metni]

    alarmlar = db.tum_alarmlari_getir(sofor_id=hedef_id)
    ses_loglar = db.tum_ses_loglarini_getir(sofor_id=hedef_id)
    vardiya_kayitlari = db.vardiya_kayitlarini_getir(sofor_id=hedef_id)
    yolcu_yorumlari = db.yolcu_yorumlarini_getir(sofor_id=hedef_id)

    sekme_alarmlar, sekme_sesler, sekme_vardiya, sekme_yorumlar, sekme_harita = st.tabs([
        "🔴 Acil Durum Alarmları", 
        "📜 Ses Geçmişi", 
        "🎙️ Vardiya Analizi", 
        "💬 Yolcu Yorumları",
        "🗺️ Canlı Harita"
    ])

    with sekme_alarmlar:
        if not alarmlar:
            st.info("📭 Bu kriterde alarm bulunmuyor.")
        else:
            df = pd.DataFrame(alarmlar)
            df = df.rename(columns={"alarm_id": "Alarm No", "sofor_adi": "Şoför Adı", "arac_plaka": "Plaka", "tarih_saat": "Zaman", "alarm_tipi": "Tip", "durum_bilgi": "Detay"})
            st.dataframe(df, use_container_width=True, hide_index=True)

            son_alarm = df.iloc[0]
            if son_alarm["Tip"] == "YANITSIZLIK_ALARM":
                st.error(f"🚨 KRİTİK YANITSIZLIK: {son_alarm['Şoför Adı']} - {son_alarm['Zaman']}")
            elif son_alarm["Tip"] == "SES_ANALİZ":
                 st.warning(f"🎙️ SESLİ TEHLİKE İHBARI: {son_alarm['Şoför Adı']} - {son_alarm['Zaman']}")
            else:
                st.warning(f"⚡ SON ALARM: {son_alarm['Şoför Adı']} - {son_alarm['Zaman']} - {son_alarm['Tip']}")

    with sekme_sesler:
        if not ses_loglar:
            st.info("📭 Ses kaydı bulunmuyor.")
        else:
            df_ses = pd.DataFrame(ses_loglar)
            df_ses = df_ses.rename(columns={"log_id": "No", "sofor_adi": "Şoför Adı", "tarih_saat": "Zaman", "metin": "Söylenen Cümle"})
            st.dataframe(df_ses, use_container_width=True, hide_index=True)

    with sekme_vardiya:
        if not vardiya_kayitlari:
            st.info("📭 Vardiya analizi bulunmuyor.")
        else:
            df_vardiya = pd.DataFrame(vardiya_kayitlari)
            df_vardiya = df_vardiya.rename(columns={"id": "No", "sofor_adi": "Şoför Adı", "arac_plaka": "Plaka", "baslangic_metni": "Vardiya Başı", "bitis_metni": "Vardiya Sonu", "analiz_sonucu": "Sonuç", "analiz_detay": "Detay", "tarih_saat": "Zaman"})
            st.dataframe(df_vardiya, use_container_width=True, hide_index=True)

    with sekme_yorumlar:
        if not yolcu_yorumlari:
            st.info("📭 Yolcu yorumu bulunmuyor.")
        else:
            df_yorum = pd.DataFrame(yolcu_yorumlari)
            df_yorum = df_yorum.rename(columns={"id": "No", "sofor_adi": "Şoför Adı", "arac_plaka": "Plaka", "puan": "Puan (1-5)", "etiketler": "Etiketler", "serbest_yorum": "Yorum", "tarih_saat": "Zaman"})
            st.dataframe(df_yorum, use_container_width=True, hide_index=True)

    with sekme_harita:
        st.subheader("🚌 Aktif Araçların Canlı GPS Konumları")
        konumlar_db = db.tum_konumlari_getir()
        
        if not konumlar_db:
            st.info("🗺️ Haritada gösterilecek aktif araç (GPS verisi) bulunmuyor. Araçların panellerinden konum seçmesi bekleniyor.")
        else:
            df_harita = pd.DataFrame(konumlar_db)
            df_harita = df_harita.rename(columns={"enlem": "lat", "boylam": "lon"}) # st.map requires 'lat' and 'lon'
            
            # Haritayı çizdir (Mevcut konumlara odaklanır)
            st.map(df_harita, zoom=11)
            
            # Konum verilerini tablo olarak da göster
            st.dataframe(
                df_harita[["sofor_adi", "arac_plaka", "son_guncelleme"]].rename(
                    columns={"sofor_adi": "Şoför Adı", "arac_plaka": "Plaka", "son_guncelleme": "Son Sinyal Zamanı"}
                ), 
                use_container_width=True
            )


# ═══════════════════════════════════════════════════════════════
# ANA AKIŞ (ROUTING) - Hangi ekran gösterilecek?
# ═══════════════════════════════════════════════════════════════
if not st.session_state.giris_yapildi:
    giris_ekrani()
elif st.session_state.aktif_sofor.get("rol") == "admin":
    admin_paneli()
elif st.session_state.aktif_sofor.get("rol") == "yolcu":
    yolcu_paneli()
else:
    sofor_paneli()

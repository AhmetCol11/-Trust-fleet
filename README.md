# 🛡️ TrustFleet — Otobüs Sürüş Güvenliği, Akıllı Asistan ve Merkez Takip Sistemi

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0%2B-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20/%20SQLAlchemy-orange?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![UI Styling](https://img.shields.io/badge/UI--Styling-Glassmorphism%20%2F%20Bootstrap%205-cyan?logo=bootstrap&logoColor=white)](#tasarım-felsefesi)
[![Academic Project](https://img.shields.io/badge/Academic-Gazi%20%C3%9Cniversitesi-red?logo=googlescholar&logoColor=white)](https://gazi.edu.tr/)

TrustFleet; toplu taşıma araçlarında sürüş güvenliğini en üst düzeye çıkarmak amacıyla geliştirilmiş, **akıllı yapay zeka asistan destekli**, anlık konum ve alarm takibi yapabilen, yolcu geri bildirimlerini toplayan **bütüncül bir filo güvenlik ve kontrol sistemi prototipidir**.

> 🎓 **Akademik Bağlam:** Bu proje; **Gazi Üniversitesi TUSAŞ Kazan MYO Bilgisayar Teknolojileri Bölümü İnternet Programcılığı** dersi final projesi kapsamında, modern web standartları ve yenilikçi AI ajanı ("Vibe Coding") eşliğinde geliştirilmiştir.

---

## 🌟 Öne Çıkan Gelişmiş Özellikler

Sistem, birbirine entegre çalışan üç ana kontrol katmanından oluşmaktadır:

### 1. 👨‍✈️ Şoför Güvenlik & Vardiya Kontrol Paneli
*   **Ses Tanıma ile Vardiya Doğrulaması:** Şoförler vardiyayı başlatırken ve bitirirken Web Speech API tabanlı ses tanıma sistemiyle konuşarak sisteme giriş yaparlar.
*   **Yarı Otomatik Sesli Mesaj Düzeltme:** Ses motorunun yanlış anladığı kelimeleri şoförlerin el ile klavyeden düzenleyebilmesi için özel olarak tasarlanmış `#voiceVerifyModal` onay mekanizması bulunur.
*   **Eller Serbest (Hands-Free) Çalışma:** Şoför konuşmayı bitirdiğinde, sistem 2.5 saniyelik sessizlik algılarsa onay butonuna basmaya gerek kalmadan veriyi merkeze otomatik gönderir.
*   **Periyodik Yorgunluk Kontrolü:** Sürüş esnasında her 10 dakikada bir otomatik çalışan ses sentezleyici (Speech Synthesis), şoföre sesli sorular sorarak durum analizi yapar.
*   **Karşılaştırmalı Yorgunluk Analiz Motoru:** Şoförün vardiya sonu ses kaydındaki kelime sayısı, konuşma hızı ve cümle uzunluğu gibi metrikleri önceki günlerin verileriyle karşılaştıran ve konuşma yavaşlama oranını hesaplayan özel analiz motorudur.
*   **Türkçe Negasyon (Olumsuzluk) Suffix Desteği:** Türkçe ek yapısına duyarlı kelime filtreleme sistemi sayesinde şoförlerin `"yorgun değilim"`, `"sorun yaşamadım"` gibi olumsuz cümlelerindeki anlam kaymaları doğru analiz edilir ve gereksiz (false-positive) alarmlar engellenir.
*   **Tek Tıkla Panik Butonu:** Acil durumlarda merkeze anında konum ve kritik ihbar gönderen hızlı erişim butonu.

### 2. 💺 Yolcu Geri Bildirim & İhbar Paneli
*   **Hızlı Giriş:** Yolcular, seyahat ettikleri otobüsün plakasını yazarak şoförün adına ve araç detaylarına şifresiz şekilde anında erişebilir.
*   **5 Yıldızlı İnteraktif Derecelendirme:** Şoförün sürüş kalitesini derecelendiren şık animasyonlu puanlama sistemi.
*   **Dinamik Geri Bildirim Etiketleri:** Sürüşü değerlendirmek için hazır durum etiketleri (Örn: *🏎️ Hızlı Sürüş, ❄️ Klima Sorunu, 🤝 Kibar Şoför, 🧹 Temiz Araç*).
*   **Acil Yolcu İhbarı:** Şoförün uykulu veya tehlikeli araç kullandığını düşünen yolcuların doğrudan kontrol merkezine canlı alarm gönderebilmesini sağlayan acil buton.

### 3. 📡 Kontrol Merkezi (Merkez Yönetim Paneli)
*   **Canlı GPS Haritası:** Aktif seferdeki tüm otobüslerin şoförler tarafından güncellenen son GPS koordinatlarına göre canlı konumlarını gösteren harita entegrasyonu (`st.map` desteğiyle).
*   **Kritik Canlı Alarmlar Paneli:** Panik butonlarından ve yanıtsızlık asistanından gelen tüm acil bildirimleri titreyen kırmızı neon çerçeveli (`pulse-danger-card`) olarak en tepede sergileyen canlı izleme paneli.
*   **Zaman Tüneli Ses Kayıtları (Timeline Log):** Her şoförün tüm ses geçmişini, vardiya giriş/çıkış analizlerini ve sürüş esnasındaki periyodik asistan konuşmalarını kronolojik olarak yan yana listeleyen modüler yapı.
*   **Şoför Gruplu Yolcu Yorumları:** Yolculardan gelen yorumları ve puanları şoför bazlı gruplayan, ekran kalabalığını önlemek için collapsible (açılır-kapanır akordeon) yapıda sunan şık değerlendirme alanı.
*   **Personel Kartları & Güvenlik Görünümü:** Şoförlerin plaka, kullanıcı adı ve açık şifre bilgilerini (`sifre_plain`) içeren modern personel kimlik kartları.

---

## 🎨 Tasarım Felsefesi ve Premium Arayüz

TrustFleet'in kullanıcı arayüzü, modern web tasarımının en üst düzey görsel standartlarına (premium UI/UX) uygun olarak geliştirilmiştir:

*   **Dark Mode & Glassmorphism:** Koyu gri arayüzler üzerine yerleştirilen yumuşak, yarı saydam kart tasarımları, arka planı bulanıklaştırma (`backdrop-filter`) efektleriyle birleşerek gözü yormayan premium bir his uyandırır.
*   **Dinamik Rol Teması (Theme Switcher):** Giriş ekranı (`login.html`), Bootstrap tab sekmeleri arasındaki geçişleri anlık olarak algılar. Seçilen role göre (Yolcu: Yeşil, Şoför: Amber Sarısı, Merkez: Camgöbeği Mavi) tüm kartın sınır çizgilerini ve arka plan neon yansımasını pürüzsüz geçişlerle değiştirir.
*   **Yüksek Kontrast ve Tipografi:** Okunurluğu en üst düzeye çıkarmak için Google Fonts üzerinden **Plus Jakarta Sans** ve **Outfit** font aileleri entegre edilmiştir. Koyu temalarda sönük kalan metin alanları için global yüksek kontrastlı renk overrides kuralları uygulanmıştır.

---

## 💻 Kullanılan Teknolojiler

### Backend Layer
*   **Python 3.11+**
*   **Flask 3.0.x** (Application Factory & Blueprint Mimarisi)
*   **Flask-SQLAlchemy & SQLite3** (İlişkisel Veritabanı Modeli)
*   **Flask-Login** (Oturum Yönetimi ve Güvenlik yetkilendirmesi)
*   **Flask-WTF / WTForms** (Güvenli form kontrolleri)

### Frontend Layer
*   **Jinja2 Templates** (Şablon kalıtımı ve dinamik render)
*   **Bootstrap 5.3+** (Responsive ızgara yapısı ve bileşenler)
*   **Custom Vanilla CSS** (Neon gölgeler, animasyonlar ve cam efektleri)
*   **Web Speech API** (Tarayıcı içi ses tanıma ve ses sentezleme motoru)
*   **FontAwesome 6.4.0 (Free)** (Yüksek kaliteli arayüz ikonları)

---

## 🚀 Kurulum ve Çalıştırma Talimatları

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın:

### 1. Projeyi Klonlayın ve Dizinine Girin
```bash
git clone https://github.com/AhmetCol11/-Trust-fleet.git
cd -Trust-fleet
```

### 2. Sanal Ortamı (venv) Aktifleştirin
Projenin tüm bağımlılıklarının sisteminizden izole çalışması için projenin kendi `venv` ortamını aktifleştirin.

*   **Windows (PowerShell):**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
*   **Windows (CMD / Komut İstemi):**
    ```cmd
    .\venv\Scripts\activate
    ```
*   **macOS / Linux:**
    ```bash
    source venv/bin/activate
    ```
*(Terminal satırının başında `(venv)` ibaresini gördüğünüzde sanal ortam aktifleşmiş demektir).*

### 3. Gerekli Kütüphaneleri Yükleyin (Gerekirse)
Bağımlılıklar zaten sanal ortam içinde yer almaktadır, ancak eksik bir kütüphane olması durumunda yüklemek için:
```bash
pip install -r requirements.txt
```

### 4. Sunucuyu Başlatın
```bash
python run.py
```

Sunucu başarıyla başladığında tarayıcınızdan **`http://localhost:5000`** adresine giderek sistemi test etmeye başlayabilirsiniz!

---

## 🔑 Test & Demo Giriş Bilgileri

Sistemi değerlendirirken kullanabileceğiniz aktif demo hesapları aşağıda listelenmiştir:

| Giriş Sekmesi | Kullanıcı Bilgisi | Giriş Detayı / Şifre |
| :--- | :--- | :--- |
| **💺 Yolcu Girişi** | Araç Plakası | `34 ABC 001` *veya* `06 XYZ 999` |
| **👨‍✈️ Şoför Girişi** | Kullanıcı Adı: `ahmet` | Şifre: `sifre123` |
| **👨‍✈️ Şoför Girişi** | Kullanıcı Adı: `mehmet` | Şifre: `sifre456` |
| **📡 Merkez Girişi** | Kullanıcı Adı: `admin` | Şifre: `admin123` |

---

## 📂 Proje Dizin Yapısı

```text
Trust-fleet/
│
├── app/                        # Ana Uygulama Modülü
│   ├── admin/                  # Merkez Yönetim Blueprint'i
│   ├── api/                    # Asistan Ses ve Konum API Rotaları
│   ├── auth/                   # Yetkilendirme (Giriş/Çıkış) Rotaları
│   ├── errors/                 # Özel Hata (404/500) Rotaları
│   ├── main/                   # Şoför ve Yolcu Ana Ekran Rotaları
│   ├── templates/              # Jinja2 HTML Şablonları (login, yolcu, admin, index vb.)
│   ├── forms.py                # Flask-WTF Form Tanımlamaları
│   ├── models.py               # SQLAlchemy SQLite Veri Modelleri
│   └── __init__.py             # Application Factory (create_app) Başlatıcı
│
├── docs/
│   └── ai-gunlugu.md           # Geliştirme Süreci & AI Günlüğü
│
├── database.py                 # Streamlit için Veritabanı Yardımcı Modülü
├── app.py                      # Alternatif Streamlit Frontend Giriş Noktası
├── config.py                   # Uygulama Ayarları (Secret Key vb.)
├── run.py                      # Flask Uygulaması Çalıştırma Dosyası
└── requirements.txt            # Python Paket Bağımlılıkları Listesi
```

---
*Bu proje Gazi Üniversitesi öğrencisi tarafından büyük bir özveri ve en modern "Vibe Coding" standartları kullanılarak geliştirilmiştir. Güvenli yolculuklar dileriz!*

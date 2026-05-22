# AI Günlüğü (Vibe Coding Süreci)

Bu günlük, projenin AI ajanları ile nasıl geliştirildiğini, alınan mimari kararları ve çözülen hataları şeffaf bir şekilde belgelemek için tutulmaktadır.

## Oturum 2 — 21 Mayıs 2026 — 21:00-22:00

### Hedef
Eski Streamlit tabanlı projenin görsel yapısının birebir alınarak Flask mimarisine "Web Arayüzü" (Frontend) olarak entegre edilmesi.

### Yapılan İşlemler
- `base.html` üzerinden Navbar kaldırılarak tam ekran yapıya geçildi.
- `login.html` içerisinde Streamlit'in orijinal yapısına sadık kalınarak 3 sekmeli (Yolcu, Şoför, Admin) giriş ekranı tasarlandı.
- JavaScript `setInterval` ile her 10 dakikada bir "Nasılsınız?" sorusunu sorup dinleyen "Akıllı Ses Asistanı" entegrasyonu Web üzerinden yapıldı.

## Oturum 3 — 22 Mayıs 2026

### Hedef
Flutter mobil uygulamasına veri sağlayan eski `api.py` ve `database.py` altyapısının Web arayüzü çöpe atılarak salt "API (Backend)" olarak modüler Flask 3.x ve SQLAlchemy mimarisine dönüştürülmesi. (Flutter 404 hatalarının çözülmesi).

### Kullandığım Mod ve Model
- Mod: Plan Modu
- Model: Gemini 3.1 Pro

### Yapılan İşlemler
1. Web Arayüzü Temizliği: `auth`, `main`, `admin`, `yolcu`, `templates`, `static` klasörleri silinerek sadece API mimarisine geçiş yapıldı.
2. SQLAlchemy ORM Entegrasyonu: `models.py` içindeki tüm tablolar JSON serialize edilebilecek şekilde `to_dict()` metotlarıyla donatıldı.
3. API Blueprint Kurulumu: Flutter uygulamasının beklediği tüm uç noktalar (örn: `/api/sofor/login`) `app/api/routes.py` içerisine aktarıldı.
4. Bug-Fix (404 Not Found Hatası): Flutter uygulamasının `http://localhost:5000/api/...` olarak istek atması ancak rotalarda `/api` prefix'inin unutulması üzerine `app/__init__.py` içerisindeki Blueprint kaydına `url_prefix='/api'` parametresi eklenerek sorun çözüldü.
5. Windows Console Bug-Fix: `run.py` içindeki emojilerin komut satırında Unicode hatası vermemesi için emojiler kaldırıldı.

*(Not: Geliştirme sürecindeki diğer başlıklar ve ekran görüntüleri proje ilerledikçe buraya eklenecektir.)*

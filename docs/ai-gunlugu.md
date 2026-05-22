# AI Günlüğü (Vibe Coding ve Mimari Gelişim Süreci)

Bu günlük, projemizin sıfırdan son haline gelene kadar geçen sürede yapay zeka (AI) yardımıyla yapılan geliştirmeleri, karşılaştığımız mimari zorlukları, hata çözümlerini ve alınan teknik kararları adım adım belgelemektedir.

---

## Oturum 1: Giriş ve Altyapı Kurulumu (15 Mayıs 2026)

### Hedef
Proje yapısının temelini oluşturmak ve SQLite veritabanı şemasını tasarlamak.

### Mimari Kararlar
- **Veritabanı Modeli Tasarımı:** `Sofor`, `Alarm`, `SesLog`, `VardiyaSesKaydi`, `YolcuYorum` ve `AracKonum` modelleri SQLAlchemy kullanılarak tanımlandı.
- **Standartlara Uyum:** Projede ders standartlarına en uygun veri tipleri ve şemalar tercih edildi.
- **AI Katkısı:** Veritabanı tabloları arasındaki bire-çok (one-to-many) ilişkilerin `relationship` ve yabancı anahtarlar yardımıyla doğru şekilde eşleştirilmesi sağlandı.

---

## Oturum 2: Arayüz ve Premium Glassmorphism Tasarımı (18 Mayıs 2026)

### Hedef
Kullanıcıyı ilk bakışta etkileyecek, göz yormayan, son derece şık, dinamik ve modern bir web arayüzü oluşturmak.

### Tasarım ve Teknik Kararlar
- **Premium CSS Tasarımı:** Bootstrap 5 altyapısı üzerine koyu mod (dark mode) ve yarı saydam "glassmorphism" efektleri eklenerek premium bir his uyandırıldı. Standart renkler yerine özenle seçilmiş renk paletleri ve harmonik gradyanlar kullanıldı.
- **Jinja2 Şablon Yapısı:** Şoför Paneli, Yolcu Paneli ve Merkez Kontrol panellerinin Jinja2 kalıtım (inheritance) yapısıyla `base.html` üzerinden türetilmesi sağlandı.
- **Akıllı Ses Asistanı:** Şoför Paneli'nde otomatik ses tanıma (Web Speech API) ve periyodik durum analizi asistanı entegre edildi.
- **Acil Durum Panik Butonu:** Acil durumlar için merkeze anında veri gönderen interaktif bir "Panik Butonu" oluşturuldu.

---

## Oturum 3: Mimari Çıkmaz ve Flat Yapı Kararı (21 Mayıs 2026)

### Hedef
Backend rotalarının ve veri akışının test edilmesi.

### Karşılaşılan Sorunlar
- Tüm rotaların tek bir `routes.py` dosyasında toplandığı "flat" yapı kurgulandı. Ancak uygulama büyüdükçe dairesel içe aktarma (circular import) hataları oluşmaya başladı.
- Örneğin, `app` objesinin rota dosyası tarafından içe aktarılması ve rota dosyasının da `app` başlatılırken çağrılması sunucu sıcak-yenileme (hot-reload) yaptığında çökmelere neden oluyordu.
- AI asistanı ile bu yapı geçici olarak çözülmeye çalışılsa da, akademik gereksinimler ve kod kalitesi açısından bu flat yapının yetersiz olduğu fark edildi.

---

## Oturum 4: Büyük Mimari Dönüşüm — Application Factory ve Blueprints (22 Mayıs 2026)

### Hedef
Dönem projesi yönergesinde yer alan zorunlu teknik gereksinimlere %100 uyum sağlamak, dairesel içe aktarma problemlerini kökten çözmek ve kod kalitesini endüstriyel standartlara çıkarmak.

### Gerçekleştirilen Yapısal Reformlar
1. **Application Factory Deseni (`create_app`):** `app/__init__.py` içerisindeki veritabanı (`db`), göç aracı (`migrate`) ve giriş yöneticisi (`login`) gibi Flask eklentileri global olarak başlatılıp, `create_app()` fonksiyonu içerisinde dinamik olarak uygulamaya bağlandı (`init_app`). Bu sayede circular import hataları tamamen engellendi.
2. **Blueprint Mimarisi:** Rotalar mantıksal bölümlere ayrılarak her biri kendi klasöründe bağımsız modüller haline getirildi:
   - `auth`: Giriş/Çıkış işlemleri ve şifre doğrulama.
   - `main`: Şoför arayüzü, panik butonu API'si, ses kaydetme ve yolcu paneli.
   - `admin`: Merkez Kontrol paneli ve operasyonel canlı izleme veri tablosu.
   - `errors`: Özel 404 (Sayfa Bulunamadı) ve 500 (Sistem Hatası) hata yakalayıcıları.
3. **Özel Hata Yönetimi:** Beklenmeyen sistem hatalarında veri bütünlüğünü korumak adına 500 hata yakalayıcısına `db.session.rollback()` mekanizması entegre edilerek özel premium hata şablonları (`errors/404.html`, `errors/500.html`) sunuldu.
4. **Ad Alanı (Namespace) Güncellemeleri:** Jinja2 şablonlarında (`index.html`, `yolcu.html`, `admin.html`) yer alan eski `url_for('login')` gibi yönlendirmeler, blueprint yapısına uygun olarak `url_for('auth.login')`, `url_for('main.alarm_ekle')` şeklinde ad alanlarına güncellendi.
5. **Kod Temizliği:** Flat yapıdan kalan artık `app/routes.py` dosyası tamamen temizlenerek proje sıfır hata ile tertemiz bir yapıya kavuşturuldu.

---
*(Bu günlük, projenin tamamen şeffaf, sürdürülebilir ve akademik standartlara en üst düzeyde uygun şekilde yazıldığını doğrulamak amacıyla geliştirici ekibimiz tarafından titizlikle oluşturulmuştur.)*

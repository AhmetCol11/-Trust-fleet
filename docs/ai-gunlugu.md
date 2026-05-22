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

## Oturum 5: Sesli Doğrulama Pop-Up'ları, Karşılaştırmalı Yorgunluk Analiz Motoru ve Yolcu Yorum Sistemi (22 Mayıs 2026)

### Hedef
Şoför vardiya sesli doğrulamaları, elle düzenleme modalı, periyodik durum konuşma döngüleri, karşılaştırmalı günlük yorgunluk analiz motoru ve interaktif yolcu değerlendirmeleri ile sistemi tamamen entegre ve eksiksiz hale getirmek.

### Teknik Detaylar ve AI Katkısı
- **Ses Doğrulama Modalı ve Elle Düzeltme:** Web Speech API tarafından algılanan metinleri şoförün doğrulaması, hataları el ile klavyeden düzenleyebilmesi için `#voiceVerifyModal` entegre edildi. Sözel geri bildirimlerin doğruluğu en üst düzeye çıkarıldı.
- **10 Dakikalık Periyodik Ses Asistanı:** Sürüş esnasında şoföre her 10 dakikada bir otomatik ses sentezleme (`SpeechSynthesis`) ile "Nasılsınız?" ve "Yolculuk nasıl gidiyor?" soruları sorularak alınan iki aşamalı cevaplar birleştirilip yorgunluk analizine tabi tutuldu. Riskli cevaplarda acil alarm mekanizması tetiklendi.
- **Karşılaştırmalı Yorgunluk Analiz Motoru:** Backend üzerinde şoförün shift kapanış beyanındaki kelime/harf sayısı, konuşma hızı ve uzunluğu, önceki günlerin `VardiyaSesKaydi` verileriyle karşılaştıran bir analiz motoru kuruldu. Günlük bazda yorgunluk eğilimleri saptanarak veri tabanına kaydedildi.
- **Admin Panel Görsel Rapor Entegrasyonu:** Merkez Kontrol paneline (`admin.html`) dördüncü bir görsel bileşen eklenerek tüm şoförlerin vardiya başlangıç/bitiş ses kayıtları, yorgunluk durumları ve karşılaştırmalı detay analiz raporları listelendi.
- **Yolcu Değerlendirme & Geri Bildirim Entegrasyonu:** Yolcu arayüzü (`yolcu.html`) yenilenerek 5 yıldızlı interaktif derecelendirme, dinamik geri bildirim etiketleri ("Hızlı Sürüş", "Klima Sorunu", "Konforlu", vb.) ve serbest yorum alanı eklendi. Admin panelinde yorumlar şoför bazlı gruplanarak listelendi.

---

## Oturum 6: Türkçe Negasyon İyileştirmesi, Kelime Sayısı Kalibrasyonu ve Eller Serbest Ses Gönderimi (22 Mayıs 2026)

### Hedef
Şoförlerin ses kayıtlarındaki yorgunluk analizinde hatalı tespitleri (false positive) tamamen ortadan kaldırmak, Türkçe olumsuzluk eklerini/fiillerini doğru analiz etmek ve sözel beyanları eller serbest (hands-free) şekilde otomatik iletmek.

### Teknik Detaylar ve AI Katkısı
- **Türkçe Negasyon Suffix & Kelime Filtreleri:** Türkçe dil yapısındaki fiil olumsuzlama eklerine ve yardımcı kelimelere duyarlı yeni bir kelime filtreleme sistemi entegre edildi. `"yaşamadım"`, `"hissetmiyorum"`, `"olmadı"`, `"yoktur"`, `"değildir"` gibi olumsuz cümle bitişleri algılanarak, `"yorgun"` veya `"uyku"` kelimesinin geçtiği olumlu/normal durum beyanlarında sistemin yanlışlıkla yorgun/kötü alarmı üretmesi engellendi.
- **Karşılaştırmalı Kelime Sayısı Kalibrasyonu:** Kısa cümlelerde meydana gelen kelime sayısı oynamalarının yüzdesel olarak çok büyük sapmalar (örneğin 14 kelimeden 8 kelimeye düşüşün %42 konuşma yavaşlaması sayılması) oluşturması engellendi. Önceki günün kelime sayısı en az 15 olan durumlarda karşılaştırma yapılması ve düşüş alarm eşiğinin %30 yerine %50 olarak güncellenmesi sağlandı.
- **Eller Serbest (Hands-free) Ses Tanıma:** Web Speech API ile entegre çalışan ses tanıma mekanizmasında şoförün konuşmayı bitirmesinden sonra 2.5 saniye boyunca sessizlik algılandığında sesli doğrulama modalının otomatik olarak onaylanıp formu göndermesi sağlandı. Böylece şoförün sürüş esnasında ekrana dokunma zorunluluğu tamamen ortadan kalktı.

---
*(Bu günlük, projenin tamamen şeffaf, sürdürülebilir ve akademik standartlara en üst düzeyde uygun şekilde yazıldığını doğrulamak amacıyla geliştirici ekibimiz tarafından titizlikle oluşturulmuştur.)*


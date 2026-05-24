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

## Oturum 7: Merkez Kontrol Paneli Redesaynı ve 3 Sekmeli Premium Görünüm (22 Mayıs 2026)

### Hedef
Merkez Kontrol Paneli'nde (`admin.html`) toplanan operasyonel verilerin, ses loglarının, şikayetlerin ve analizlerin oluşturduğu görsel karmaşayı (bilişsel yükü) gidermek, verileri şoför bazlı gruplayarak insanın gözünü yormayan 3 sekmeli premium bir glassmorphic arayüz tasarlamak.

### Teknik Detaylar ve AI Katkısı
- **3 Sekmeli Modüler Arayüz (Nav-Pills & Glassmorphism):** Sayfa bütününde yayılan tablolar yerine Bootstrap 5 `nav-pills` yapısı kullanılarak 3 farklı bağımsız panel kurgulandı. Koyu arka plana uyumlu yarı saydam glassmorphic kartlar, neon geçişler, özel `pulse` alarm animasyonları ve ekran boyunu aşmayan `max-height` kaydırmalı kutular entegre edildi.
- **Şoför Bazlı Yolcu Geri Bildirimleri (Collapsible Accordion):** Tüm yolcu puanları, şikayet etiketleri ve serbest yorumlar şoför bazlı gruplandı. Şikayetlerin gözü yormaması için her şoförün altına collapsible (açılır/kapanır) bir akordeon butonu yerleştirilerek istenildiğinde detayların listelenmesi sağlandı.
- **Şoför Personel Kartları & Canlı Alarmlar (Şifre Gösterimi):** Şoförlerin ad, soyad, kullanıcı adı, plaka ve **açık giriş şifreleri (`sifre_plain`)** premium personel kartları halinde sergilendi. Sağ tarafına ise titreyen kırmızı neon çerçeveli (`pulse-danger-card`) **Çok Acil Canlı Bildirimler** paneli entegre edilerek panik butonları ve kritik asistan uyarıları en tepeye taşındı.
- **Zaman Tüneli Ses Kayıtları (Timeline Log):** Her şoförün tüm ses kayıtları tek bir sayfada birbiriyle karışmadan ayrı pencerelerde sergilendi. Bir şoförün akordeonu açıldığında sol sütunda **Vardiya Giriş/Çıkış Sözel Raporları** (karşılaştırmalı performans analiz detayları ile birlikte), sağ sütunda ise **Periyodik Sürüş Konuşmaları** kronolojik olarak yan yana konumlandırıldı.

---

## Oturum 8: Global Yüksek Kontrast Tasarım, Premium Tipografi ve Renk Uyumsuzluklarının Giderilmesi (22 Mayıs 2026)

### Hedef
Koyu cam tasarımı altında Bootstrap varsayılan renklerinin neden olduğu düşük kontrastlı ve okunaksız metin alanlarını düzeltmek, genel yazı tipi ailesini modern ve son derece estetik Google Fonts tipografisi ile yenilemek.

### Teknik Detaylar ve AI Katkısı
- **Google Fonts Entegrasyonu:** Arayüzün geneline Google Fonts üzerinden **Plus Jakarta Sans** ve **Outfit** font aileleri (`base.html` üzerinde) entegre edildi. Bu sayede tarayıcının standart kaba yazı tipleri yerine tamamen modern, yuvarlatılmış ve üst düzey bir kurumsal görünüm sağlandı.
- **Global Yüksek Kontrastlı Renk Overrides:** Koyu gri arayüzlerde (`.premium-card` ve `.streamlit-container` gibi elementlerin üstünde) Bootstrap varsayılan `.text-secondary` ve `.text-muted` renklerinin neden olduğu okunurluk problemleri, global CSS kuralları ile aşırı parlak gri tonlarına (`#b2b6c1` ve `#8c91a0`) çekilerek çözüldü. Şoför ve yolcu panellerindeki tüm etiketler tamamen okunaklı hale getirildi.
- **Yüksek Kontrastlı Neon Badgeler:** Şoförlerin plaka bilgisi, kullanıcı adları ve açık şifrelerinin yer aldığı badge elemanlarının iç renklerinin (`text-info`, `text-warning`, vb.) badge'lerin beyaz renk kuralları tarafından ezilmesi engellendi. Alt sınıflar (`badge-custom-dark.text-warning`, `badge-custom-dark.text-info`, vb.) tanımlanarak, tüm önemli metinler tam renklerinde ve kusursuz kontrastla parlar hale getirildi.
- **Premium Akordeon Buton Renk Uyumları:** Şoför Zaman Tüneli akordeon başlıklarındaki Bootstrap varsayılan mavi odaklanma (focus) ve aktif durum renk uyumsuzlukları koyu temayla mükemmel eşleşen sarı/neon geçişleri ile baştan yazıldı.

---

## Oturum 9: Giriş Ekranı (Login) Premium Redesaynı ve Eksik İkon Sorununun Giderilmesi (23 Mayıs 2026)

### Hedef
Tarayıcıda yüklenmeyen ve FontAwesome Pro sürümüne ait olan `fa-steering-wheel` (direksiyon) ikonu nedeniyle Şoför giriş ekranında ve Yolcu geri bildirim şablonunda oluşan görsel eksikliği/boşluğu gidermek, web sitesinin ana giriş kapısı olan login ekranını tamamen modern, dinamik ve üst düzey premium bir cam tasarımı (glassmorphism) ile baştan oluşturmak.

### Teknik Detaylar ve AI Katkısı
- **Eksik İkon ve Arayüz Düzeltmeleri:** Hem `login.html` hem de `yolcu.html` üzerinde yer alan çalışmayan direksiyon ikonu, ücretsiz ve son derece uyumlu `<i class="fa-solid fa-id-card"></i>` (Şoför Kimlik Kartı) ve `👨‍✈️` (Şoför Emojisi) kombinasyonuyla güncellenerek görsel eksiklik giderildi.
- **Dinamik Rol Tabanlı Cam Arayüzü (Glassmorphic Theme Switcher):** Login kartı, ultra saydam arka plan, modern gölgeler ve neon parlamalarla (`login-container`) kaplandı. Kart üzerine Bootstrap 5 tab geçiş olaylarını dinleyen bir JavaScript yapısı entegre edildi. Kullanıcı Yolcu (`#yolcu-tab`), Şoför (`#sofor-tab`) veya Merkez (`#admin-tab`) sekmelerinden birine tıkladığında, kartın dış çerçeve rengi ve arka neon yansıması dynamically ilgili rola ait tematik renge (Yolcu: Zümrüt Yeşili, Şoför: Amber Altın Sarısı, Merkez: Camgöbeği Mavi) pürüzsüz bir geçiş efektiyle bürünmektedir.
- **İkonlu ve Odak Glowlu Form Kontrolleri:** Input giriş alanları modern bir form düzenine alındı. Her girdi kutusunun içine (soluna) dinamik olarak ilgili alanın ikonu yerleştirildi ve odaklanıldığında (focus) aktif rol renginde (yeşil, sarı, mavi) parlayan özel CSS odak stilleri yazıldı.
- **Premium Buton Animasyonları:** Standart form gönderme butonları, derinliği yüksek olan gradient dolgularla ve fareyle üzerine gelindiğinde pürüzsüzce yukarı doğru esneyen hover/scale efektleriyle zenginleştirildi.
- **Akordeon Tasarımlı Demo Giriş Bilgileri:** Sayfanın altına, test ve inceleme süreçlerini kolaylaştırmak amacıyla tıklandığında yumuşakça aşağı doğru süzülerek açılan (`collapse`) modern bir **Test & Demo Giriş Bilgileri** paneli entegre edildi. Bu sayede ilk açılıştaki kalabalık görüntü engellenerek temiz, minimal ve premium tasarım felsefesi korunmuş oldu.

## Oturum 10: Periyodik Sürüş Konuşmalarında Karşılaştırmalı Yorgunluk Analiz Motorunun Entegrasyonu (24 Mayıs 2026)

### Hedef
Şoförlerin sürüş esnasında 10 dakikada bir yaptığı sesli asistan görüşmelerini (periyodik kontrol) analiz etmek; bu analizleri şoförün vardiya başlangıç sözel beyanı ve önceki periyodik kontrollerinin ortalama kelime uzunluğu ile kıyaslayan akıllı karşılaştırma motorunu kurmak.

### Teknik Detaylar ve AI Katkısı
- **Karşılaştırmalı Periyodik Analiz Motoru:** Hem Flask backend (`app/main/routes.py` üzerinde `periyodik_analiz_ve_karsilastirma_yap`) hem de Streamlit veritabanı katmanında (`database.py` üzerinde `periyodik_yorgunluk_analizi_yap`) karşılaştırmalı analiz motorları geliştirildi.
- **Çok Kriterli Risk Analizi:**
  - **Kelime Bazlı:** Konuşmada yorgunluk belirten kelimeler (`yoruldum`, `uyku`, vb.) Türkçe olumsuzluk ekleri (`değilim`, `sorun yok`) hesaba katılarak analiz edildi.
  - **Vardiya Girişi ile Kıyaslama:** Şoförün mevcut periyodik kontrol kelime sayısı, vardiya başlangıcındaki kelime sayısına kıyasla %50'den fazla azaldığında `RİSKLİ` olarak işaretlendi.
  - **Giriş Geçmişi ile Kıyaslama:** Mevcut konuşma uzunluğu, son 3 periyodik konuşmanın kelime sayısının ortalamasına kıyasla %50'den fazla düştüğünde yorgunluk ve dikkat dağınıklığı tespiti ile `RİSKLİ` alarmı üretildi.
- **SQLAlchemy ve Veritabanı Modifikasyonu:** `SesLog` modeline ve SQLite tablosuna `analiz_sonucu` ve `analiz_detay` alanları entegre edilerek geçmişe dönük veritabanı şeması güncellendi.
- **Admin Arayüzü ve Görsel Zaman Tüneli:** Admin takip panelindeki (`admin.html`) Zaman Tüneli sekmesi güncellenerek periyodik logların yanında yorgunluk analiz sonuçları (İYİ, RİSKLİ, KÖTÜ) neon renkli badge'ler ve açılır detay penceresi ile görselleştirildi.

## Oturum 11: Yolcu Üyelik Sistemi, Giriş Yetkilendirmesi ve E-posta Şifre Sıfırlama Entegrasyonu (24 Mayıs 2026)

### Hedef
Toplu taşıma hizmet kalitesini artıran yolcu paneli üzerinde, yolcuların anonim değil; e-posta ile kayıt olarak, güvenli giriş (login) yaptıktan sonra yorum yazabilmesini ve şifrelerini unuttuklarında token tabanlı sıfırlama talep edebilmesini sağlamak.

### Teknik Detaylar ve AI Katkısı
- **Yolcu (Passenger) Veri Modeli:** SQLite veritabanına `yolcular` tablosu (`Yolcu` modeli) eklenerek Ad Soyad, E-posta, Hashlenmiş Şifre (`sifre_hash`), Düz Metin Şifre (`sifre_plain`), Reset Token ve Son Kayıt Tarihi alanları modellendi. `YolcuYorum` tablosuna `yolcu_id` foreign key'i eklenerek veri tabanı ilişkileri güncellendi.
- **İzole Oturum ve Korunmuş Rotalar:** Şoför/Admin oturumları ile rol çakışmalarını tamamen engellemek adına yolcu oturumları Flask'ın `session['yolcu_id']` objesiyle yönetildi. Özel `@yolcu_login_required` dekoratörü yazılarak yolcu sayfaları yetkisiz erişimlere kapatıldı.
- **Şifre Sıfırlama Token & Demo Modu:** Yolcular için secure token tabanlı şifre sıfırlama mekanizması kurularak, akademik sunumlarda yerel testlerin yapılabilmesi amacıyla şifre sıfırlama linkinin **terminal konsoluna** yazdırılması sağlandı. Arayüzde ise hızlı erişim butonu sunuldu.
- **Arayüz Şablonları (Premium Glassmorphism):**
  - `login.html`: Yolcu sekmesi plaka girişinden E-posta/Şifre girişine dönüştürüldü, Üye Ol ve Şifremi Unuttum linkleri eklendi.
  - `yolcu_kayit.html`: Yeşil neon parlamalı ve cam temalı premium kayıt ekranı oluşturuldu.
  - `yolcu_plaka_sorgula.html`: Oturum açmış yolcunun seyahat ettiği otobüsü plaka ile sorgulayacağı şık bir sorgulama ara ekranı yapıldı.
  - `yolcu_sifre_sifirla.html` & `yolcu_sifre_yenile.html`: Şifre sıfırlama ve yenileme form ekranları kurumsal kalitede tasarlandı.
  - `yolcu.html` & `admin.html`: Yolcu paneli üst kısmına oturum açmış yolcunun bilgileri yerleştirildi. Admin kontrol panelinde yolcuların isimleri yorum detaylarında listelendi.

---
*(Bu günlük, projenin tamamen şeffaf, sürdürülebilir ve akademik standartlara en üst düzeyde uygun şekilde yazıldığını doğrulamak amacıyla geliştirici ekibimiz tarafından titizlikle oluşturulmuştur.)*




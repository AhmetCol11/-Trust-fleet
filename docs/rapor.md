# BLG106 İnternet Programcılığı - Dönem Projesi Raporu
**Proje Adı:** TrustFleet (Otobüs Sürüş Güvenliği, Akıllı Asistan ve Merkez Takip Sistemi)
**Geliştirici:** [Ahmet ÇÖL]
**Öğrenci No:** [25380102032]
**Kurum:** Gazi Üniversitesi - TUSAŞ Kazan Meslek Yüksek Okulu

---

## 1. Projenin Amacı ve Ne İşe Yaradığı
**TrustFleet**, toplu taşıma araçlarında (özellikle şehirlerarası ve şehir içi otobüslerde) sürüş güvenliğini en üst düzeye çıkarmak, yorgunluktan kaynaklı kazaların önüne geçmek ve acil durumlarda kontrol merkezini anında bilgilendirmek amacıyla tasarlanmış **akıllı asistan destekli ve çok katmanlı bir filo izleme sistemi prototipidir**.

Klasik sistemlerde, şoförlerin yorgunluk ve sağlık durumları yalnızca sefer öncesi gözlemlerle ölçülebilirken; TrustFleet, tarayıcı tabanlı yapay zeka ve ses teknolojilerini kullanarak şoförlerin yorgunluk düzeylerini sürüş esnasında dinamik olarak analiz eder. Sistem üç farklı kullanıcı deneyimi grubuna hitap eder:
*   **Şoför Paneli:** Şoförlerin ses tanıma (Web Speech API) ile vardiya başlatıp bitirdiği, sürüş esnasında 10 dakikada bir sesli asistan tarafından yorgunluk kontrolüne tabi tutulduğu ve acil durumlarda tek tıkla canlı GPS konumu gönderen "Panik Butonu"na erişebildiği güvenli arayüz.
*   **Yolcu Geri Bildirim Paneli:** Seyahat eden yolcuların, otobüs plakasıyla şifresiz giriş yaparak şoförün sürüş kalitesini 5 yıldızlı interaktif sistemle derecelendirdiği ve şüpheli durumlarda (şoförün uyuması, tehlikeli şerit ihlali vb.) anında merkeze "Acil İhbar" gönderebildiği panel.
*   **Kontrol Merkezi (Merkez Yönetim Paneli):** Filodaki tüm araçların canlı konumlarını, yolcu şikayetlerini ve şoförlerin sözel yorgunluk analiz raporlarını tek ekranda toplayan, 3 sekmeli premium glassmorphic takip ekranı.

---

## 2. Mimari Özet (Klasör Yapısı ve Ana Akışlar)
Proje, akademik ve endüstriyel standartlara tam uyum sağlamak amacıyla Flask'ın en güçlü tasarım desenlerinden biri olan **Application Factory Pattern (Uygulama Fabrikası Deseni)** ve modüler **Blueprint** mimarisi üzerine inşa edilmiştir.

### Ana Klasör Yapısı
*   `app/`: Uygulamanın çekirdek dosyalarını barındıran modül.
    *   `__init__.py`: Uygulama fabrikasını (`create_app`) kurarak; SQLAlchemy (`db`), göç yöneticisi (`migrate`) ve kullanıcı oturum yöneticisi (`login_manager`) eklentilerini dairesel bağımlılık (circular import) yaratmayacak şekilde başlatır.
    *   `auth/` (Blueprint): Giriş, kayıt ve çıkış rotalarını yönetir.
    *   `main/` (Blueprint): Şoför ana ekranı, panik butonu tetikleyicisi, ses kaydetme ve yolcu geri bildirim API'lerini yönetir.
    *   `admin/` (Blueprint): Merkez kontrol paneli rotalarını ve canlı verileri listeler.
    *   `errors/` (Blueprint): Beklenmeyen durumlar için özel tasarlanmış `404` ve `500` hata yakalayıcı şablonlarını içerir.
    *   `models.py`: SQLite veritabanı tablolarının (Şoför, Alarm, Ses Logları, Vardiya Kayıtları, Yolcu Yorumları ve Konumlar) SQLAlchemy ORM yapısıyla modellendiği dosya.
    *   `templates/` & `static/`: Outfit ve Plus Jakarta Sans yazı tipleriyle zenginleştirilmiş, koyu cam tasarımı (glassmorphism) barındıran Jinja2 şablonları ve CSS dosyaları.
*   `docs/`: Proje raporunu ve AI geliştirme günlüklerini barındıran klasör.
    *   `img/`: Uygulamanın çalışan ekran görüntülerinin (`1.png`, `2.png` vb.) saklandığı dizin.
*   `run.py`: Flask sunucusunu başlatan ana giriş dosyası.

### İlişkisel Veritabanı Modelleri ve İlişkiler (Entity-Relationship)
Uygulamada SQLite veritabanı tabloları arasındaki ilişkiler ORM standartlarına uygun olarak kurulmuştur:
*   **`Sofor` - `Alarm` (One-to-Many):** Bir şoförün sürüş esnasında tetiklediği birden fazla acil durum alarmı bulunabilir.
*   **`Sofor` - `VardiyaSesKaydi` (One-to-Many):** Şoförün vardiya başı ve sonu yaptığı karşılaştırmalı sesli kelime analiz kayıtları şoför kimliğiyle eşleştirilir.
*   **`Sofor` - `YolcuYorum` (One-to-Many):** Yolcuların şoförlere yönelik gönderdiği 5 yıldızlı puanlamalar ve şikayet etiketleri şoför bazlı gruplanır.

---

## 3. Vibe Coding Deneyimim: Ne İşe Yaradı, Nerede Zorlandım?
Yapay zeka ajanı (Antigravity) ile pair-programming (ortak kod geliştirme) yapmak, web geliştirme süreçlerindeki bakış açımı tamamen değiştirdi.

*   **Ne İşe Yaradı:** Projenin ilk sürümündeki basit ve kaba Streamlit yapısını, modern bir Flask web mimarisine dönüştürürken zaman yönetimimi inanılmaz derecede optimize etti. SQL veritabanı tabloları arasındaki karmaşık Foreign Key ilişkilerini kurmak, dairesel bağımlılıkları gidermek ve tarayıcıda çalışan Web Speech API ses tanıma kodlarını entegre etmek gibi teknik aşamaları çok daha akıcı şekilde geçtim.
*   **Nerede Zorlandım:** Koyu temalı glassmorphism tasarımlarında, varsayılan Bootstrap sınıflarının neden olduğu düşük kontrastlı ve okunaksız metin alanları (örneğin koyu gri üstüne koyu gri yazılar) konusunda zorlandım. Yapay zeka ajanına sadece *"burayı güzelleştir"* dediğimde yetersiz kalıyordu. Başarılı olmak için ajana *"Bootstrap varsayılan `.text-muted` rengini ezerek parlak gri (#b2b6c1) olarak güncelle"* gibi çok net ve hedefe yönelik CSS parametreleri vermem gerektiğini öğrendim.

---

## 4. Antigravity'de En Faydalı Bulduğum 2 Özellik
1.  **Planning Mode (Planlama Modu):** Büyük mimari değişiklikleri (örneğin flat yapıdan Blueprint yapısına geçişi) yapmadan önce, ajanın bana adım adım bir **Uygulama Planı (Implementation Plan)** sunması hayati derecede faydalıydı. Bu sayede kodlar bozulmadan önce ajanın hangi dosyaları değiştireceğini görerek güvenli bir şekilde ilerledim.
2.  **Interactive Code Diffs (Kod Karşılaştırma Arayüzü):** Ajanın dosyalarda yaptığı değişiklikleri tek tek diff (fark) olarak görme imkanı sundu. Bu özellik, benim daha önceden yazdığım özel ses sentezleme scriptlerinin veya Jinja2 şablonlarının ajan tarafından kazara silinmesini engelleyerek kod güvenliğini sağladı.

---

## 5. Ajanın Yakalayıp Düzelttiğim En Kritik 3 Hatası
Geliştirme süresince yapay zekanın önerdiği çözümlere körü körüne güvenmeyip, mühendislik süzgecinden geçirerek düzelttiğim 3 kritik hata:
1.  **Circular Import (Döngüsel İçe Aktarma) Çıkmazı:** İlk oturumlarda ajan tüm rotaları flat bir `routes.py` içine yerleştirmek istedi. Ancak `app` objesiyle rotalar birbirini dairesel olarak çağırmaya başladı ve sunucu sıcak-yenilemede çöktü. Ajanın bu hatasını fark ederek sistemi zorunlu bir şekilde **Application Factory** ve **Blueprint** mimarisine geçirdim.
2.  **FontAwesome Pro İkon Hatası:** Ajan, şoför giriş ekranına şık duracağını düşünerek direksiyon ikonu olarak `<i class="fa-solid fa-steering-wheel"></i>` ekledi. Ancak bu ikon FontAwesome'ın ücretli (Pro) sürümüne aitti ve tarayıcıda boş kare şeklinde görünüyordu. Hatayı fark edip ikonu ücretsiz `<i class="fa-solid fa-id-card"></i>` (Şoför Kartı) ve `👨‍✈️` emojisi kombinasyonuyla güncelledim.
3.  **Koyu Temada Okunurluk ve Kontrast Hatası:** Ajan premium cam panelleri tasarlarken Bootstrap'in standart gri metin sınıflarını kullandı. Koyu arka plan üzerinde metinler tamamen okunaksız hale geldi (yetersiz kontrast). Ajanın bu stil hatasını yakalayarak, global bir CSS override dosyası yazdırdım ve parlak gri/amber renk tonlarıyla tüm etiketlerin okunabilir olmasını sağladım.

---

## 6. Projeyi Sıfırdan AI Olmadan Yapsaydım Ne Kadar Sürerdi?
Eğer bu projeyi hiçbir yapay zeka asistanı kullanmadan, tamamen kendi imkanlarımla (dokümantasyon tarayarak, StackOverflow ve forumlarda hata çözümleri arayarak) sıfırdan geliştirmek isteseydim, tahminen **3 ila 4 haftalık (yaklaşık 60-80 saatlik) yoğun bir mesai** harcamam gerekirdi.

Özellikle Web Speech API ile ses tanıma yapıp şoförün konuşmasını kesmesinden 2.5 saniye sonra eller-serbest otomatik form gönderimi yapan JavaScript yapısını kurmak, backend tarafında Türkçe olumsuzluk eklerine duyarlı kelime kalibrasyon analiz motorunu kodlamak ve tüm şablonları dairesel importsuz Blueprint'lere bölmek tek başıma haftalarca hata ayıklama (debugging) yapmamı gerektirebilirdi.

---

## 7. Bu Projeyi Sürdürürsem Bir Sonraki Adım Ne Olur?
TrustFleet projesini ticari veya endüstriyel bir ürüne dönüştürmek amacıyla sürdürmek istersem uygulayacağım sonraki adımlar:
1.  **Yapay Zeka Destekli Kamera İzleme (Computer Vision):** Şoförün yorgunluğunu sadece ses analizinden değil, araç içine yerleştirilecek bir mobil kamera yardımıyla **OpenCV (göz kırpma sıklığı ve esneme takibi)** algoritmaları üzerinden gerçek zamanlı izlemek.
2.  **Şoför Rolleri ve Vardiya Planlama:** Sisteme "Baş Şoför", "Operatör" ve "Yolcu İlişkileri Sorumlusu" gibi gelişmiş yetkilendirme rolleri ekleyerek şoför vardiya ve dinlenme saatlerini otomatik planlayan bir yapay zeka algoritması entegre etmek.
3.  **Mobil Uygulama Entegrasyonu:** Şoför ve Yolcu panellerini yerel mobil uygulamalara (Flutter/React Native) dönüştürerek acil durumlarda telefon kapalı olsa dahi arka planda panik butonu sinyalinin gönderilmesini sağlamak.

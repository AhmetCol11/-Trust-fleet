# AI Günlüğü (Vibe Coding Süreci)

Bu günlük, projenin AI ajanları ile nasıl geliştirildiğini, alınan mimari kararları ve çözülen hataları şeffaf bir şekilde belgelemek için tutulmaktadır.

## Oturum 2 — 21 Mayıs 2026 — 21:00-22:00

### Hedef
Modern bir Web Arayüzü (Frontend) tasarlanarak Flask mimarisine entegre edilmesi ve kullanıcı dostu bir deneyim sunulması.

### Yapılan İşlemler
- `base.html` şablonu oluşturularak tüm sayfalara ortak, temiz ve modern bir yapı kazandırıldı.
- `login.html` içerisinde Bootstrap 5 sekme (Tab) yapısı kullanılarak Yolcu, Şoför ve Admin (Merkez) girişleri tek bir sayfada birleştirildi.
- "Akıllı Ses Asistanı" entegrasyonu için JavaScript `setInterval` kullanılarak arka planda periyodik olarak çalışan ve sesi metne döken bir sistem geliştirildi.

## Oturum 3 — 22 Mayıs 2026

### Hedef
Projenin tamamen bağımsız, modüler ve güçlü bir Flask 3.x altyapısında çalışmasını sağlamak üzere arka plan (Backend) sisteminin sıfırdan tasarlanması ve geliştirilmesi.

### Kullandığım Mod ve Model
- Mod: Plan Modu
- Model: Gemini 3.1 Pro

### Yapılan İşlemler
1. Mimari Tasarım: Proje, `Blueprint` mimarisiyle parçalara ayrılarak (`auth`, `main`, `admin` vb.) profesyonel bir yapıya kavuşturuldu.
2. SQLAlchemy ORM Entegrasyonu: `models.py` tasarlanarak veri tabanı işlemleri nesne yönelimli hale getirildi. Veri tabanı sorguları güvenli (SQL Injection korumalı) yapıya taşındı.
3. Rota Geliştirmeleri: REST standartlarına uygun olarak API ve web yönlendirmeleri sıfırdan oluşturuldu.

*(Not: Geliştirme sürecindeki diğer başlıklar ve ekran görüntüleri proje ilerledikçe buraya eklenecektir.)*

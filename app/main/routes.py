from flask import render_template, flash, redirect, url_for, request, jsonify, session
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.main import bp
from app.models import Sofor, Alarm, SesLog, YolcuYorum, VardiyaSesKaydi
from app.auth.routes import yolcu_login_required

# Akıllı Türkçe Yorgunluk & Risk Analiz Motoru
def yorgunluk_analiz_et(metin):
    if not metin:
        return False
    metin_lower = metin.lower()
    
    # Yorgunluk/Risk belirten kelimeler
    yorgunluk_kelimeleri = ["yoruldum", "yorgun", "bitik", "halsiz", "uykusuz", "uyku", "uyuyakaldım", "kötüyüm", "halsizim", "bitkinim", "uykum", "zor", "ağrıyor"]
    
    # Negatif / Olumlu belirteçler (Aynı cümlede geçiyorsa riski temizler)
    negasyonlar = [
        "değil", "değilim", "yok", "iyiyim", "iyi", "dinç", 
        "sorunsuz", "sıkıntı yok", "sorun yok", "güzel", 
        "yaşamadım", "hissetmiyorum", "olmadı", "yoktur", "değildir"
    ]
    
    # Metni cümle veya ifadelere ayıralım
    cumleler = [c.strip() for c in metin_lower.replace('|', '.').replace(',', '.').split('.') if c.strip()]
    
    tehlikeli = False
    for cumle in cumleler:
        has_risk_word = False
        for k in yorgunluk_kelimeleri:
            if k in cumle:
                has_risk_word = True
                break
        
        if has_risk_word:
            # Olumlu ifade veya negasyon kontrolü
            has_negation = False
            for n in negasyonlar:
                if n in cumle:
                    has_negation = True
                    break
            
            # Eğer cümlede yorgunluk geçiyor ama olumlu/negatif bir belirteç YOKSA tehlikeli kabul et
            if not has_negation:
                tehlikeli = True
                break
                
    return tehlikeli

# Karşılaştırmalı Yorgunluk Analiz Motoru
def analiz_ve_karsilastirma_yap(sofor_id, baslangic, bitis):
    baslangic = baslangic or ""
    bitis = bitis or ""
    
    bas_kelime = len(baslangic.split())
    bit_kelime = len(bitis.split())
    
    bas_yorgunluk = yorgunluk_analiz_et(baslangic)
    bit_yorgunluk = yorgunluk_analiz_et(bitis)
    
    detaylar = []
    detaylar.append("🔍 <b>KARŞILAŞTIRMALI YORGUNLUK ANALİZ RAPORU</b>")
    detaylar.append(f"• Vardiya Başlangıç Ses Raporu: <i>\"{baslangic}\"</i> ({bas_kelime} kelime)")
    detaylar.append(f"• Vardiya Sonu Ses Raporu: <i>\"{bitis}\"</i> ({bit_kelime} kelime)")
    
    # Yorgunluk Durumu Tespiti
    durum = "İYİ"
    if bit_yorgunluk:
        durum = "KÖTÜ"
        detaylar.append("⚠️ <b>Risk Uyarısı:</b> Şoförün vardiya sonu konuşmasında yorgunluk/uyku belirten kelimeler tespit edildi.")
    elif bit_kelime < (bas_kelime * 0.5) and bas_kelime >= 3:
        durum = "KÖTÜ"
        detaylar.append("⚠️ <b>Risk Uyarısı:</b> Şoförün vardiya sonu yanıtı, başlangıca kıyasla aşırı derecede kısa sürdü (%50'den fazla düşüş). Dikkat eksikliği veya yorgunluk şüphesi.")
    
    # Önceki Günler ile Karşılaştırma
    gecmis = db.session.scalars(
        db.select(VardiyaSesKaydi)
        .filter(VardiyaSesKaydi.sofor_id == sofor_id, VardiyaSesKaydi.bitis_metni != None)
        .order_by(VardiyaSesKaydi.id.desc())
    ).all()
    
    # Listenin ilk elemanı şu an kaydetmekte olduğumuz kayıttır, o yüzden önceki kayıt için 1. indekse bakacağız (varsa)
    onceki_kayit = None
    if len(gecmis) > 1:
        onceki_kayit = gecmis[1]
    
    if onceki_kayit:
        onceki_bitis = onceki_kayit.bitis_metni or ""
        onceki_bit_kelime = len(onceki_bitis.split())
        
        detaylar.append("\n📊 <b>Önceki Günler ile Karşılaştırma Raporu:</b>")
        detaylar.append(f"• Dünkü Vardiya Sonu Söz Raporu: <i>\"{onceki_bitis}\"</i> ({onceki_bit_kelime} kelime)")
        
        if onceki_bit_kelime >= 15 and bit_kelime < onceki_bit_kelime * 0.5:
            detaylar.append("📉 <b>Konuşma Hızı Düşüşü:</b> Şoförün konuşma uzunluğu bir önceki güne kıyasla %50'den fazla azalmış. Enerji düşüklüğü ve uykusuzluk riski barizdir.")
            durum = "KÖTÜ"
        elif onceki_bit_kelime >= 15 and bit_kelime > onceki_bit_kelime * 1.3:
            detaylar.append("📈 <b>Konuşma Artışı:</b> Şoförün konuşma akıcılığı ve uzunluğu dünden daha fazla. Şoför dinç görünüyor.")
        else:
            detaylar.append("🔄 <b>Stabil Durum:</b> Şoförün konuşma uzunluğu ve kelime ritmi düne kıyasla paralel seyrediyor. Ciddi bir yorgunluk değişimi gözlemlenmedi.")
    else:
        detaylar.append("\nℹ️ <b>Referans Verisi:</b> Geçmiş günlere ait karşılaştırılacak veri bulunamadı. Bugünün verileri sonraki günler için baseline (referans) olarak kaydedildi.")
        
    return durum, "\n".join(detaylar)

# Periyodik Yorgunluk & Tepki Analiz Motoru
def periyodik_analiz_ve_karsilastirma_yap(sofor_id, metin):
    import re
    
    # 1. Metni ayrıştır ve temizle ("Soru 1: ... | Soru 2: ...")
    m = re.search(r"Soru 1:\s*(.*?)\s*\|\s*Soru 2:\s*(.*)", metin)
    if m:
        clean_text = m.group(1).strip() + " " + m.group(2).strip()
    else:
        clean_text = metin.strip()
        
    periyodik_kelime_sayisi = len(clean_text.split())
    
    # 2. Kelime bazlı yorgunluk / risk tespiti
    tehlikeli = yorgunluk_analiz_et(clean_text)
    
    durum = "İYİ"
    detaylar = []
    detaylar.append("🔍 <b>PERİYODİK DURUM ANALİZ RAPORU</b>")
    detaylar.append(f"• Mevcut Periyodik Beyan: <i>\"{clean_text}\"</i> ({periyodik_kelime_sayisi} kelime)")
    
    if tehlikeli:
        durum = "KÖTÜ"
        detaylar.append("⚠️ <b>Risk Tespiti:</b> Konuşmada yorgunluk veya risk belirten anahtar kelimeler algılandı.")
        
    # 3. Vardiya Başlangıcı ile Karşılaştır
    son_shift = db.session.scalar(
        db.select(VardiyaSesKaydi)
        .filter_by(sofor_id=sofor_id)
        .order_by(VardiyaSesKaydi.id.desc())
    )
    
    if son_shift and son_shift.baslangic_metni:
        baslangic_metni = son_shift.baslangic_metni
        baslangic_kelime_sayisi = len(baslangic_metni.split())
        if baslangic_kelime_sayisi >= 3:
            oran = periyodik_kelime_sayisi / baslangic_kelime_sayisi
            detaylar.append(f"• Vardiya Giriş Raporu: <i>\"{baslangic_metni}\"</i> ({baslangic_kelime_sayisi} kelime) | Oran: <b>%{oran*100:.0f}</b>")
            if oran < 0.5:
                durum = "RİSKLİ"
                detaylar.append("⚠️ <b>Vardiya Girişine Göre Düşüş:</b> Konuşma uzunluğu vardiya başlangıcına kıyasla %50'den fazla azaldı! Odaklanma veya yorgunluk şüphesi.")
                
    # 4. Önceki Periyodik Kontrollerle Karşılaştır
    gecmis_loglar = db.session.scalars(
        db.select(SesLog)
        .filter(SesLog.sofor_id == sofor_id)
        .order_by(SesLog.log_id.desc())
        .limit(3)
    ).all()
    
    prev_word_counts = []
    for log in gecmis_loglar:
        prev_metin = log.metin
        m_prev = re.search(r"Soru 1:\s*(.*?)\s*\|\s*Soru 2:\s*(.*)", prev_metin)
        prev_text = m_prev.group(1).strip() + " " + m_prev.group(2).strip() if m_prev else prev_metin.strip()
        prev_word_counts.append(len(prev_text.split()))
        
    if prev_word_counts:
        avg_prev = sum(prev_word_counts) / len(prev_word_counts)
        detaylar.append(f"• Önceki Periyodik Kayıtların Ortalama Kelime Sayısı: <b>{avg_prev:.1f}</b>")
        if avg_prev >= 3 and periyodik_kelime_sayisi < avg_prev * 0.5:
            if durum != "KÖTÜ":
                durum = "RİSKLİ"
            detaylar.append("📉 <b>Periyodik Düşüş Eğilimi:</b> Konuşma uzunluğu önceki periyodik kontrollere kıyasla %50'den fazla düştü! Enerji düşüklüğü ve uykusuzluk riski.")
            
    if durum == "İYİ":
        detaylar.append("✅ <b>Durum Stabil:</b> Şoförün konuşma ritmi ve uzunluğu standart seviyede. Yorgunluk saptanmadı.")
        
    return durum, "<br>".join(detaylar)

@bp.route('/index')
@login_required
def index():
    # Şoförün en son vardiya kaydını bulup bitiş metninin boş olup olmadığına göre aktifliği kontrol edelim
    son_shift = db.session.scalar(
        db.select(VardiyaSesKaydi)
        .filter_by(sofor_id=current_user.id)
        .order_by(VardiyaSesKaydi.id.desc())
    )
    vardiya_aktif = False
    if son_shift and son_shift.baslangic_metni and not son_shift.bitis_metni:
        vardiya_aktif = True
    return render_template('index.html', title='Şoför Paneli', vardiya_aktif=vardiya_aktif)

@bp.route('/api/alarm_ekle', methods=['POST'])
@login_required
def alarm_ekle():
    data = request.json
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alarm = Alarm(sofor_id=current_user.id, durum_bilgi=data.get('sebep', 'PANİK BUTONU!'), alarm_tipi="ACİL DURUM", tarih_saat=simdi)
    db.session.add(alarm)
    db.session.commit()
    return jsonify({"success": True})

@bp.route('/api/ses_kaydet', methods=['POST'])
@login_required
def ses_kaydet():
    data = request.json
    metin = data.get('metin', '')
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Yeni karşılaştırmalı durum ve yorgunluk analizi
    durum, detay = periyodik_analiz_ve_karsilastirma_yap(current_user.id, metin)
    
    log = SesLog(
        sofor_id=current_user.id, 
        metin=metin, 
        tarih_saat=simdi,
        analiz_sonucu=durum,
        analiz_detay=detay
    )
    db.session.add(log)
    
    alert_triggered = False
    alert_message = ""
    if durum in ["KÖTÜ", "RİSKLİ"]:
        alert_triggered = True
        alert_message = f"⚠️ Dikkat! Periyodik kontrolde risk ({durum}) tespit edildi. Acil durum alarmı merkeze iletiliyor!"
        
        # Temiz metni durum bilgisinde göstermek için Soru 1 ve 2'yi ayrıştırıp özetleyelim
        import re
        m = re.search(r"Soru 1:\s*(.*?)\s*\|\s*Soru 2:\s*(.*)", metin)
        clean_msg = m.group(1).strip() + " " + m.group(2).strip() if m else metin
        
        alarm = Alarm(
            sofor_id=current_user.id,
            durum_bilgi=f"Akıllı asistan periyodik kontrol risk ({durum}) saptadı: '{clean_msg[:120]}'",
            alarm_tipi="ASİSTAN ALARMI",
            tarih_saat=simdi
        )
        db.session.add(alarm)
        
    db.session.commit()
    return jsonify({
        "success": True, 
        "alert_triggered": alert_triggered, 
        "alert_message": alert_message,
        "analiz_sonucu": durum,
        "analiz_detay": detay
    })


@bp.route('/api/vardiya_baslat', methods=['POST'])
@login_required
def vardiya_baslat():
    data = request.json
    metin = data.get('metin', '')
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    shift = VardiyaSesKaydi(
        sofor_id=current_user.id,
        baslangic_metni=metin,
        analiz_sonucu="BAŞLATILDI",
        analiz_detay="Vardiya başlangıç kaydı alındı. Gün içi kontroller bekleniyor.",
        tarih_saat=simdi
    )
    db.session.add(shift)
    db.session.commit()
    return jsonify({"success": True})

@bp.route('/api/vardiya_bitir', methods=['POST'])
@login_required
def vardiya_bitir():
    data = request.json
    metin = data.get('metin', '')
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Şoförün son aktif vardiya kaydını bul
    shift = db.session.scalar(
        db.select(VardiyaSesKaydi)
        .filter_by(sofor_id=current_user.id)
        .order_by(VardiyaSesKaydi.id.desc())
    )
    
    if not shift:
        shift = VardiyaSesKaydi(
            sofor_id=current_user.id,
            baslangic_metni="Vardiya başlangıcında ses kaydı alınamadı.",
            analiz_sonucu="TAMAMLANDI",
            analiz_detay="Başlangıç kaydı olmadan bitirildi.",
            tarih_saat=simdi
        )
        db.session.add(shift)
        
    shift.bitis_metni = metin
    durum, detay = analiz_ve_karsilastirma_yap(current_user.id, shift.baslangic_metni, metin)
    shift.analiz_sonucu = durum
    shift.analiz_detay = detay
    db.session.commit()
    
    return jsonify({
        "success": True, 
        "analiz_sonucu": durum, 
        "analiz_detay": detay
    })

@bp.route('/yolcu_plaka_sorgula', methods=['GET', 'POST'])
@yolcu_login_required
def yolcu_plaka_sorgula():
    if request.method == 'POST':
        plaka = request.form.get('plaka', '').strip().upper()
        if not plaka:
            flash('Lütfen otobüs plakasını girin.', 'danger')
            return redirect(url_for('main.yolcu_plaka_sorgula'))
            
        sofor = db.session.scalar(db.select(Sofor).filter_by(arac_plaka=plaka))
        if sofor:
            return redirect(url_for('main.yolcu_panel', sofor_id=sofor.id))
        else:
            flash('Bu plakaya ait aktif bir otobüs/sefer bulunamadı.', 'danger')
            
    soforler = db.session.scalars(db.select(Sofor)).all()
    return render_template('yolcu_plaka_sorgula.html', title='Otobüs Sorgula', soforler=soforler)

@bp.route('/yolcu/<int:sofor_id>', methods=['GET', 'POST'])
@yolcu_login_required
def yolcu_panel(sofor_id):
    sofor = db.session.get(Sofor, sofor_id)
    if not sofor:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        puan = int(request.form.get('puan', 5))
        etiketler = request.form.get('etiketler', '')
        serbest_yorum = request.form.get('serbest_yorum', '')
        simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        yorum = YolcuYorum(
            sofor_id=sofor_id,
            yolcu_id=session.get('yolcu_id'),
            puan=puan,
            etiketler=etiketler,
            serbest_yorum=serbest_yorum,
            tarih_saat=simdi
        )
        db.session.add(yorum)
        db.session.commit()
        flash('Geri bildiriminiz başarıyla merkeze iletildi. Katkılarınız için teşekkür ederiz!', 'success')
        return redirect(url_for('main.yolcu_panel', sofor_id=sofor_id))

    return render_template('yolcu.html', title='Yolcu Paneli', sofor=sofor)

@bp.route('/api/yolcu_alarm_ekle/<int:sofor_id>', methods=['POST'])
@yolcu_login_required
def yolcu_alarm_ekle(sofor_id):
    sofor = db.session.get(Sofor, sofor_id)
    if not sofor:
        return jsonify({"success": False, "error": "Şoför bulunamadı"}), 404
        
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alarm = Alarm(
        sofor_id=sofor_id, 
        durum_bilgi=f"Yolcu ({session.get('yolcu_ad')}) tarafından Acil Durum/Tehlike Bildirimi yapıldı!", 
        alarm_tipi="YOLCU ACİL ALARMI", 
        tarih_saat=simdi
    )
    db.session.add(alarm)
    db.session.commit()
    return jsonify({"success": True})

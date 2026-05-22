from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.main import bp
from app.models import Sofor, Alarm, SesLog, YolcuYorum, VardiyaSesKaydi

# Karşılaştırmalı Yorgunluk Analiz Motoru
def analiz_ve_karsilastirma_yap(sofor_id, baslangic, bitis):
    yorgunluk_kelimeleri = ["yoruldum", "yorgun", "çok yoruldum", "bitik", "halsiz", "uyku", "uyuyakaldım", "kötüyüm", "halsizim", "bitkinim", "uykum var", "zor", "ağrıyor", "bitti"]
    
    baslangic = baslangic or ""
    bitis = bitis or ""
    
    bas_kelime = len(baslangic.split())
    bit_kelime = len(bitis.split())
    
    bas_yorgunluk = any(k in baslangic.lower() for k in yorgunluk_kelimeleri)
    bit_yorgunluk = any(k in bitis.lower() for k in yorgunluk_kelimeleri)
    
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
        
        if bit_kelime < onceki_bit_kelime * 0.7:
            detaylar.append("📉 <b>Konuşma Hızı Düşüşü:</b> Şoförün konuşma uzunluğu bir önceki güne kıyasla %30'dan fazla azalmış. Enerji düşüklüğü ve uykusuzluk riski barizdir.")
            durum = "KÖTÜ"
        elif bit_kelime > onceki_bit_kelime * 1.3:
            detaylar.append("📈 <b>Konuşma Artışı:</b> Şoförün konuşma akıcılığı ve uzunluğu dünden daha fazla. Şoför dinç görünüyor.")
        else:
            detaylar.append("🔄 <b>Stabil Durum:</b> Şoförün konuşma uzunluğu ve kelime ritmi düne kıyasla paralel seyrediyor. Ciddi bir yorgunluk değişimi gözlemlenmedi.")
    else:
        detaylar.append("\nℹ️ <b>Referans Verisi:</b> Geçmiş günlere ait karşılaştırılacak veri bulunamadı. Bugünün verileri sonraki günler için baseline (referans) olarak kaydedildi.")
        
    return durum, "\n".join(detaylar)

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
    
    # Yorgunluk/Risk analizi
    yorgunluk_kelimeleri = ["yoruldum", "yorgun", "çok yoruldum", "bitik", "halsiz", "uyku", "uyuyakaldım", "kötüyüm", "halsizim", "bitkinim", "uykum var"]
    tehlikeli = any(k in metin.lower() for k in yorgunluk_kelimeleri)
    
    log = SesLog(sofor_id=current_user.id, metin=metin, tarih_saat=simdi)
    db.session.add(log)
    
    alert_triggered = False
    alert_message = ""
    if tehlikeli:
        alert_triggered = True
        alert_message = "⚠️ Dikkat! Yorgunluk veya risk tespit edildi. Acil durum alarmı merkeze iletiliyor!"
        alarm = Alarm(
            sofor_id=current_user.id,
            durum_bilgi=f"Akıllı asistan periyodik ses kontrolünde yorgunluk/risk tespit etti: '{metin}'",
            alarm_tipi="ASİSTAN ALARMI",
            tarih_saat=simdi
        )
        db.session.add(alarm)
        
    db.session.commit()
    return jsonify({
        "success": True, 
        "alert_triggered": alert_triggered, 
        "alert_message": alert_message
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

@bp.route('/yolcu/<int:sofor_id>', methods=['GET', 'POST'])
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
def yolcu_alarm_ekle(sofor_id):
    sofor = db.session.get(Sofor, sofor_id)
    if not sofor:
        return jsonify({"success": False, "error": "Şoför bulunamadı"}), 404
        
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alarm = Alarm(
        sofor_id=sofor_id, 
        durum_bilgi="Yolcu tarafından Acil Durum/Tehlike Bildirimi yapıldı!", 
        alarm_tipi="YOLCU ACİL ALARMI", 
        tarih_saat=simdi
    )
    db.session.add(alarm)
    db.session.commit()
    return jsonify({"success": True})

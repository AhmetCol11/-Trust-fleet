from flask import request, jsonify
from datetime import datetime
from app import db
from app.api import bp
from app.models import Sofor, Alarm, SesLog, VardiyaSesKaydi, YolcuYorum, AracKonum

# ==============================================================================
# ŞOFÖR İŞLEMLERİ
# ==============================================================================

@bp.route('/sofor/login', methods=['POST'])
def sofor_login():
    data = request.json
    kullanici_adi = data.get('kullanici_adi')
    sifre = data.get('sifre')
    
    if not kullanici_adi or not sifre:
        return jsonify({"success": False, "message": "Kullanıcı adı ve şifre gereklidir."}), 400
        
    sofor = db.session.scalar(db.select(Sofor).filter_by(kullanici_adi=kullanici_adi))
    if sofor and sofor.check_password(sifre):
        return jsonify({"success": True, "data": sofor.to_dict()}), 200
    else:
        return jsonify({"success": False, "message": "Geçersiz kullanıcı adı veya şifre."}), 401

@bp.route('/sofor/konum_guncelle', methods=['POST'])
def konum_guncelle():
    data = request.json
    sofor_id = data.get('sofor_id')
    enlem = data.get('enlem')
    boylam = data.get('boylam')
    
    if not sofor_id or enlem is None or boylam is None:
        return jsonify({"success": False, "message": "sofor_id, enlem ve boylam gereklidir."}), 400
        
    konum = db.session.get(AracKonum, sofor_id)
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if konum:
        konum.enlem = enlem
        konum.boylam = boylam
        konum.son_guncelleme = simdi
    else:
        konum = AracKonum(sofor_id=sofor_id, enlem=enlem, boylam=boylam, son_guncelleme=simdi)
        db.session.add(konum)
    
    db.session.commit()
    return jsonify({"success": True, "message": "Konum başarıyla güncellendi."}), 200

@bp.route('/sofor/alarm_olustur', methods=['POST'])
def alarm_olustur():
    data = request.json
    sofor_id = data.get('sofor_id')
    durum_bilgi = data.get('durum_bilgi', 'ACİL DURUM')
    alarm_tipi = data.get('alarm_tipi', 'MOBIL_PANIK_BUTONU')
    
    if not sofor_id:
        return jsonify({"success": False, "message": "sofor_id gereklidir."}), 400
        
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alarm = Alarm(sofor_id=sofor_id, durum_bilgi=durum_bilgi, alarm_tipi=alarm_tipi, tarih_saat=simdi)
    db.session.add(alarm)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Alarm merkeze iletildi.", "zaman": simdi}), 201

@bp.route('/sofor/ses_log_ekle', methods=['POST'])
def ses_log_ekle():
    data = request.json
    sofor_id = data.get('sofor_id')
    metin = data.get('metin')
    
    if not sofor_id or not metin:
        return jsonify({"success": False, "message": "sofor_id ve metin gereklidir."}), 400
        
    log = SesLog(sofor_id=sofor_id, metin=metin)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Ses logu eklendi."}), 201

@bp.route('/sofor/vardiya_analizi_kaydet', methods=['POST'])
def vardiya_analiz_kaydet():
    data = request.json
    sofor_id = data.get('sofor_id')
    baslangic_metni = data.get('baslangic_metni', '')
    bitis_metni = data.get('bitis_metni', '')
    analiz_sonucu = data.get('analiz_sonucu')
    analiz_detay = data.get('analiz_detay', '')
    
    if not sofor_id or not analiz_sonucu:
        return jsonify({"success": False, "message": "sofor_id ve analiz_sonucu gereklidir."}), 400
        
    kayit = VardiyaSesKaydi(
        sofor_id=sofor_id, 
        baslangic_metni=baslangic_metni, 
        bitis_metni=bitis_metni, 
        analiz_sonucu=analiz_sonucu, 
        analiz_detay=analiz_detay
    )
    db.session.add(kayit)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Vardiya analizi kaydedildi."}), 201


# ==============================================================================
# YOLCU İŞLEMLERİ
# ==============================================================================

@bp.route('/yolcu/login', methods=['POST'])
def yolcu_login():
    data = request.json
    plaka = data.get('plaka')
    
    if not plaka:
        return jsonify({"success": False, "message": "Plaka gereklidir."}), 400
        
    sofor = db.session.scalar(db.select(Sofor).filter_by(arac_plaka=plaka.strip()))
    if sofor:
        return jsonify({"success": True, "data": sofor.to_dict()}), 200
    else:
        return jsonify({"success": False, "message": "Bu plakaya ait kayıtlı şoför/araç bulunamadı."}), 404

@bp.route('/yolcu/yorum_ekle', methods=['POST'])
def yolcu_yorum_ekle():
    data = request.json
    sofor_id = data.get('sofor_id')
    puan = data.get('puan')
    etiketler = data.get('etiketler', '')
    serbest_yorum = data.get('serbest_yorum', '')
    
    if not sofor_id or not puan:
        return jsonify({"success": False, "message": "sofor_id ve puan gereklidir."}), 400
        
    yorum = YolcuYorum(
        sofor_id=sofor_id, 
        puan=puan, 
        etiketler=etiketler, 
        serbest_yorum=serbest_yorum
    )
    db.session.add(yorum)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Yorumunuz başarıyla kaydedildi. Teşekkür ederiz."}), 201


# ==============================================================================
# ADMİN İŞLEMLERİ (MERKEZ)
# ==============================================================================

@bp.route('/admin/alarmlar', methods=['GET'])
def admin_alarmlar():
    alarmlar = db.session.scalars(db.select(Alarm).order_by(Alarm.alarm_id.desc())).all()
    return jsonify({"success": True, "data": [a.to_dict() for a in alarmlar]}), 200

@bp.route('/admin/ses_loglari', methods=['GET'])
def admin_ses_loglari():
    loglar = db.session.scalars(db.select(SesLog).order_by(SesLog.log_id.desc())).all()
    return jsonify({"success": True, "data": [l.to_dict() for l in loglar]}), 200

@bp.route('/admin/vardiya_kayitlari', methods=['GET'])
def admin_vardiya_kayitlari():
    kayitlar = db.session.scalars(db.select(VardiyaSesKaydi).order_by(VardiyaSesKaydi.id.desc())).all()
    return jsonify({"success": True, "data": [k.to_dict() for k in kayitlar]}), 200

@bp.route('/admin/yolcu_yorumlari', methods=['GET'])
def admin_yolcu_yorumlari():
    yorumlar = db.session.scalars(db.select(YolcuYorum).order_by(YolcuYorum.id.desc())).all()
    return jsonify({"success": True, "data": [y.to_dict() for y in yorumlar]}), 200

@bp.route('/admin/konumlar', methods=['GET'])
def admin_konumlar():
    konumlar = db.session.scalars(db.select(AracKonum)).all()
    return jsonify({"success": True, "data": [k.to_dict() for k in konumlar]}), 200

@bp.route('/admin/soforler', methods=['GET'])
def admin_soforler():
    soforler = db.session.scalars(db.select(Sofor)).all()
    return jsonify({"success": True, "data": [s.to_dict() for s in soforler]}), 200

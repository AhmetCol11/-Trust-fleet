from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.main import bp
from app.models import Sofor, Alarm, SesLog

def yorgunluk_analizi_yap(baslangic_metni: str, bitis_metni: str, baslangic_suresi: float = 1.0, bitis_suresi: float = 1.0):
    yorgunluk_kelimeleri = ["yoruldum", "yorgun", "çok yoruldum", "bitik", "halsiz", "uyku", "uyuyakaldım"]
    bas_kelime = len(baslangic_metni.split()) if baslangic_metni else 0
    bit_kelime = len(bitis_metni.split()) if bitis_metni else 0
    bas_hiz = bas_kelime / baslangic_suresi if baslangic_suresi > 0 else 0
    bit_hiz = bit_kelime / bitis_suresi if bitis_suresi > 0 else 0
    tehlikeli = any(k in bitis_metni.lower() for k in yorgunluk_kelimeleri)
    cok_kisa = bit_kelime < 2
    oransal_yorgunluk = (bas_hiz > 0.5) and (bit_hiz < (bas_hiz * 0.75))
    mutlak_yorgunluk = (bit_hiz > 0) and (bit_hiz < 0.9)

    if tehlikeli:
        return "KÖTÜ", f"⚠️ Tehlike ifadesi algılandı: '{bitis_metni[:60]}'"
    elif oransal_yorgunluk:
        return "KÖTÜ", f"⚠️ Konuşma hızınızda belirgin bir düşüş var. Yorgunluk belirtisi."
    elif mutlak_yorgunluk:
        return "KÖTÜ", f"⚠️ Konuşma hızınız çok yavaş. Dikkat eksikliği riski."
    elif cok_kisa:
        return "KÖTÜ", f"⚠️ Vardiya sonu yanıtı çok kısa — yorgunluk şüphesi."
    return "İYİ", "✅ Şoför dinç. Ses ritmi ve konuşma hızı normal."

@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Şoför Paneli')

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
    log = SesLog(sofor_id=current_user.id, metin=metin, tarih_saat=simdi)
    db.session.add(log)
    db.session.commit()
    return jsonify({"success": True})

@bp.route('/yolcu/<int:sofor_id>')
def yolcu_panel(sofor_id):
    sofor = db.session.get(Sofor, sofor_id)
    if not sofor:
        return redirect(url_for('auth.login'))
    return render_template('yolcu.html', title='Yolcu Paneli', sofor=sofor)

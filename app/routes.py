from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from datetime import datetime
from app import app, db
from app.forms import LoginForm, YolcuSorguForm
from app.models import Sofor, Alarm, SesLog, VardiyaSesKaydi, YolcuYorum, AracKonum

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

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    yolcu_form = YolcuSorguForm()
    
    if form.validate_on_submit() and request.form.get('login_type') == 'sofor':
        user = db.session.scalar(db.select(Sofor).filter_by(kullanici_adi=form.kullanici_adi.data))
        if user is None or not user.check_password(form.sifre.data):
            flash('Geçersiz kullanıcı adı veya şifre')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    if request.method == 'POST' and request.form.get('login_type') == 'admin':
        if request.form.get('kullanici_adi') == 'admin' and request.form.get('sifre') == 'admin123':
            return redirect(url_for('admin_panel'))
        else:
            flash('Admin bilgileri hatalı')

    if yolcu_form.validate_on_submit() and request.form.get('login_type') == 'yolcu':
        user = db.session.scalar(db.select(Sofor).filter_by(arac_plaka=yolcu_form.plaka.data))
        if user:
            return redirect(url_for('yolcu_panel', sofor_id=user.id))
        else:
            flash('Bu plakaya ait sefer bulunamadı.')
            
    return render_template('login.html', title='Giriş', form=form, yolcu_form=yolcu_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Şoför Paneli')

@app.route('/api/alarm_ekle', methods=['POST'])
@login_required
def alarm_ekle():
    data = request.json
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alarm = Alarm(sofor_id=current_user.id, durum_bilgi=data.get('sebep', 'PANİK BUTONU!'), alarm_tipi="ACİL DURUM", tarih_saat=simdi)
    db.session.add(alarm)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/ses_kaydet', methods=['POST'])
@login_required
def ses_kaydet():
    data = request.json
    metin = data.get('metin', '')
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = SesLog(sofor_id=current_user.id, metin=metin, tarih_saat=simdi)
    db.session.add(log)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/admin')
def admin_panel():
    alarmlar = db.session.scalars(db.select(Alarm).order_by(Alarm.alarm_id.desc())).all()
    loglar = db.session.scalars(db.select(SesLog).order_by(SesLog.log_id.desc())).all()
    return render_template('admin.html', title='Merkez Yönetim', alarmlar=alarmlar, loglar=loglar)

@app.route('/yolcu/<int:sofor_id>')
def yolcu_panel(sofor_id):
    sofor = db.session.get(Sofor, sofor_id)
    if not sofor:
        return redirect(url_for('login'))
    return render_template('yolcu.html', title='Yolcu Paneli', sofor=sofor)

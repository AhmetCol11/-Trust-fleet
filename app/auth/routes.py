from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit
from functools import wraps
import hashlib
import secrets
from app import db
from app.auth import bp
from app.forms import LoginForm, YolcuSorguForm
from app.models import Sofor, Yolcu

# Yolcu login_required decorator'ı
def yolcu_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'yolcu_id' not in session:
            flash('Bu sayfayı görmek için lütfen yolcu girişi yapın.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if 'yolcu_id' in session:
        return redirect(url_for('main.yolcu_plaka_sorgula'))
        
    form = LoginForm()
    yolcu_form = YolcuSorguForm()
    
    if form.validate_on_submit() and request.form.get('login_type') == 'sofor':
        user = db.session.scalar(db.select(Sofor).filter_by(kullanici_adi=form.kullanici_adi.data))
        if user is None or not user.check_password(form.sifre.data):
            flash('Geçersiz kullanıcı adı veya şifre')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    if request.method == 'POST' and request.form.get('login_type') == 'admin':
        if request.form.get('kullanici_adi') == 'admin' and request.form.get('sifre') == 'admin123':
            return redirect(url_for('admin.admin_panel'))
        else:
            flash('Admin bilgileri hatalı')

    # Yolcu E-posta & Şifre Giriş Doğrulaması
    if request.method == 'POST' and request.form.get('login_type') == 'yolcu':
        email = request.form.get('yolcu_email')
        sifre = request.form.get('yolcu_sifre')
        
        yolcu = db.session.scalar(db.select(Yolcu).filter_by(email=email))
        if yolcu is None or not yolcu.check_password(sifre):
            flash('Geçersiz e-posta veya şifre', 'danger')
            return redirect(url_for('auth.login'))
            
        session['yolcu_id'] = yolcu.id
        session['yolcu_email'] = yolcu.email
        session['yolcu_ad'] = yolcu.ad_soyad
        
        flash(f'Hoş geldiniz, {yolcu.ad_soyad}!', 'success')
        return redirect(url_for('main.yolcu_plaka_sorgula'))
            
    return render_template('login.html', title='Giriş', form=form, yolcu_form=yolcu_form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/yolcu_logout')
def yolcu_logout():
    session.pop('yolcu_id', None)
    session.pop('yolcu_email', None)
    session.pop('yolcu_ad', None)
    flash('Yolcu oturumu başarıyla kapatıldı.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/yolcu_kayit', methods=['GET', 'POST'])
def yolcu_kayit():
    if 'yolcu_id' in session:
        return redirect(url_for('main.yolcu_plaka_sorgula'))
        
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        email = request.form.get('email')
        sifre = request.form.get('sifre')
        
        if not ad_soyad or not email or not sifre:
            flash('Lütfen tüm alanları doldurun.', 'danger')
            return redirect(url_for('auth.yolcu_kayit'))
            
        existing = db.session.scalar(db.select(Yolcu).filter_by(email=email))
        if existing:
            flash('Bu e-posta adresiyle zaten kayıt yapılmış.', 'danger')
            return redirect(url_for('auth.yolcu_kayit'))
            
        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        yolcu = Yolcu(ad_soyad=ad_soyad, email=email, sifre_hash=sifre_hash, sifre_plain=sifre)
        db.session.add(yolcu)
        db.session.commit()
        
        flash('Kaydınız başarıyla tamamlandı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('yolcu_kayit.html', title='Yolcu Kayıt')

@bp.route('/yolcu_sifre_sifirla', methods=['GET', 'POST'])
def yolcu_sifre_sifirla():
    if request.method == 'POST':
        email = request.form.get('email')
        yolcu = db.session.scalar(db.select(Yolcu).filter_by(email=email))
        
        if yolcu:
            token = secrets.token_hex(16)
            yolcu.reset_token = token
            db.session.commit()
            
            # Akademik/Demo Modunda Linki Konsola Yazdır
            reset_url = url_for('auth.yolcu_sifre_yenile', token=token, _external=True)
            print("\n" + "="*80)
            print("🔑 [AKADEMİK/DEMO ŞİFRE SIFIRLAMA E-POSTASI]")
            print(f"Alıcı: {yolcu.ad_soyad} ({email})")
            print(f"Şifre Sıfırlama Linki: {reset_url}")
            print("="*80 + "\n")
            
            flash('Şifre sıfırlama linki e-posta adresinize gönderildi (Demo modunda terminal konsoluna yazdırılmıştır).', 'success')
            return render_template('yolcu_sifre_sifirla.html', title='Şifre Sıfırlama', email_sent=True, reset_url=reset_url)
        else:
            flash('Bu e-posta adresiyle kayıtlı bir yolcu bulunamadı.', 'danger')
            
    return render_template('yolcu_sifre_sifirla.html', title='Şifre Sıfırlama', email_sent=False)

@bp.route('/yolcu_sifre_yenile/<token>', methods=['GET', 'POST'])
def yolcu_sifre_yenile(token):
    yolcu = db.session.scalar(db.select(Yolcu).filter_by(reset_token=token))
    if not yolcu:
        flash('Geçersiz veya süresi dolmuş sıfırlama token\'ı.', 'danger')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        yeni_sifre = request.form.get('sifre')
        if not yeni_sifre:
            flash('Lütfen geçerli bir şifre girin.', 'danger')
            return redirect(url_for('auth.yolcu_sifre_yenile', token=token))
            
        yolcu.sifre_hash = hashlib.sha256(yeni_sifre.encode()).hexdigest()
        yolcu.sifre_plain = yeni_sifre
        yolcu.reset_token = None
        db.session.commit()
        
        flash('Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('yolcu_sifre_yenile.html', title='Yeni Şifre Belirle', token=token)


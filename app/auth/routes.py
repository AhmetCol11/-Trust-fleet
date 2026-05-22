from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit
from app import db
from app.auth import bp
from app.forms import LoginForm, YolcuSorguForm
from app.models import Sofor

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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

    if yolcu_form.validate_on_submit() and request.form.get('login_type') == 'yolcu':
        user = db.session.scalar(db.select(Sofor).filter_by(arac_plaka=yolcu_form.plaka.data))
        if user:
            return redirect(url_for('main.yolcu_panel', sofor_id=user.id))
        else:
            flash('Bu plakaya ait sefer bulunamadı.')
            
    return render_template('login.html', title='Giriş', form=form, yolcu_form=yolcu_form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

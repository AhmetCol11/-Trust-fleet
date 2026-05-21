from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import SoforEkleForm, AlarmEkleForm
from app.models import Sofor, Alarm

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        sofor = current_user.sofor_profili
        alarmlar = sofor.alarmlar if sofor else []
        return render_template('index.html', title='Anasayfa', sofor=sofor, alarmlar=alarmlar)
    return render_template('index.html', title='Hoşgeldiniz')

@bp.route('/sofor_ekle', methods=['GET', 'POST'])
@login_required
def sofor_ekle():
    if current_user.sofor_profili:
        flash('Zaten bir şoför profiliniz var.', 'info')
        return redirect(url_for('main.index'))
        
    form = SoforEkleForm()
    if form.validate_on_submit():
        try:
            sofor = Sofor(
                ad_soyad=form.ad_soyad.data,
                tc_kimlik=form.tc_kimlik.data,
                user=current_user
            )
            db.session.add(sofor)
            db.session.commit()
            flash('Şoför profiliniz başarıyla oluşturuldu!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
            
    return render_template('main/sofor_ekle.html', title='Şoför Profili Oluştur', form=form)

@bp.route('/alarm_ekle', methods=['GET', 'POST'])
@login_required
def alarm_ekle():
    if not current_user.sofor_profili:
        flash('Alarm eklemek için önce şoför profili oluşturmalısınız.', 'danger')
        return redirect(url_for('main.sofor_ekle'))
        
    form = AlarmEkleForm()
    if form.validate_on_submit():
        alarm = Alarm(
            alarm_turu=form.alarm_turu.data,
            sofor=current_user.sofor_profili
        )
        db.session.add(alarm)
        db.session.commit()
        flash('Acil durum alarmı sisteme kaydedildi.', 'warning')
        return redirect(url_for('main.index'))
        
    return render_template('main/alarm_ekle.html', title='Alarm Bildir', form=form)

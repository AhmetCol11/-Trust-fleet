from flask import render_template, jsonify
from flask_login import login_required
from app import db
from app.admin import bp
from app.models import Alarm, SesLog, YolcuYorum, VardiyaSesKaydi, Sofor, AracKonum

@bp.route('/admin')
def admin_panel():
    alarmlar = db.session.scalars(db.select(Alarm).order_by(Alarm.alarm_id.desc())).all()
    loglar = db.session.scalars(db.select(SesLog).order_by(SesLog.log_id.desc())).all()
    yorumlar = db.session.scalars(db.select(YolcuYorum).order_by(YolcuYorum.id.desc())).all()
    vardiya_kayitlari = db.session.scalars(db.select(VardiyaSesKaydi).order_by(VardiyaSesKaydi.id.desc())).all()
    soforler = db.session.scalars(db.select(Sofor).order_by(Sofor.ad)).all()
    return render_template('admin.html', title='Merkez Yönetim', alarmlar=alarmlar, loglar=loglar, yorumlar=yorumlar, vardiya_kayitlari=vardiya_kayitlari, soforler=soforler)

@bp.route('/api/admin/konumlar', methods=['GET'])
def admin_konumlar():
    konumlar = db.session.scalars(db.select(AracKonum)).all()
    return jsonify({
        "success": True,
        "data": [k.to_dict() for k in konumlar]
    })


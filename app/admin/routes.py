from flask import render_template, jsonify, request
from flask_login import login_required
from app import db
from app.admin import bp
from app.models import Alarm, SesLog, YolcuYorum, VardiyaSesKaydi, Sofor, AracKonum

PER_PAGE = 10  # Sayfa başına kayıt sayısı


@bp.route('/admin')
def admin_panel():
    # Sayfalama için page parametresini al
    alarm_sayfa = request.args.get('alarm_sayfa', 1, type=int)
    log_sayfa = request.args.get('log_sayfa', 1, type=int)

    # Alarmlar — sayfalı sorgu (paginate)
    alarmlar_pagination = db.paginate(
        db.select(Alarm).order_by(Alarm.alarm_id.desc()),
        page=alarm_sayfa,
        per_page=PER_PAGE,
        error_out=False
    )

    # Ses logları — sayfalı sorgu (paginate)
    loglar_pagination = db.paginate(
        db.select(SesLog).order_by(SesLog.log_id.desc()),
        page=log_sayfa,
        per_page=PER_PAGE,
        error_out=False
    )

    # Diğer listeler (sayfalama gerektirmiyor — az kayıt)
    yorumlar = db.session.scalars(db.select(YolcuYorum).order_by(YolcuYorum.id.desc())).all()
    vardiya_kayitlari = db.session.scalars(db.select(VardiyaSesKaydi).order_by(VardiyaSesKaydi.id.desc())).all()
    soforler = db.session.scalars(db.select(Sofor).order_by(Sofor.ad)).all()

    return render_template(
        'admin.html',
        title='Merkez Yönetim',
        alarmlar=alarmlar_pagination.items,
        alarmlar_pagination=alarmlar_pagination,
        loglar=loglar_pagination.items,
        loglar_pagination=loglar_pagination,
        yorumlar=yorumlar,
        vardiya_kayitlari=vardiya_kayitlari,
        soforler=soforler
    )


@bp.route('/api/admin/konumlar', methods=['GET'])
def admin_konumlar():
    konumlar = db.session.scalars(db.select(AracKonum)).all()
    return jsonify({
        "success": True,
        "data": [k.to_dict() for k in konumlar]
    })

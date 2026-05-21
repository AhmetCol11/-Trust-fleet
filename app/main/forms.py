from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlalchemy as sa
from app import db
from app.models import Sofor

class SoforEkleForm(FlaskForm):
    ad_soyad = StringField('Ad Soyad', validators=[DataRequired(), Length(min=3, max=120)])
    tc_kimlik = StringField('TC Kimlik No', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Profili Kaydet')

    def validate_tc_kimlik(self, tc_kimlik):
        sofor = db.session.scalar(sa.select(Sofor).where(Sofor.tc_kimlik == tc_kimlik.data))
        if sofor is not None:
            raise ValueError('Bu TC Kimlik numarası zaten sistemde kayıtlı.')

class AlarmEkleForm(FlaskForm):
    alarm_turu = SelectField('Alarm Türü', choices=[
        ('Panik Butonu', 'Panik Butonu'),
        ('Yorgunluk Tespit', 'Yorgunluk Tespit'),
        ('Sağlık Sorunu', 'Sağlık Sorunu'),
        ('Kaza/Arıza', 'Kaza/Arıza')
    ], validators=[DataRequired()])
    submit = SubmitField('Alarm Kaydı Oluştur')

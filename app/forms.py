from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    kullanici_adi = StringField('Kullanıcı Adı', validators=[DataRequired()])
    sifre = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

class YolcuSorguForm(FlaskForm):
    plaka = StringField('Araç Plakası', validators=[DataRequired()])
    submit = SubmitField('Sorgula')

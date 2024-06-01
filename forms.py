from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    nama = StringField('Nama', validators=[DataRequired()])
    pekerjaan = StringField('Pekerjaan', validators=[DataRequired()])
    tgl_lahir = DateField('Tanggal Lahir (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    umur = IntegerField('Umur', validators=[DataRequired()])
    submit = SubmitField('Register')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StockForm(FlaskForm):
    emtn = SelectField('Pilih Emiten', choices=[
        ('BBCA.JK', 'BBCA.JK'), ('BBRI.JK', 'BBRI.JK'), ('BMRI.JK', 'BMRI.JK'), 
        ('TLKM.JK', 'TLKM.JK'), ('ASII.JK', 'ASII.JK'), ('BBNI.JK', 'BBNI.JK'), 
        ('GGRM.JK', 'GGRM.JK'), ('HMSP.JK', 'HMSP.JK'), ('ICBP.JK', 'ICBP.JK'), 
        ('KLBF.JK', 'KLBF.JK'), ('PGAS.JK', 'PGAS.JK'), ('PTBA.JK', 'PTBA.JK'), 
        ('SMGR.JK', 'SMGR.JK'), ('UNVR.JK', 'UNVR.JK'), ('WIKA.JK', 'WIKA.JK')
    ])
    time = SelectField('Pilih Waktu', choices=[
        ('3d', '3 Hari'), ('5d', '5 Hari'), ('1mo', '1 Bulan'), 
        ('3mo', '3 Bulan'), ('6mo', '6 Bulan'), ('1y', '1 Tahun'), 
        ('5y', '5 Tahun')
    ])
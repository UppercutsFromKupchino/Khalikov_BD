from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    loginfield = StringField("Login", validators=[DataRequired()])
    passwordfield = PasswordField("Password", validators=[DataRequired()])
    submitfield = SubmitField()


class RegisterForm(FlaskForm):
    loginfield = StringField("Login", validators=[DataRequired()])
    passwordfield = PasswordField("Password", validators=[DataRequired()])
    fiofield = StringField("FIO", validators=[DataRequired()])
    phonefield = IntegerField("Phone")
    submitfield = SubmitField()
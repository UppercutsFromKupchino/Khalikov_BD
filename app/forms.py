from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    loginfield = StringField("Login", validators=[DataRequired()])
    passwordfield = PasswordField("Password", validators=[DataRequired()])
    submitfield = SubmitField()


class RegisterForm(FlaskForm):
    loginfield = StringField("Login", validators=[DataRequired()])
    passwordfield = PasswordField("Password", validators=[DataRequired()])
    fiofield = StringField("FIO", validators=[DataRequired()])
    photofield = StringField("Photo link")
    phonefield = IntegerField("Phone")
    rolefield = SelectField("Role", choices=[])
    submitfield = SubmitField()


class FeedbackForm(FlaskForm):
    textfield = StringField(validators=[DataRequired()])
    submitfield = SubmitField()


class DeletingFeedbackForm(FlaskForm):
    id_of_feedback_form = HiddenField()
    submit_delete_field = SubmitField("Delete feedback")


class AddingOrderForm(FlaskForm):
    description_of_order = StringField(validators=[DataRequired()])
    price_of_order = IntegerField(validators=[DataRequired()])
    submitfield = SubmitField()


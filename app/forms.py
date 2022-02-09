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


class AddingFeedbackForm(FlaskForm):
    textfield = StringField(validators=[DataRequired()])
    submitfield = SubmitField("Add feedback")


class DeletingFeedbackForm(FlaskForm):
    id_of_feedback_form = HiddenField()
    submit_delete_field = SubmitField("Delete feedback")


class AddingOrderForm(FlaskForm):
    description_of_order = StringField(validators=[DataRequired()])
    price_of_order = IntegerField(validators=[DataRequired()])
    submitfield = SubmitField("Add order")


class ExecutingOrderForm(FlaskForm):
    id_of_order_form = HiddenField()
    submit_execute_field = SubmitField("Execute order")


class DeletingOrderForm(FlaskForm):
    id_of_order_form = HiddenField()
    submit_delete_field = SubmitField("Delete order")


class AddingAdForm(FlaskForm):
    description_of_ad = StringField(validators=[DataRequired()])
    price_of_ad = IntegerField(validators=[DataRequired()])
    submit_add_field = SubmitField()


class ConsumeAdForm(FlaskForm):
    id_of_ad_form = HiddenField()
    submit_consume_field = SubmitField("Consume ad")


class DeletingAdForm(FlaskForm):
    id_of_ad_form = HiddenField()
    submit_delete_field = SubmitField("Delete ad")


class RedirectingToConversationConsumerForm(FlaskForm):
    id_of_executor_form = HiddenField()
    submit_redirecting_field = SubmitField("Go to conversation")


class RedirectingToConversationExecutorForm(FlaskForm):
    id_of_consumer_form = HiddenField()
    submit_redirecting_field = SubmitField("Go to conversation")


class AddingMessageForm(FlaskForm):
    text_of_message_field = StringField()
    submit_adding_field = SubmitField("Add message")

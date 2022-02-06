from app import app
from flask import render_template, flash, url_for, session, redirect
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegisterForm, FeedbackForm, DeletingFeedbackForm, AddingOrderForm
from app.models import User, RoleOfUser, Feedback, Order
import datetime


@app.route('/')
@app.route('/main')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()

    if loginform.validate_on_submit():
        user_on_identification = User.get_user_for_login(loginform.loginfield.data)

        if user_on_identification and user_on_identification.check_password_correction(attempted_password
                                                                                       =loginform.passwordfield.data):
            login_user(user_on_identification)
            session['role'] = RoleOfUser.get_role_for_id(user_on_identification.id_of_role)
            print(session['role'])
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return render_template("login.html", loginform=loginform)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegisterForm()

    roles = RoleOfUser.get_all_roles()
    registerform.rolefield.choices = [i.name_of_role for i in roles if i.name_of_role != 'moderator']

    if registerform.validate_on_submit():

        role_for_user = RoleOfUser.get_role_for_name(registerform.rolefield.data)

        User.add_user(registerform.passwordfield.data, registerform.fiofield.data,
                      registerform.loginfield.data, registerform.photofield.data,
                      registerform.phonefield.data, role_for_user)

        return redirect(url_for('login'))

    return render_template("register.html", registerform=registerform)


@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    feedback_now = Feedback.get_all_feedback()
    if session['role'] != 'moderator':
        feedbackform = FeedbackForm()

        if feedbackform.validate_on_submit():
            Feedback.add_feedback(feedbackform.textfield.data, current_user.get_id())
            return redirect(url_for('feedback'))
        return render_template("feedback.html", feedbackform=feedbackform, feedback_now=feedback_now)

    elif session['role'] == 'moderator':
        deleting_feedback_form = DeletingFeedbackForm()
        print("deleting")

        if deleting_feedback_form.submit_delete_field.data:
            Feedback.delete_feedback(deleting_feedback_form.id_of_feedback_form.data)
            return redirect(url_for('feedback'))
        return render_template("feedback.html", deleting_feedback_form=deleting_feedback_form, feedback_now=feedback_now)


@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():

    # orders = Order.get_orders_consumer(current_user.get_id())

    if session['role'] == 'consumer':

        adding_order_form = AddingOrderForm()

        if adding_order_form.submitfield.data:

            current_time = datetime.datetime.now()
            Order.add_order(current_time, adding_order_form.description_of_order.data,
                            adding_order_form.price_of_order.data, current_user.get_id())

            return redirect(url_for('order'))

        return render_template("order.html", adding_order_form=adding_order_form)


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/logout')
def logout():
    logout_user()
    # session.pop('role', None)
    session.clear()
    return redirect(url_for('index'))

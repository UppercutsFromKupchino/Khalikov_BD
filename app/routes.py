from app import app
from flask import render_template, flash, url_for, session, redirect
from flask_login import login_user, logout_user, current_user
from app.forms import LoginForm, RegisterForm, FeedbackForm
from app.models import User, RoleOfUser, Feedback


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
def feedback():

    feedbackform = FeedbackForm()

    feedback_now = Feedback.get_all_feedback()

    if feedbackform.validate_on_submit():
        Feedback.add_feedback(feedbackform.textfield.data, current_user.get_id())
        return redirect(url_for('feedback'))

    return render_template("feedback.html", feedbackform=feedbackform, feedback_now=feedback_now)


@app.route('/logout')
def logout():
    logout_user()
    # session.pop('role', None)
    # session.clear()
    return redirect(url_for('index'))

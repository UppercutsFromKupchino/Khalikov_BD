from app import app
from flask import render_template, flash, url_for, session, redirect
# from flask_login import login_user, logout_user
from app.forms import LoginForm, RegisterForm
from app.models import User, RoleOfUser


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    loginform = LoginForm()
    return render_template("login.html", loginform=loginform)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegisterForm()

    roles = RoleOfUser.get_all_roles()
    registerform.rolefield.choices = [i.name_of_role for i in roles]

    if registerform.validate_on_submit():

        role_for_user = RoleOfUser.get_role_for_name(registerform.rolefield.data)

        User.add_user(registerform.passwordfield.data, registerform.fiofield.data,
                      registerform.loginfield.data, registerform.photofield.data,
                      registerform.phonefield.data, role_for_user)

        return redirect(url_for('login'))

    return render_template("register.html", registerform=registerform)

from app import app
from flask import render_template, flash, url_for, session
# from flask_login import login_user, logout_user
from app.forms import LoginForm, RegisterForm


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    loginform = LoginForm()
    return render_template("login.html", loginform=loginform)


@app.route('/register')
def register():
    registerform = RegisterForm()
    return render_template("register.html", registerform=registerform)

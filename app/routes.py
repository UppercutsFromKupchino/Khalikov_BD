from app import app
from flask import render_template, flash, url_for, session
# from flask_login import login_user, logout_user


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("index.html")

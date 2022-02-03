from app import app
from flask import render_template, flash, url_for, session
from flask_login import LoginManager


login_manager = LoginManager(app)

@login_manager.init_app(app)
def load_user():
    return

@app.route('/')
def index():
    return render_template("index.html")

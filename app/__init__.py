from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# login_manager = LoginManager(app)
# login_manager.login_view = 'login_page'
# login_manager.login_message_category = 'info'
# login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Место для подключения узлов
from app import routes

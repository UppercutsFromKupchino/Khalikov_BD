from flask import flash, redirect, url_for
from flask_login import UserMixin
from app import db
# from app import login_manager


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __teblename__ = '_user'
    __table_args__ = {'extend_existing': True}

    id_of_user = db.Column(db.Integer(), primary_key=True)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_of_user

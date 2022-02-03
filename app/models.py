from flask import flash, redirect, url_for
from flask_login import UserMixin
from app import db
# from app import login_manager


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = '_user'
    __table_args__ = {'extend_existing': True}

    id_of_user = db.Column(db.Integer(), primary_key=True)
    role_of_user = db.relationship('RoleOfUser', backref='role_of_user', uselist=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_of_user


class Order(db.Model):
    __tablename__ = '_order'
    __table_args__ = {'extend_existing': True}

    id_of_consumer = db.relationship('User', backref='_user', uselist=False)


class Ad(db.Model):
    __tablename__ = 'adr'
    __table_args__ = {'extend_existing': True}

    id_of_executor = db.relationship('User', backref='_user', uselist=False)


class ConsumerOfAd(db.Model):
    __tablename__ = 'consumer_of_ad'
    __table_args__ = {'extend_existing': True}

    id_of_consumer = db.relationship('User', backref='_user', uselist=False)


class ExecutorOfAd(db.Model):
    __tablename__ = 'executor_of_ad'
    __table_args__ = {'extend_existing': True}

    id_of_executor = db.relationship('User', backref='_user', uselist=False)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    __table_args__ = {'extend_existing': True}

    id_of_user = db.relationship('User', backref='_user', uselist=False)


class RoleOfUser(db.Model):
    __tablename__ = 'role_of_user'
    __table_args__ = {'extend_existing': True}


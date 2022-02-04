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
    # role_of_user = db.relationship('RoleOfUser', backref='role_of_user', uselist=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_of_user

    @staticmethod
    def add_user(password_of_user, fio_of_user, login_of_user, photo_of_user, phone_of_user, id_of_role):
        user_to_add = User(password_of_user=password_of_user, fio_of_user=fio_of_user, login_of_user=login_of_user,
                           photo_of_user=photo_of_user, phone_of_user=phone_of_user, id_of_role=id_of_role)

        db.session.add(user_to_add)
        db.session.commit()
        # except:
        #     db.session.rollback()


class Order(db.Model):
    __tablename__ = '_order'
    __table_args__ = {'extend_existing': True}

    # id_of_consumer = db.relationship('User', backref='_user', uselist=False)


class Ad(db.Model):
    __tablename__ = 'ad'
    __table_args__ = {'extend_existing': True}

    # id_of_executor = db.relationship('User', backref='_user', uselist=False)


class ConsumerOfAd(db.Model):
    __tablename__ = 'consumer_of_ad'
    __table_args__ = {'extend_existing': True}

    # id_of_consumer = db.relationship('User', backref='_user', uselist=False)


class ExecutorOfOrder(db.Model):
    __tablename__ = 'executor_of_order'
    __table_args__ = {'extend_existing': True}

    # id_of_executor = db.relationship('User', backref='_user', uselist=False)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_feedback(text_of_feedback, id_of_user):
        feedback_to_add = Feedback(text_of_feedback=text_of_feedback, id_of_user=id_of_user)

        db.session.add(feedback_to_add)
        db.session.commit()

    # id_of_user = db.relationship('User', backref='_user', uselist=False)


class RoleOfUser(db.Model):
    __tablename__ = 'role_of_user'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_roles():
        return RoleOfUser.query.all()

    @staticmethod
    def get_role_for_name(name_of_role):
        chosen_role = RoleOfUser.query.filter_by(name_of_role=name_of_role).one()
        return chosen_role.id_of_role
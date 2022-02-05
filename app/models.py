from flask_login import UserMixin
from app import db
from app import bcrypt
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = '_user'
    __table_args__ = {'extend_existing': True}

    id_of_user = db.Column(db.Integer(), primary_key=True)
    password_of_user = db.Column(db.String(length=150), nullable=False)

    # role_of_user = db.relationship('RoleOfUser', backref='role_of_user', uselist=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_of_user

    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password_of_user = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_of_user, attempted_password)

    @staticmethod
    def get_user_for_login(login_of_user):
        return User.query.filter_by(login_of_user=login_of_user).first()

    @staticmethod
    def add_user(password_of_user, fio_of_user, login_of_user, photo_of_user, phone_of_user, id_of_role):
        user_to_add = User(unencrypted_password=password_of_user, fio_of_user=fio_of_user, login_of_user=login_of_user,
                           photo_of_user=photo_of_user, phone_of_user=phone_of_user, id_of_role=id_of_role)

        try:
            db.session.add(user_to_add)
            db.session.commit()
        except:
            db.session.rollback()


class Order(db.Model):
    __tablename__ = '_order'
    __table_args__ = {'extend_existing': True}


class Ad(db.Model):
    __tablename__ = 'ad'
    __table_args__ = {'extend_existing': True}


class ConsumerOfAd(db.Model):
    __tablename__ = 'consumer_of_ad'
    __table_args__ = {'extend_existing': True}


class ExecutorOfOrder(db.Model):
    __tablename__ = 'executor_of_order'
    __table_args__ = {'extend_existing': True}


class Feedback(db.Model):
    __tablename__ = 'feedback'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_feedback():
        query = db.session.query(Feedback, User)
        query = query.join(User, User.id_of_user == Feedback.id_of_user)
        query = query.order_by(Feedback.id_of_feedback.desc())
        return query.all()

    @staticmethod
    def add_feedback(text_of_feedback, id_of_user):
        feedback_to_add = Feedback(text_of_feedback=text_of_feedback, id_of_user=id_of_user)

        try:
            db.session.add(feedback_to_add)
            db.session.commit()
        except:
            db.session.rollback()


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

    @staticmethod
    def get_role_for_id(id_of_role):
        chosen_role = RoleOfUser.query.filter_by(id_of_role=id_of_role).one()
        return chosen_role.name_of_role
from flask_login import UserMixin
from app import db
from app import bcrypt
from app import login_manager
from flask import flash


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
            flash('Пользователь успешно зарегистрирован!')
        except:
            flash('Ошибка взаимодействия с базой данных. Повторите позже')
            db.session.rollback()

    @staticmethod
    def get_user(id_user):
        query = db.session.query(User).filter(User.id_of_user == id_user).one()
        return query


class Order(db.Model):
    __tablename__ = '_order'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_orders_consumer():
        query = db.session.query(Order, ExecutorOfOrder, User)
        query = query.outerjoin(ExecutorOfOrder, Order.id_of_order == ExecutorOfOrder.id_of_order)
        query = query.join(User, User.id_of_user == Order.id_of_consumer)
        query = query.filter(None == ExecutorOfOrder.id_of_order)
        # query = query.filter(Order.id_of_consumer != consumer).all()
        return query.all()

    @staticmethod
    def add_order(datetime, description, price, id_of_consumer):
        order_to_add = Order(datetime_of_order=datetime, description_of_order=description,
                             price_of_order=price, id_of_consumer=id_of_consumer)

        try:
            db.session.add(order_to_add)
            db.session.commit()
            flash('Заказ успешно добавлен!')
        except:
            flash('Ошибка взаимодействия с базой данных. Повторите позже')
            db.session.rollback()

    @staticmethod
    def get_all_orders():
        query = db.session.query(Order, User)
        query = query.join(User, User.id_of_user == Order.id_of_consumer)
        return query

    @staticmethod
    def delete_order(id_of_order):
        order_to_delete = Order(id_of_order=id_of_order)

        try:
            db.session.delete(order_to_delete)
            db.session.commit()
            flash('Заказ успешно удалён')
        except:
            flash('Ошибка взаимодействия с базой данных')
            db.session.rollback()

    @staticmethod
    def get_orders_profile_consumer(id_consumer):
        query = db.session.query(Order, ExecutorOfOrder, User)
        query = query.outerjoin(ExecutorOfOrder, Order.id_of_order == ExecutorOfOrder.id_of_order)
        query = query.join(User, ExecutorOfOrder.id_of_executor == User.id_of_user)
        query = query.filter(None != ExecutorOfOrder.id_of_executor)
        query = query.filter(Order.id_of_consumer == id_consumer)
        return query.all()

class Ad(db.Model):
    __tablename__ = 'ad'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_ad_executor():
        query = db.session.query(Ad, ConsumerOfAd, User)
        query = query.outerjoin(ConsumerOfAd, ConsumerOfAd.id_of_ad == Ad.id_of_ad)
        query = query.join(User, User.id_of_user == Ad.id_of_executor)
        query = query.filter(None == ConsumerOfAd.id_of_ad)
        return query.all()

    @staticmethod
    def add_ad(datetime_of_ad, description_of_ad, price_of_ad, id_of_executor):
        ad_to_add = Ad(datetime_of_ad=datetime_of_ad, description_of_ad=description_of_ad,
                       price_of_ad=price_of_ad, id_of_executor=id_of_executor)

        try:
            db.session.add(ad_to_add)
            db.session.commit()
            flash('Объявление успешно добавлено')
        except:
            flash('Ошибка взаимодействия с базой данных')
            db.session.rollback()

    @staticmethod
    def get_all_ads():
        query = db.session.query(Ad, User)
        query = query.join(User, Ad.id_of_executor == User.id_of_user)
        return query

    @staticmethod
    def delete_ad(id_of_ad):
        ad_to_delete = Ad(id_of_ad=id_of_ad)

        try:
            db.session.delete(ad_to_delete)
            db.session.commit()
            flash('Объявление успешно удалено')
        except:
            flash('Ошибка взаимодействия с базой данных')
            db.session.rollback()

    @staticmethod
    def get_ads_profile_consumer(id_consumer):
        query = db.session.query(Ad, ConsumerOfAd, User)
        query = query.outerjoin(ConsumerOfAd, ConsumerOfAd.id_of_ad == Ad.id_of_ad)
        query = query.join(User, Ad.id_of_executor == User.id_of_user)
        query = query.filter(ConsumerOfAd.id_of_consumer == id_consumer)
        return query.all()


class ConsumerOfAd(db.Model):
    __tablename__ = 'consumer_of_ad'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def consume_ad(id_of_consumer, id_of_ad):
        ad_to_consume = ConsumerOfAd(id_of_consumer=id_of_consumer, id_of_ad=id_of_ad)

        try:
            db.session.add(ad_to_consume)
            db.session.commit()
            flash('Объявление успешно заказано')
        except:
            flash('Ошибка взаимодействия с базой данных')
            db.session.rollback()


class ExecutorOfOrder(db.Model):
    __tablename__ = 'executor_of_order'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def execute_order(id_of_executor, id_of_order):
        order_to_execute = ExecutorOfOrder(id_of_executor=id_of_executor, id_of_order=id_of_order)

        try:
            db.session.add(order_to_execute)
            db.session.commit()
            flash('Заказ успешно принят к исполнению')
        except:
            flash('Ошибка взаимодействия с базой данных. Повторите позже')
            db.session.rollback()


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
            flash('Отзыв успешно добавлен!')
        except:
            flash('Ошибка взаимодействия с базой данных. Повторите позже')
            db.session.rollback()

    @staticmethod
    def delete_feedback(id_of_feedback):
        try:
            Feedback.query.filter_by(id_of_feedback=id_of_feedback).delete()
            db.session.commit()
            flash('Отзыв успешно удалён!')
        except:
            flash('Ошибка взаимодействия с базой данных. Повторите позже')
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

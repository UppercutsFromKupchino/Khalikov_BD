from app import app
from flask import render_template, flash, url_for, session, redirect
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegisterForm, AddingFeedbackForm, DeletingFeedbackForm, AddingOrderForm
from app.forms import DeletingOrderForm, ExecutingOrderForm, AddingAdForm, ConsumeAdForm, DeletingAdForm
from app.forms import RedirectingToConversationConsumerForm, RedirectingToConversationExecutorForm
from app.forms import AddingMessageForm
from app.models import User, RoleOfUser, Feedback, Order, ExecutorOfOrder, Ad, ConsumerOfAd, Message
import datetime


@app.route('/')
@app.route('/main')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    loginform = LoginForm()

    if loginform.validate_on_submit():

        user_on_identification = User.get_user_for_login(loginform.loginfield.data)

        if user_on_identification and user_on_identification.check_password_correction(attempted_password
                                                                                       =loginform.passwordfield.data):
            login_user(user_on_identification)
            session['role'] = RoleOfUser.get_role_for_id(user_on_identification.id_of_role)
            return redirect(url_for('index'))

        else:
            return redirect(url_for('login'))

    return render_template("login.html", loginform=loginform)


@app.route('/register', methods=['GET', 'POST'])
def register():

    registerform = RegisterForm()

    roles = RoleOfUser.get_all_roles()
    registerform.rolefield.choices = [i.name_of_role for i in roles if i.name_of_role != 'moderator']

    if registerform.validate_on_submit():

        role_for_user = RoleOfUser.get_role_for_name(registerform.rolefield.data)

        User.add_user(registerform.passwordfield.data, registerform.fiofield.data,
                      registerform.loginfield.data, registerform.photofield.data,
                      registerform.phonefield.data, role_for_user)
        return redirect(url_for('login'))

    return render_template("register.html", registerform=registerform)


@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():

    feedback_now = Feedback.get_all_feedback()
    if session['role'] != 'moderator':

        feedbackform = AddingFeedbackForm()

        if feedbackform.validate_on_submit():

            Feedback.add_feedback(feedbackform.textfield.data, current_user.get_id())
            return redirect(url_for('feedback'))

        return render_template("feedback.html", feedbackform=feedbackform, feedback_now=feedback_now)

    elif session['role'] == 'moderator':

        deleting_feedback_form = DeletingFeedbackForm()

        if deleting_feedback_form.submit_delete_field.data:

            Feedback.delete_feedback(deleting_feedback_form.id_of_feedback_form.data)
            return redirect(url_for('feedback'))

        return render_template("feedback.html", deleting_feedback_form=deleting_feedback_form, feedback_now=feedback_now)


@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():

    if session['role'] == 'consumer':

        orders = Order.get_orders_consumer()
        orders_len = len(orders)

        adding_order_form = AddingOrderForm()

        if adding_order_form.submitfield.data:

            current_time = datetime.datetime.now()
            Order.add_order(current_time, adding_order_form.description_of_order.data,
                            adding_order_form.price_of_order.data, current_user.get_id())
            return redirect(url_for('order'))

        return render_template("order.html", adding_order_form=adding_order_form, orders=orders,
                               orders_len=orders_len)

    if session['role'] == 'executor':

        orders = Order.get_orders_consumer()
        orders_len = len(orders)

        executing_order_form = ExecutingOrderForm()

        if executing_order_form.submit_execute_field.data:

            ExecutorOfOrder.execute_order(current_user.get_id(), executing_order_form.id_of_order_form.data)
            return redirect(url_for('order'))

        return render_template("order.html", executing_order_form=executing_order_form, orders=orders,
                               orders_len=orders_len)

    if session['role'] == 'moderator':

        orders = Order.get_all_orders()

        deleting_order_form = DeletingOrderForm()

        if deleting_order_form.submit_delete_field.data:

            ExecutorOfOrder.delete_order(deleting_order_form.id_of_order_form.data)
            Order.delete_order(deleting_order_form.id_of_order_form.data)
            return redirect(url_for('order'))

        return render_template("order.html", orders=orders, deleting_order_form=deleting_order_form)


@app.route('/ad', methods=['GET', 'POST'])
def ad():

    if session['role'] == 'executor':

        ads = Ad.get_ad_executor()
        ads_len = len(ads)

        adding_ad_form = AddingAdForm()

        if adding_ad_form.submit_add_field.data:

            current_time = datetime.datetime.now()
            Ad.add_ad(current_time, adding_ad_form.description_of_ad.data,
                      adding_ad_form.price_of_ad.data, current_user.get_id())
            return redirect(url_for('ad'))

        return render_template("ad.html", adding_ad_form=adding_ad_form, ads=ads,
                               ads_len=ads_len)

    if session['role'] == 'consumer':

        ads = Ad.get_ad_executor()
        ads_len = len(ads)

        consuming_ad_form = ConsumeAdForm()

        if consuming_ad_form.submit_consume_field.data:

            ConsumerOfAd.consume_ad(current_user.get_id(), consuming_ad_form.id_of_ad_form.data)
            return redirect(url_for('ad'))

        return render_template("ad.html", consuming_ad_form=consuming_ad_form, ads=ads,
                               ads_len=ads_len)

    if session['role'] == 'moderator':

        ads = Ad.get_all_ads()

        deleting_ad_form = DeletingAdForm()

        if deleting_ad_form.submit_delete_field.data:

            ConsumerOfAd.delete_ad(deleting_ad_form.id_of_ad_form.data)
            Ad.delete_ad(deleting_ad_form.id_of_ad_form.data)
            return redirect(url_for('ad'))

        return render_template("ad.html", ads=ads, deleting_ad_form=deleting_ad_form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    user = User.get_user(current_user.get_id())
    print(current_user.get_id())

    if session['role'] == 'consumer':

        redirecting_to_conversation_consumer_form = RedirectingToConversationConsumerForm()

        orders = Order.get_orders_profile_consumer(current_user.get_id())
        orders_len = len(orders)
        ads = Ad.get_ads_profile_consumer(current_user.get_id())
        ads_len = len(ads)

        if redirecting_to_conversation_consumer_form.submit_redirecting_field.data:
            return redirect(url_for('conversation',
                                    receiver=redirecting_to_conversation_consumer_form.id_of_executor_form.data))

        return render_template("profile.html", user=user, orders=orders, ads=ads,
                               orders_len=orders_len, ads_len=ads_len,
                               redirecting_to_conversation_consumer_form=redirecting_to_conversation_consumer_form)

    elif session['role'] == 'executor':

        redirecting_to_conversation_executor_form = RedirectingToConversationExecutorForm()

        orders = Order.get_orders_profile_executor(current_user.get_id())
        orders_len = len(orders)
        ads = Ad.get_ads_profile_executor(current_user.get_id())
        ads_len = len(ads)

        if redirecting_to_conversation_executor_form.submit_redirecting_field.data:
            return redirect(url_for('conversation',
                                    receiver=redirecting_to_conversation_executor_form.id_of_consumer_form.data))

        return render_template("profile.html", user=user, orders=orders, ads=ads,
                               orders_len=orders_len, ads_len=ads_len,
                               redirecting_to_conversation_executor_form=redirecting_to_conversation_executor_form)

    elif session['role'] == 'moderator':
        return redirect(url_for('index'))


@app.route('/conversation/<receiver>', methods=['GET', 'POST'])
@login_required
def conversation(receiver):

    messages_in_conv = Message.get_messages(current_user.get_id(), receiver)
    adding_message_form = AddingMessageForm()

    if adding_message_form.submit_adding_field.data:

        current_time = datetime.datetime.now()
        Message.add_message(current_user.get_id(), adding_message_form.text_of_message_field.data,
                            current_time, receiver)
        return redirect(url_for('conversation', receiver=receiver))

    return render_template("conversation.html", receiver=receiver, messages_in_conv=messages_in_conv,
                           adding_message_form=adding_message_form)


@app.route('/logout')
def logout():
    logout_user()
    # session.pop('role', None)
    session.clear()
    return redirect(url_for('index'))

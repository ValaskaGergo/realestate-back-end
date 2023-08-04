# -*- coding: utf-8 -*-
from app import db
from passlib.hash import pbkdf2_sha256 as sha256


# ======== Mixed ================================================================================ #

# -------- DB Session Commit ---------------------------- #
class DBCommit(object):
    def db_post(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def db_put():
        db.session.commit()

    def db_delete(self):
        db.session.delete(self)
        db.session.commit()


# ======== Relationship ========================================================================= #

# -------- PERMISSION ----------------------------------- #
user_permission = db.Table('user_permission_relationship',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('user_permission_id', db.Integer, db.ForeignKey('user_permission.id'))
                           )

# -------- PROFILE -------------------------------------- #
user_profile = db.Table('user_profile_relationship',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('user_profile_id', db.Integer, db.ForeignKey('user_profile.id'))
                        )

# -------- BILLING -------------------------------------- #
user_billing_information = db.Table('user_billing_information_relationship',
                                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                    db.Column('user_billing_information_id', db.Integer,
                                              db.ForeignKey('user_billing_information.id'))
                                    )

# -------- SHIPPING ------------------------------------- #
user_shipping_information = db.Table('user_shipping_information_relationship',
                                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                     db.Column('user_shipping_information_id', db.Integer,
                                               db.ForeignKey('user_shipping_information.id'))
                                     )

# -------- Change Email --------------------------------- #
user_secondary_email = db.Table('user_secondary_email_relationship',
                                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                db.Column('user_secondary_email_id', db.Integer,
                                          db.ForeignKey('user_secondary_email.id'))
                                )

# -------- Session History ------------------------------ #
user_session_history_login = db.Table('user_session_history_login_relationship',
                                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                      db.Column('user_session_history_login_id', db.Integer,
                                                db.ForeignKey('user_session_history_login.id'))
                                      )

# -------- Barion Payment --------------------------------- #
barion_payment = db.Table('barion_payment_relationship',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('barion_payment_id', db.Integer,
                                    db.ForeignKey('barion_payment.id'))
                          )

# -------- PayPal Payment --------------------------------- #
paypal_payment = db.Table('paypal_payment_relationship',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('paypal_payment_id', db.Integer,
                                    db.ForeignKey('paypal_payment.id'))
                          )

# -------- Category ------------------------------------------- #
sub_category = db.Table('sub_category_relationship',
                        db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                        db.Column('sub_category_id', db.Integer,
                                  db.ForeignKey('sub_category.id'))
                        )

# -------- Subcategory ------------------------------------------- #
translate_talking = db.Table('translate_talking_relationship',
                             db.Column('sub_category_id', db.Integer, db.ForeignKey('sub_category.id')),
                             db.Column('translate_talking_id', db.Integer,
                                       db.ForeignKey('translate_talking.id'))
                             )

# -------- Animal --------------------------------------------- #
animal = db.Table('animal_relationship',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('animal_id', db.Integer,
                            db.ForeignKey('animal.id'))
                  )

animal_photos = db.Table('animal_photos_relationship',
                         db.Column('animal_id', db.Integer, db.ForeignKey('animal.id')),
                         db.Column('animal_photos_id', db.Integer,
                                   db.ForeignKey('animal_photos.id'))
                         )

animal_videos = db.Table('animal_videos_relationship',
                         db.Column('animal_id', db.Integer, db.ForeignKey('animal.id')),
                         db.Column('animal_videos_id', db.Integer,
                                   db.ForeignKey('animal_videos.id'))
                         )

animal_pdf = db.Table('animal_pdf_relationship',
                      db.Column('animal_id', db.Integer, db.ForeignKey('animal.id')),
                      db.Column('animal_pdf_id', db.Integer,
                                db.ForeignKey('animal_pdf.id'))
                      )

translate = db.Table('translate_relationship',
                     db.Column('animal_id', db.Integer, db.ForeignKey('animal.id')),
                     db.Column('translate_id', db.Integer,
                               db.ForeignKey('translate.id'))
                     )

# -------- Notification --------------------------------------- #

online = db.Table('online_relationship',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('online_id', db.Integer, db.ForeignKey('online.id'))
                  )

messages = db.Table('messages_relationship',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('messages_id', db.Integer, db.ForeignKey('messages.id'))
                    )

notification_settings = db.Table('notification_settings_relationship',
                                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                 db.Column('notification_settings_id', db.Integer,
                                           db.ForeignKey('notification_settings.id'))
                                 )

# -------- Questions And Answers ------------------------------ #
answers = db.Table('answers_relationship',
                   db.Column('questions_id', db.Integer, db.ForeignKey('questions.id')),
                   db.Column('answers_id', db.Integer,
                             db.ForeignKey('answers.id'))
                   )

questions_history = db.Table('questions_history_relationship',
                             db.Column('questions_id', db.Integer, db.ForeignKey('questions.id')),
                             db.Column('questions_history_id', db.Integer,
                                       db.ForeignKey('questions_history.id'))
                             )

answers_history = db.Table('answers_history_relationship',
                           db.Column('answers_id', db.Integer, db.ForeignKey('answers.id')),
                           db.Column('answers_history_id', db.Integer,
                                     db.ForeignKey('answers_history.id'))
                           )

# -------- Talking -------------------------------------- #
talking_history = db.Table('talking_history_relationship',
                           db.Column('talking_id', db.Integer, db.ForeignKey('talking.id')),
                           db.Column('talking_history_id', db.Integer,
                                     db.ForeignKey('talking_history.id'))
                           )

talking_answer = db.Table('talking_answer_relationship',
                          db.Column('talking_id', db.Integer, db.ForeignKey('talking.id')),
                          db.Column('talking_answer_id', db.Integer,
                                    db.ForeignKey('talking_answer.id'))
                          )

talking_answer_history = db.Table('talking_answer_history_relationship',
                                  db.Column('talking_answer_id', db.Integer, db.ForeignKey('talking_answer.id')),
                                  db.Column('talking_answer_history_id', db.Integer,
                                            db.ForeignKey('talking_answer_history.id'))
                                  )

talking_vote = db.Table('talking_vote_relationship',
                        db.Column('talking_id', db.Integer, db.ForeignKey('talking.id')),
                        db.Column('talking_vote_id', db.Integer,
                                  db.ForeignKey('talking_vote.id'))
                        )

# -------- Wishlist -------------------------------------- #
wishlist = db.Table('wishlist_relationship',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('wishlist_id', db.Integer, db.ForeignKey('wishlist.id'))
                    )


class User(db.Model, DBCommit):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, nullable=False)
    privacy = db.Column(db.String, nullable=False)
    deleted = db.Column(db.String, unique=False, nullable=True, default="False")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    permission = db.relationship('UserPermission',
                                 secondary=user_permission,
                                 backref='user_permission_backref',
                                 cascade='save-update, delete',
                                 lazy='dynamic')

    profile = db.relationship('UserProfile',
                              secondary=user_profile,
                              backref='user_profile_backref',
                              cascade='save-update, delete',
                              lazy='dynamic')

    billing_information = db.relationship('UserBillingInformation',
                                          secondary=user_billing_information,
                                          backref='user_billing_information_backref',
                                          cascade='save-update, delete',
                                          lazy='dynamic')

    shipping_information = db.relationship('UserShippingInformation',
                                           secondary=user_shipping_information,
                                           backref='user_shipping_information_backref',
                                           cascade='save-update, delete',
                                           lazy='dynamic')

    secondary_email = db.relationship('UserSecondaryEmail',
                                      secondary=user_secondary_email,
                                      backref='user_secondary_email_backref',
                                      cascade='save-update, delete',
                                      lazy='dynamic')

    session_history_login = db.relationship('UserSessionHistoryLogin',
                                            secondary=user_session_history_login,
                                            backref='user_session_history_login_backref',
                                            cascade='save-update, delete',
                                            lazy='dynamic')

    barion_payment = db.relationship('BarionPayment',
                                     secondary=barion_payment,
                                     backref='barion_payment_backref',
                                     cascade='save-update, delete',
                                     lazy='dynamic')

    paypal_payment = db.relationship('PayPalPayment',
                                     secondary=paypal_payment,
                                     backref='paypal_payment_backref',
                                     cascade='save-update, delete',
                                     lazy='dynamic')

    animal = db.relationship('Animal',
                             secondary=animal,
                             backref='animal_backref',
                             cascade='save-update, delete',
                             lazy='dynamic')

    online = db.relationship('Online',
                             secondary=online,
                             backref='online_backref',
                             cascade='save-update, delete',
                             lazy='dynamic')

    messages = db.relationship('Messages',
                               secondary=messages,
                               backref='messages_backref',
                               cascade='save-update, delete',
                               lazy='dynamic')

    notification_settings = db.relationship('NotificationSettings',
                                            secondary=notification_settings,
                                            backref='notification_settings_backref',
                                            cascade='save-update, delete',
                                            lazy='dynamic')

    wishlist = db.relationship('Wishlist',
                               secondary=wishlist,
                               backref='wishlist_backref',
                               cascade='save-update, delete',
                               lazy='dynamic')

    def __init__(self, email):
        self.email = email

    def password_hash(self, password):
        self.password = sha256.hash(password)

    @staticmethod
    def password_verify(password, sha):
        return sha256.verify(password, sha)

    def __repr__(self):
        return '<User %r>' % self.id


class UserPermission(db.Model, DBCommit):
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True)
    is_worker = db.Column(db.String, unique=False, nullable=False, default="False")
    is_admin = db.Column(db.String, unique=False, nullable=False, default="False")
    is_admin_settings_management = db.Column(db.String, unique=False, nullable=False, default="False")
    is_user_management = db.Column(db.String, unique=False, nullable=False, default="False")
    is_category_management = db.Column(db.String, unique=False, nullable=False, default="False")
    is_notifications = db.Column(db.String, unique=False, nullable=False, default="False")
    subscribed = db.Column(db.String, unique=False, nullable=False, default="False")
    subscribed_start = db.Column(db.DateTime, nullable=True)
    subscribed_end = db.Column(db.DateTime, nullable=True)
    subscribed_type = db.Column(db.Numeric, unique=False, nullable=True)
    subscribed_monthly = db.Column(db.Numeric, unique=False, nullable=True)
    subscribed_ads = db.Column(db.Numeric, unique=False, nullable=True)
    subscribed_chat = db.Column(db.Numeric, unique=False, nullable=True)
    inactive_account = db.Column(db.String, unique=False, nullable=False, default="False")
    last_modification_user_id = db.Column(db.Integer, unique=False, nullable=True)
    last_modification_user_name = db.Column(db.String, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<UserPermission %r>' % self.id


class UserProfile(db.Model, DBCommit):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<UserProfile %r>' % self.id


class UserBillingInformation(db.Model, DBCommit):
    __tablename__ = 'user_billing_information'

    id = db.Column(db.Integer, primary_key=True)
    is_company = db.Column(db.String, unique=False, nullable=True, default="False")
    first_name = db.Column(db.String, unique=False, nullable=True)
    last_name = db.Column(db.String, unique=False, nullable=True)
    company_name = db.Column(db.String, unique=False, nullable=True)
    company_tax = db.Column(db.String, unique=False, nullable=True)
    phone = db.Column(db.String, unique=False, nullable=True)
    email = db.Column(db.String, unique=False, nullable=True)
    country = db.Column(db.String, unique=False, nullable=True)
    country_vat = db.Column(db.String, unique=False, nullable=True)
    payment_country_vat = db.Column(db.String, unique=False, nullable=True)
    zip_number = db.Column(db.String, unique=False, nullable=True)
    place = db.Column(db.String, unique=False, nullable=True)
    street = db.Column(db.String, unique=False, nullable=True)
    currency = db.Column(db.String, unique=False, nullable=True)
    is_shipping_address = db.Column(db.String, unique=False, nullable=True, default="True")
    billingo_partner_id = db.Column(db.Numeric, unique=False, nullable=True)
    completed = db.Column(db.String, unique=False, nullable=False, default="False")
    last_modification_user_id = db.Column(db.Integer, unique=False, nullable=True)
    last_modification_user_name = db.Column(db.String, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<UserBillingInformation %r>' % self.id


class UserShippingInformation(db.Model, DBCommit):
    __tablename__ = 'user_shipping_information'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, unique=False, nullable=True)
    last_name = db.Column(db.String, unique=False, nullable=True)
    company_name = db.Column(db.String, unique=False, nullable=True)
    phone = db.Column(db.String, unique=False, nullable=True)
    email = db.Column(db.String, unique=False, nullable=True)
    country = db.Column(db.String, unique=False, nullable=True)
    zip_number = db.Column(db.String, unique=False, nullable=True)
    place = db.Column(db.String, unique=False, nullable=True)
    street = db.Column(db.String, unique=False, nullable=True)
    currency = db.Column(db.String, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<UserShippingInformation %r>' % self.id


class AdminSettings(db.Model, DBCommit):
    __tablename__ = 'admin_settings'

    id = db.Column(db.Integer, primary_key=True)
    settings_user_id = db.Column(db.Integer, unique=False, nullable=False)
    settings_user_name = db.Column(db.String, unique=False, nullable=False)
    settings_name = db.Column(db.String, unique=False, nullable=False)
    #  settings_type insert: "number" vs "string" only
    settings_type = db.Column(db.String, unique=False, nullable=False)
    settings_value = db.Column(db.String, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, settings_user_id, settings_user_name, settings_name, settings_type, settings_value):
        self.settings_user_id = settings_user_id
        self.settings_user_name = settings_user_name
        self.settings_name = settings_name
        self.settings_type = settings_type
        self.settings_value = settings_value

    def __repr__(self):
        return '<AdminSettings %r>' % self.id


class UserSecondaryEmail(db.Model, DBCommit):
    __tablename__ = 'user_secondary_email'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    secret_key = db.Column(db.String)
    count = db.Column(db.Numeric, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<UserSecondaryEmail %r>' % self.id


class UserSessionHistoryLogin(db.Model, DBCommit):
    __tablename__ = 'user_session_history_login'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String)
    country_name = db.Column(db.String)
    ip = db.Column(db.String)
    browser_name = db.Column(db.String)
    browser_version = db.Column(db.String)
    os_name = db.Column(db.String)
    platform_type = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, country_code, country_name, ip, browser_name, browser_version, os_name, platform_type):
        self.country_code = country_code
        self.country_name = country_name
        self.ip = ip
        self.browser_name = browser_name
        self.browser_version = browser_version
        self.os_name = os_name
        self.platform_type = platform_type

    def __repr__(self):
        return '<UserSessionHistoryLogin %r>' % self.id


class BarionPayment(db.Model, DBCommit):
    __tablename__ = 'barion_payment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=True)
    payment_type = db.Column(db.String, unique=False, nullable=True)
    payment_id = db.Column(db.String, unique=False, nullable=True)
    payment_request_id = db.Column(db.String, unique=False, nullable=True)
    order_number = db.Column(db.String, unique=False, nullable=True)
    status = db.Column(db.String, unique=False, nullable=True)
    funding_source = db.Column(db.String, unique=False, nullable=True)
    completed_at = db.Column(db.String, unique=False, nullable=True)
    transaction_id = db.Column(db.String, unique=False, nullable=True)
    price = db.Column(db.Numeric, unique=False, nullable=True)
    vat = db.Column(db.Numeric, unique=False, nullable=True)
    total = db.Column(db.Numeric, unique=False, nullable=True)
    currency = db.Column(db.String, unique=False, nullable=True)
    billing_url = db.Column(db.String, unique=False, nullable=True)
    account_type = db.Column(db.Numeric, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, payment_type, payment_id, payment_request_id, status, price, vat, total, account_type):
        self.user_id = user_id
        self.payment_type = payment_type
        self.payment_id = payment_id
        self.payment_request_id = payment_request_id
        self.status = status
        self.price = price
        self.vat = vat
        self.total = total
        self.account_type = account_type

    def __repr__(self):
        return '<BarionPayment %r>' % self.id


class PayPalPayment(db.Model, DBCommit):
    __tablename__ = 'paypal_payment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=True)
    payment_type = db.Column(db.String, unique=False, nullable=True)
    payment_id = db.Column(db.String, unique=False, nullable=True)
    payment_request_id = db.Column(db.String, unique=False, nullable=True)
    order_number = db.Column(db.String, unique=False, nullable=True)
    status = db.Column(db.String, unique=False, nullable=True)
    funding_source = db.Column(db.String, unique=False, nullable=True)
    completed_at = db.Column(db.String, unique=False, nullable=True)
    transaction_id = db.Column(db.String, unique=False, nullable=True)
    price = db.Column(db.Numeric, unique=False, nullable=True)
    vat = db.Column(db.Numeric, unique=False, nullable=True)
    total = db.Column(db.Numeric, unique=False, nullable=True)
    currency = db.Column(db.String, unique=False, nullable=True)
    billing_url = db.Column(db.String, unique=False, nullable=True)
    account_type = db.Column(db.Numeric, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, payment_type, payment_id, payment_request_id, status, price, vat, total, account_type):
        self.user_id = user_id
        self.payment_type = payment_type
        self.payment_id = payment_id
        self.payment_request_id = payment_request_id
        self.status = status
        self.price = price
        self.vat = vat
        self.total = total
        self.account_type = account_type

    def __repr__(self):
        return '<PayPalPayment %r>' % self.id


class Category(db.Model, DBCommit):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category_user_id = db.Column(db.Integer, unique=False, nullable=False)
    category_user_name = db.Column(db.String, unique=False, nullable=False)
    name_hu = db.Column(db.String, unique=False, nullable=False)
    name_en = db.Column(db.String, unique=False, nullable=False)
    name_de = db.Column(db.String, unique=False, nullable=False)
    name_fr = db.Column(db.String, unique=False, nullable=False)
    name_es = db.Column(db.String, unique=False, nullable=False)
    gender_hu = db.Column(db.String, unique=False, nullable=False)
    gender_en = db.Column(db.String, unique=False, nullable=False)
    gender_de = db.Column(db.String, unique=False, nullable=False)
    gender_fr = db.Column(db.String, unique=False, nullable=False)
    gender_es = db.Column(db.String, unique=False, nullable=False)
    be_used_for_hu = db.Column(db.String, unique=False, nullable=True)
    be_used_for_en = db.Column(db.String, unique=False, nullable=True)
    be_used_for_de = db.Column(db.String, unique=False, nullable=True)
    be_used_for_fr = db.Column(db.String, unique=False, nullable=True)
    be_used_for_es = db.Column(db.String, unique=False, nullable=True)
    color_hu = db.Column(db.String, unique=False, nullable=True)
    color_en = db.Column(db.String, unique=False, nullable=True)
    color_de = db.Column(db.String, unique=False, nullable=True)
    color_fr = db.Column(db.String, unique=False, nullable=True)
    color_es = db.Column(db.String, unique=False, nullable=True)
    img_data = db.Column(db.String, unique=False, nullable=True)
    img = db.Column(db.String, unique=False, nullable=True)
    visibility = db.Column(db.String, unique=False, nullable=True, default="True")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    sub_category = db.relationship('SubCategory',
                                   secondary=sub_category,
                                   backref='sub_category_backref',
                                   cascade='save-update, delete',
                                   lazy='dynamic')

    def __init__(self, category_user_id, category_user_name, name_hu, name_en, name_de, name_fr, name_es, gender_hu,
                 gender_en, gender_de, gender_fr, gender_es, be_used_for_hu, be_used_for_en, be_used_for_de,
                 be_used_for_fr, be_used_for_es, color_hu,
                 color_en, color_de, color_fr, color_es, img_data, img, visibility):
        self.category_user_id = category_user_id
        self.category_user_name = category_user_name
        self.name_hu = name_hu
        self.name_en = name_en
        self.name_de = name_de
        self.name_fr = name_fr
        self.name_es = name_es
        self.gender_hu = gender_hu
        self.gender_en = gender_en
        self.gender_de = gender_de
        self.gender_fr = gender_fr
        self.gender_es = gender_es
        self.be_used_for_hu = be_used_for_hu
        self.be_used_for_en = be_used_for_en
        self.be_used_for_de = be_used_for_de
        self.be_used_for_fr = be_used_for_fr
        self.be_used_for_es = be_used_for_es
        self.color_hu = color_hu
        self.color_en = color_en
        self.color_de = color_de
        self.color_fr = color_fr
        self.color_es = color_es
        self.img_data = img_data
        self.img = img
        self.visibility = visibility

    def __repr__(self):
        return '<Category %r>' % self.id


class SubCategory(db.Model, DBCommit):
    __tablename__ = 'sub_category'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, unique=False, nullable=False)
    category_user_id = db.Column(db.Integer, unique=False, nullable=False)
    category_user_name = db.Column(db.String, unique=False, nullable=False)
    name_hu = db.Column(db.String, unique=False, nullable=True)
    name_en = db.Column(db.String, unique=False, nullable=True)
    name_de = db.Column(db.String, unique=False, nullable=True)
    name_fr = db.Column(db.String, unique=False, nullable=True)
    name_es = db.Column(db.String, unique=False, nullable=True)
    description_hu = db.Column(db.String, unique=False, nullable=True)
    description_en = db.Column(db.String, unique=False, nullable=True)
    description_de = db.Column(db.String, unique=False, nullable=True)
    description_fr = db.Column(db.String, unique=False, nullable=True)
    description_es = db.Column(db.String, unique=False, nullable=True)
    img_data = db.Column(db.String, unique=False, nullable=True)
    img = db.Column(db.String, unique=False, nullable=True)
    visibility = db.Column(db.String, unique=False, nullable=True, default="True")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    translate_talking = db.relationship('TranslateTalking',
                                        secondary=translate_talking,
                                        backref='translate_talking_backref',
                                        cascade='save-update, delete',
                                        lazy='dynamic')

    def __init__(self, category_id, category_user_id, category_user_name, name_hu, name_en, name_de, name_fr, name_es,
                 description_hu, description_en, description_de, description_fr, description_es, img_data, img,
                 visibility):
        self.category_id = category_id
        self.category_user_id = category_user_id
        self.category_user_name = category_user_name
        self.name_hu = name_hu
        self.name_en = name_en
        self.name_de = name_de
        self.name_fr = name_fr
        self.name_es = name_es
        self.description_hu = description_hu
        self.description_en = description_en
        self.description_de = description_de
        self.description_fr = description_fr
        self.description_es = description_es
        self.img_data = img_data
        self.img = img
        self.visibility = visibility

    def __repr__(self):
        return '<SubCategory %r>' % self.id


class Animal(db.Model, DBCommit):
    __tablename__ = 'animal'

    id = db.Column(db.Integer, primary_key=True)
    advertisement_id = db.Column(db.BigInteger, unique=False, nullable=True)
    user_id = db.Column(db.Integer, unique=False, nullable=True)
    category_id = db.Column(db.Integer, unique=False, nullable=True)
    subcategory_id = db.Column(db.Integer, unique=False, nullable=True)
    name = db.Column(db.String, unique=False, nullable=True)
    region_residence = db.Column(db.String, unique=False, nullable=True)
    country_residence = db.Column(db.String, unique=False, nullable=True)
    be_used_for_hu = db.Column(db.String, unique=False, nullable=True)
    be_used_for_en = db.Column(db.String, unique=False, nullable=True)
    be_used_for_de = db.Column(db.String, unique=False, nullable=True)
    be_used_for_fr = db.Column(db.String, unique=False, nullable=True)
    be_used_for_es = db.Column(db.String, unique=False, nullable=True)
    gender_hu = db.Column(db.String, unique=False, nullable=True)
    gender_en = db.Column(db.String, unique=False, nullable=True)
    gender_de = db.Column(db.String, unique=False, nullable=True)
    gender_fr = db.Column(db.String, unique=False, nullable=True)
    gender_es = db.Column(db.String, unique=False, nullable=True)
    color_hu = db.Column(db.String, unique=False, nullable=True)
    color_en = db.Column(db.String, unique=False, nullable=True)
    color_de = db.Column(db.String, unique=False, nullable=True)
    color_fr = db.Column(db.String, unique=False, nullable=True)
    color_es = db.Column(db.String, unique=False, nullable=True)
    brief_description = db.Column(db.String, unique=False, nullable=True)
    brief_description_detect_lang = db.Column(db.String, unique=False, nullable=True)
    description = db.Column(db.String, unique=False, nullable=True)
    description_detect_lang = db.Column(db.String, unique=False, nullable=True)
    page_url = db.Column(db.String, unique=False, nullable=True)
    url_01 = db.Column(db.String, unique=False, nullable=True)
    url_02 = db.Column(db.String, unique=False, nullable=True)
    price = db.Column(db.INTEGER, unique=False, nullable=True)
    rating = db.Column(db.FLOAT, unique=False, nullable=True, default=0)
    visibility = db.Column(db.String, unique=False, nullable=True, default="True")
    deleted = db.Column(db.Boolean, default=False)
    worker_visibility = db.Column(db.String, unique=False, nullable=True, default="True")
    last_modification_user_id = db.Column(db.Integer, unique=False, nullable=True)
    last_modification_user_name = db.Column(db.String, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    photos = db.relationship('AnimalPhotos',
                             secondary=animal_photos,
                             backref='animal_photos_backref',
                             cascade='save-update, delete',
                             lazy='dynamic')

    videos = db.relationship('AnimalVideos',
                             secondary=animal_videos,
                             backref='animal_videos_backref',
                             cascade='save-update, delete',
                             lazy='dynamic')

    pdf = db.relationship('AnimalPDF',
                          secondary=animal_pdf,
                          backref='animal_pdf_backref',
                          cascade='save-update, delete',
                          lazy='dynamic')

    translate = db.relationship('Translate',
                                secondary=translate,
                                backref='translate_backref',
                                cascade='save-update, delete',
                                lazy='dynamic')

    def __init__(self, user_id, advertisement_id, category_id, subcategory_id, name,
                 region_residence, country_residence, be_used_for_hu,
                 be_used_for_en, be_used_for_de, be_used_for_fr, be_used_for_es, gender_hu, gender_en, gender_de,
                 gender_fr, gender_es, color_hu, color_en, color_de, color_fr, color_es, brief_description,
                 brief_description_detect_lang, description, description_detect_lang, page_url, url_01, url_02, price,
                 last_modification_user_id,
                 last_modification_user_name):
        self.user_id = user_id
        self.advertisement_id = advertisement_id
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.name = name
        self.region_residence = region_residence
        self.country_residence = country_residence
        self.be_used_for_hu = be_used_for_hu
        self.be_used_for_en = be_used_for_en
        self.be_used_for_de = be_used_for_de
        self.be_used_for_fr = be_used_for_fr
        self.be_used_for_es = be_used_for_es
        self.gender_hu = gender_hu
        self.gender_en = gender_en
        self.gender_de = gender_de
        self.gender_fr = gender_fr
        self.gender_es = gender_es
        self.color_hu = color_hu
        self.color_en = color_en
        self.color_de = color_de
        self.color_fr = color_fr
        self.color_es = color_es
        self.brief_description = brief_description
        self.brief_description_detect_lang = brief_description_detect_lang
        self.description = description
        self.description_detect_lang = description_detect_lang
        self.page_url = page_url
        self.url_01 = url_01
        self.url_02 = url_02
        self.price = price
        self.last_modification_user_id = last_modification_user_id
        self.last_modification_user_name = last_modification_user_name

    def __repr__(self):
        return '<Animal %r>' % self.id


class AnimalPhotos(db.Model, DBCommit):
    __tablename__ = 'animal_photos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=True)
    animal_id = db.Column(db.Integer, unique=False, nullable=True)
    img_01 = db.Column(db.String, unique=False, nullable=True)
    img_01_data = db.Column(db.String, unique=False, nullable=True)
    img_02 = db.Column(db.String, unique=False, nullable=True)
    img_02_data = db.Column(db.String, unique=False, nullable=True)
    img_03 = db.Column(db.String, unique=False, nullable=True)
    img_03_data = db.Column(db.String, unique=False, nullable=True)
    img_04 = db.Column(db.String, unique=False, nullable=True)
    img_04_data = db.Column(db.String, unique=False, nullable=True)
    img_05 = db.Column(db.String, unique=False, nullable=True)
    img_05_data = db.Column(db.String, unique=False, nullable=True)
    img_06 = db.Column(db.String, unique=False, nullable=True)
    img_06_data = db.Column(db.String, unique=False, nullable=True)
    img_07 = db.Column(db.String, unique=False, nullable=True)
    img_07_data = db.Column(db.String, unique=False, nullable=True)
    img_08 = db.Column(db.String, unique=False, nullable=True)
    img_08_data = db.Column(db.String, unique=False, nullable=True)
    img_09 = db.Column(db.String, unique=False, nullable=True)
    img_09_data = db.Column(db.String, unique=False, nullable=True)
    img_10 = db.Column(db.String, unique=False, nullable=True)
    img_10_data = db.Column(db.String, unique=False, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id,
                 animal_id,
                 img_01, img_01_data,
                 img_02, img_02_data,
                 img_03, img_03_data,
                 img_04, img_04_data,
                 img_05, img_05_data,
                 img_06, img_06_data,
                 img_07, img_07_data,
                 img_08, img_08_data,
                 img_09, img_09_data,
                 img_10, img_10_data,
                 ):
        self.user_id = user_id
        self.animal_id = animal_id
        self.img_01 = img_01
        self.img_01_data = img_01_data
        self.img_02 = img_02
        self.img_02_data = img_02_data
        self.img_03 = img_03
        self.img_03_data = img_03_data
        self.img_04 = img_04
        self.img_04_data = img_04_data
        self.img_05 = img_05
        self.img_05_data = img_05_data
        self.img_06 = img_06
        self.img_06_data = img_06_data
        self.img_07 = img_07
        self.img_07_data = img_07_data
        self.img_08 = img_08
        self.img_08_data = img_08_data
        self.img_09 = img_09
        self.img_09_data = img_09_data
        self.img_10 = img_10
        self.img_10_data = img_10_data

    def __repr__(self):
        return '<AnimalPhotos %r>' % self.id


class AnimalVideos(db.Model, DBCommit):
    __tablename__ = 'animal_videos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=True)
    animal_id = db.Column(db.Integer, unique=False, nullable=True)
    video_01 = db.Column(db.String, unique=False, nullable=True)
    video_01_data = db.Column(db.String, unique=False, nullable=True)
    youtube_id = db.Column(db.String, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, animal_id, video_01, video_01_data):
        self.user_id = user_id
        self.animal_id = animal_id
        self.video_01 = video_01
        self.video_01_data = video_01_data

    def __repr__(self):
        return '<AnimalVideos %r>' % self.id


class AnimalPDF(db.Model, DBCommit):
    __tablename__ = 'animal_pdf'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=True)
    animal_id = db.Column(db.Integer, unique=False, nullable=True)
    x_ray = db.Column(db.String, unique=False, nullable=True)
    x_ray_data = db.Column(db.String, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, animal_id,
                 x_ray, x_ray_data):
        self.user_id = user_id
        self.animal_id = animal_id
        self.x_ray = x_ray
        self.x_ray_data = x_ray_data

    def __repr__(self):
        return '<AnimalPDF %r>' % self.id


class Online(db.Model, DBCommit):
    __tablename__ = 'online'

    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String)
    online = db.Column(db.String, default="False")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<Online %r>' % self.id


class Messages(db.Model, DBCommit):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, index=True)
    sender_first_name = db.Column(db.String)
    sender_last_name = db.Column(db.String)
    sender_username = db.Column(db.String)
    host_id = db.Column(db.Integer, index=True)
    host_first_name = db.Column(db.String)
    host_last_name = db.Column(db.String)
    host_username = db.Column(db.String)
    message = db.Column(db.String)
    received = db.Column(db.String, default="False")
    sender_assistant = db.Column(db.String, default="False")
    room = db.Column(db.String)
    archive_sender_id = db.Column(db.Integer)
    archive_host_id = db.Column(db.Integer)
    two_sided_archiving = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, sender_id, sender_first_name, sender_last_name, sender_username, host_id, host_first_name,
                 host_last_name, host_username,
                 message, room):
        self.sender_id = sender_id
        self.sender_first_name = sender_first_name
        self.sender_last_name = sender_last_name
        self.sender_username = sender_username
        self.host_id = host_id,
        self.host_first_name = host_first_name
        self.host_last_name = host_last_name
        self.host_username = host_username
        self.message = message
        self.room = room

    def __repr__(self):
        return '<Messages %r>' % self.id


class NotificationSettings(db.Model, DBCommit):
    __tablename__ = 'notification_settings'

    id = db.Column(db.Integer, primary_key=True)
    assistant = db.Column(db.Integer)
    notifications_01 = db.Column(db.Boolean, default=True)
    notifications_02 = db.Column(db.Boolean, default=True)
    notifications_03 = db.Column(db.Boolean, default=True)
    notifications_04 = db.Column(db.Boolean, default=True)
    notifications_05 = db.Column(db.Boolean, default=True)
    notifications_06 = db.Column(db.Boolean, default=True)
    lang = db.Column(db.String, default="en")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, assistant):
        self.assistant = assistant

    def __repr__(self):
        return '<NotificationSettings %r>' % self.id


class Rating(db.Model, DBCommit):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    animal_id = db.Column(db.Integer, unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, animal_id, rating):
        self.user_id = user_id
        self.animal_id = animal_id
        self.rating = rating

    def __repr__(self):
        return '<Rating %r>' % self.id


class Questions(db.Model, DBCommit):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    question = db.Column(db.String)
    question_detect_lang = db.Column(db.String)
    editing = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    answers = db.relationship('Answers',
                              secondary=answers,
                              backref='answers_backref',
                              cascade='save-update, delete',
                              lazy='dynamic')

    questions_history = db.relationship('QuestionsHistory',
                                        secondary=questions_history,
                                        backref='questions_history_backref',
                                        cascade='save-update, delete',
                                        lazy='dynamic')

    def __init__(self, animal_id, user_id, question, question_detect_lang):
        self.animal_id = animal_id
        self.user_id = user_id
        self.question = question
        self.question_detect_lang = question_detect_lang

    def __repr__(self):
        return '<Questions %r>' % self.id


class QuestionsHistory(db.Model, DBCommit):
    __tablename__ = 'questions_history'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    question = db.Column(db.String)
    question_detect_lang = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, question_id, question, question_detect_lang):
        self.question_id = question_id
        self.question = question
        self.question_detect_lang = question_detect_lang

    def __repr__(self):
        return '<QuestionsHistory %r>' % self.id


class Answers(db.Model, DBCommit):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    answer = db.Column(db.String)
    answer_detect_lang = db.Column(db.String)
    editing = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    answers_history = db.relationship('AnswersHistory',
                                      secondary=answers_history,
                                      backref='answers_history_backref',
                                      cascade='save-update, delete',
                                      lazy='dynamic')

    def __init__(self, question_id, user_id, answer, answer_detect_lang):
        self.question_id = question_id
        self.user_id = user_id
        self.answer = answer
        self.answer_detect_lang = answer_detect_lang

    def __repr__(self):
        return '<Answers %r>' % self.id


class AnswersHistory(db.Model, DBCommit):
    __tablename__ = 'answers_history'

    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer)
    answer = db.Column(db.String)
    answer_detect_lang = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, answer_id, answer, answer_detect_lang):
        self.answer_id = answer_id
        self.answer = answer
        self.answer_detect_lang = answer_detect_lang

    def __repr__(self):
        return '<AnswersHistory %r>' % self.id


class Talking(db.Model, DBCommit):
    __tablename__ = 'talking'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    subcategory_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    experience = db.Column(db.String)
    experience_detect_lang = db.Column(db.String)
    vote = db.Column(db.Integer, default=0)
    editing = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    talking_history = db.relationship('TalkingHistory',
                                      secondary=talking_history,
                                      backref='talking_history_backref',
                                      cascade='save-update, delete',
                                      lazy='dynamic')

    talking_answer = db.relationship('TalkingAnswer',
                                     secondary=talking_answer,
                                     backref='talking_answer_backref',
                                     cascade='save-update, delete',
                                     lazy='dynamic')

    talking_vote = db.relationship('TalkingVote',
                                   secondary=talking_vote,
                                   backref='talking_vote_backref',
                                   cascade='save-update, delete',
                                   lazy='dynamic')

    def __init__(self, category_id, subcategory_id, user_id, experience, experience_detect_lang):
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.user_id = user_id
        self.experience = experience
        self.experience_detect_lang = experience_detect_lang

    def __repr__(self):
        return '<Talking %r>' % self.id


class TalkingHistory(db.Model, DBCommit):
    __tablename__ = 'talking_history'

    id = db.Column(db.Integer, primary_key=True)
    talking_id = db.Column(db.Integer)
    experience = db.Column(db.String)
    experience_detect_lang = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, talking_id, experience, experience_detect_lang):
        self.talking_id = talking_id
        self.experience = experience
        self.experience_detect_lang = experience_detect_lang

    def __repr__(self):
        return '<TalkingHistory %r>' % self.id


class TalkingAnswer(db.Model, DBCommit):
    __tablename__ = 'talking_answer'

    id = db.Column(db.Integer, primary_key=True)
    talking_id = db.Column(db.Integer)
    talking_answer_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    answer = db.Column(db.String)
    answer_detect_lang = db.Column(db.String)
    answer_type = db.Column(db.String)
    editing = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    talking_answer_history = db.relationship('TalkingAnswerHistory',
                                             secondary=talking_answer_history,
                                             backref='talking_answer_history_backref',
                                             cascade='save-update, delete',
                                             lazy='dynamic')

    def __init__(self, talking_id, user_id, answer, answer_detect_lang, answer_type):
        self.talking_id = talking_id
        self.user_id = user_id
        self.answer = answer
        self.answer_detect_lang = answer_detect_lang
        self.answer_type = answer_type

    def __repr__(self):
        return '<TalkingAnswer %r>' % self.id


class TalkingAnswerHistory(db.Model, DBCommit):
    __tablename__ = 'talking_answer_history'

    id = db.Column(db.Integer, primary_key=True)
    talking_id = db.Column(db.Integer)
    answer = db.Column(db.String)
    answer_detect_lang = db.Column(db.String)
    answer_type = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, talking_id, answer, answer_detect_lang, answer_type):
        self.talking_id = talking_id
        self.answer = answer
        self.answer_detect_lang = answer_detect_lang
        self.answer_type = answer_type

    def __repr__(self):
        return '<TalkingAnswerHistory %r>' % self.id


class TalkingVote(db.Model, DBCommit):
    __tablename__ = 'talking_vote'

    id = db.Column(db.Integer, primary_key=True)
    talking_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    vote = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, talking_id, user_id, vote):
        self.talking_id = talking_id
        self.user_id = user_id
        self.vote = vote

    def __repr__(self):
        return '<TalkingVote %r>' % self.id


class Translate(db.Model, DBCommit):
    __tablename__ = 'translate'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)
    target = db.Column(db.String)
    source_data = db.Column(db.String)
    target_data = db.Column(db.String)
    translate_type = db.Column(db.String)
    translate_type_id = db.Column(db.Integer)
    translate_type_data = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, source, target, source_data, target_data):
        self.source = source
        self.target = target
        self.source_data = source_data
        self.target_data = target_data

    def __repr__(self):
        return '<Translate %r>' % self.id


class TranslateTalking(db.Model, DBCommit):
    __tablename__ = 'translate_talking'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)
    target = db.Column(db.String)
    source_data = db.Column(db.String)
    target_data = db.Column(db.String)
    translate_type = db.Column(db.String)
    translate_type_id = db.Column(db.Integer)
    translate_type_data = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, source, target, source_data, target_data):
        self.source = source
        self.target = target
        self.source_data = source_data
        self.target_data = target_data

    def __repr__(self):
        return '<TranslateTalking %r>' % self.id


class Wishlist(db.Model, DBCommit):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    animal_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, animal_id):
        self.user_id = user_id
        self.animal_id = animal_id

    def __repr__(self):
        return '<Wishlist %r>' % self.id

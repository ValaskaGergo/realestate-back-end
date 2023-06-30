# -*- coding: utf-8 -*-
import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import urllib3

app = Flask(__name__)

env_file = find_dotenv(".env.template")
load_dotenv(env_file)
app.config.from_object(os.getenv('SERVER'))
# app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ======== Flask Commands ======================================================================= #
from app.commands import mod as commands

app.register_blueprint(commands)

# ======== Register Views ======================================================================= #

# -------- API ---------------------------------------------------- #
from .views.api import mod as api_module

app.register_blueprint(api_module)

# -------- SIGN UP ------------------------------------------------ #
from .views.sign_up import mod as signup_module

app.register_blueprint(signup_module)

# -------- SIGN IN ------------------------------------------------ #
from .views.sign_in import mod as signin_module

app.register_blueprint(signin_module)

# -------- PASSWORD RESET ----------------------------------------- #
from .views.password_reset import mod as password_reset_module

app.register_blueprint(password_reset_module)

# -------- ADMIN SETTINGS ----------------------------------------- #
from .views.admin_settings import mod as admin_settings_module

app.register_blueprint(admin_settings_module)

# -------- USER MANAGEMENT ---------------------------------------- #
from .views.user_management import mod as user_management_module

app.register_blueprint(user_management_module)

# -------- BILLING AND SHIPPING ADDRESS --------------------------- #
from .views.billing_and_shipping_address import mod as billing_and_shipping_address_module

app.register_blueprint(billing_and_shipping_address_module)

# -------- SECURITY ----------------------------------------------- #
from .views.security import mod as security_module

app.register_blueprint(security_module)

# -------- EXCHANGE ----------------------------------------------- #
from .views.exchange import mod as exchange_module

app.register_blueprint(exchange_module)

# -------- BARION PAYMENT ----------------------------------------- #
from .views.barion_payment import mod as barion_payment_module

app.register_blueprint(barion_payment_module)

# -------- PAYPAL PAYMENT ----------------------------------------- #
from .views.paypal_payment import mod as paypal_payment_module

app.register_blueprint(paypal_payment_module)

# -------- INVOICES ----------------------------------------------- #
from .views.invoices import mod as invoices_module

app.register_blueprint(invoices_module)

# -------- CATEGORY ----------------------------------------------- #
from .views.category import mod as category_module

app.register_blueprint(category_module)

# -------- SUBCATEGORY -------------------------------------------- #
from .views.subcategory import mod as subcategory_module

app.register_blueprint(subcategory_module)

# -------- ANIMAL ------------------------------------------------- #
from .views.animal import mod as animal_module

app.register_blueprint(animal_module)

# -------- NOTIFICATION ------------------------------------------- #
from .views.notification import mod as notification_module

app.register_blueprint(notification_module)

# -------- FILTER ------------------------------------------------- #
from .views.filter import mod as filter_module

app.register_blueprint(filter_module)

# -------- FULL PAGE ---------------------------------------------- #
from .views.full_page import mod as full_page_module

app.register_blueprint(full_page_module)

# -------- RATING ------------------------------------------------- #
from .views.rating import mod as rating_module

app.register_blueprint(rating_module)

# -------- Questions And Answers ---------------------------------- #
from .views.questions_and_answers import mod as questions_and_answers_module

app.register_blueprint(questions_and_answers_module)

# -------- Talking ------------------------------------------------ #
from .views.talking import mod as talking_module

app.register_blueprint(talking_module)

# -------- Translate ------------------------------------------------ #
from .views.translate import mod as translate_module

app.register_blueprint(translate_module)

# -------- Status ------------------------------------------------ #
from .views.status import mod as status_module

app.register_blueprint(status_module)

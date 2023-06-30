# -*- coding: utf-8 -*-
from app import app
from config import _basedir
from flask import Blueprint, make_response, jsonify, request, json
from flask_restful import Api, Resource, reqparse
from app.models.models import User, UserProfile, UserPermission, UserBillingInformation, UserShippingInformation, \
    UserSecondaryEmail, Online, NotificationSettings, Messages, AdminSettings
import io
from datetime import datetime, timedelta
from sqlalchemy import or_, desc
from dateutil.parser import parse
import itertools
from .utilities.utility import Difference

mod = Blueprint('api_module', __name__)
api = Api(mod)

get_user_data = reqparse.RequestParser()
get_user_data.add_argument('email', required=False)
get_user_data.add_argument('user_id', required=False)
get_user_data.add_argument('lang', required=False)


class GetApiStatus(Resource):
    @staticmethod
    def get():
        api_key = request.headers['X-Api-Key']

        if api_key == app.config['API_KEY']:
            try:
                data = {"status": "success"}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetUserData(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_user_data.parse_args()

        email = data['email']
        user_id = data['user_id']
        lang = data['lang']

        if api_key == app.config['API_KEY']:
            try:
                user = None
                if email is not None:
                    user = User.query.filter_by(email=email).first()
                elif user_id is not None:
                    user = User.query.filter_by(id=user_id).first()

                if user is not None:
                    user_permission = UserPermission \
                        .query.join(User.permission) \
                        .filter(User.id == user.id).first()

                    user_profile = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == user.id).first()

                    user_billing_information = UserBillingInformation \
                        .query.join(User.billing_information) \
                        .filter(User.id == user.id).first()

                    user_shipping_information = UserShippingInformation \
                        .query.join(User.shipping_information) \
                        .filter(User.id == user.id).first()

                    user_secondary_email = UserSecondaryEmail \
                        .query.join(User.secondary_email) \
                        .filter(User.id == user.id).first()

                    user_online = Online \
                        .query.join(User.online) \
                        .filter(User.id == user.id).first()

                    user_online.online = "True"
                    user_online.db_post()

                    notification_settings = NotificationSettings \
                        .query.join(User.notification_settings) \
                        .filter(User.id == user.id).first()

                    datetime_now = datetime.now()
                    if user_permission.is_worker != "True":
                        if user_permission.subscribed != "False" and datetime_now > user_permission.subscribed_end:
                            user_permission.subscribed = "False"
                            user_permission.subscribed_start = None
                            user_permission.subscribed_end = None
                            user_permission.db_post()

                    if user_billing_information.currency is not None:
                        exchange_json = io.open(_basedir + "/app/json/exchange.json", 'r')
                        exchange_json_read = json.loads(exchange_json.read())

                        vat = "0." + user_billing_information.country_vat

                        eur1_to_net = 1
                        eur1_to_net_currency = float(exchange_json_read['rates'][user_billing_information.currency])
                        if user_billing_information.country_vat != "0":
                            eur1_to_total = 1 + (1 * float(vat))
                            eur1_to_total_currency = eur1_to_net_currency + (eur1_to_net_currency * float(vat))
                        else:
                            eur1_to_total = eur1_to_net
                            eur1_to_total_currency = eur1_to_net_currency

                        eur1_to_net = round(eur1_to_net, 2)
                        eur1_to_total = round(eur1_to_total, 2)
                        eur1_to_net_currency = round(eur1_to_net_currency, 2)
                        eur1_to_total_currency = round(eur1_to_total_currency, 2)
                    else:
                        eur1_to_net = None
                        eur1_to_total = None
                        eur1_to_net_currency = None
                        eur1_to_total_currency = None

                    messages_received = Messages.query \
                        .filter(Messages.host_id == user.id) \
                        .filter(Messages.received == "False") \
                        .count()

                    if lang is not None:
                        try:
                            notification_settings = NotificationSettings \
                                .query.join(User.notification_settings) \
                                .filter(User.id == user.id).first()
                            notification_settings.lang = lang
                            notification_settings.db_post()
                        except AttributeError:
                            pass

                    try:
                        date1 = datetime.strptime(str(datetime_now), "%Y-%m-%d %H:%M:%S.%f")
                        date2 = datetime.strptime(str(user_permission.subscribed_end), "%Y-%m-%d %H:%M:%S.%f")
                        subscribed_start_end_difference = Difference.diff_from(Difference.diff_to(date2, date1))
                    except:
                        subscribed_start_end_difference = None

                    if user_permission.subscribed_type == 1 or user_permission.subscribed_type == 4 or user_permission.subscribed_type == 7:
                        subscribed_ads_default = AdminSettings.query.filter_by(id=10).first().settings_value
                        subscribed_chat_default = AdminSettings.query.filter_by(id=13).first().settings_value
                    elif user_permission.subscribed_type == 2 or user_permission.subscribed_type == 5 or user_permission.subscribed_type == 8:
                        subscribed_ads_default = AdminSettings.query.filter_by(id=11).first().settings_value
                        subscribed_chat_default = AdminSettings.query.filter_by(id=14).first().settings_value
                    elif user_permission.subscribed_type == 3 or user_permission.subscribed_type == 6 or user_permission.subscribed_type == 9:
                        subscribed_ads_default = AdminSettings.query.filter_by(id=12).first().settings_value
                        subscribed_chat_default = AdminSettings.query.filter_by(id=15).first().settings_value
                    else:
                        subscribed_ads_default = None
                        subscribed_chat_default = None

                    payload = {
                        "is_logged": True,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "deleted": user.deleted,
                            "created_at": user.created_at,
                            "updated_at": user.updated_at
                        },
                        "user_profile": {
                            "username": user_profile.username
                        },
                        "user_online": {
                            "sid": user_online.sid,
                            "online": user_online.online,
                            "created_at": user_online.created_at,
                            "updated_at": user_online.updated_at
                        },
                        "user_notification_settings": {
                            "assistant": notification_settings.assistant,
                            "notifications_01": notification_settings.notifications_01,
                            "notifications_02": notification_settings.notifications_02,
                            "notifications_03": notification_settings.notifications_03,
                            "notifications_04": notification_settings.notifications_04,
                            "notifications_05": notification_settings.notifications_05,
                            "notifications_06": notification_settings.notifications_06,
                            "lang": notification_settings.lang,
                            "created_at": notification_settings.created_at,
                            "updated_at": notification_settings.updated_at
                        },
                        "user_permission": {
                            "is_worker": user_permission.is_worker,
                            "is_admin": user_permission.is_admin,
                            "is_admin_settings_management": user_permission.is_admin_settings_management,
                            "is_user_management": user_permission.is_user_management,
                            "is_category_management": user_permission.is_category_management,
                            "is_notifications": user_permission.is_notifications,
                            "subscribed": user_permission.subscribed,
                            "subscribed_start": user_permission.subscribed_start,
                            "subscribed_end": user_permission.subscribed_end,
                            "subscribed_start_end_difference": subscribed_start_end_difference,
                            "subscribed_type": user_permission.subscribed_type,
                            "subscribed_monthly": user_permission.subscribed_monthly,
                            "subscribed_ads": user_permission.subscribed_ads,
                            "subscribed_ads_default": subscribed_ads_default,
                            "subscribed_chat": user_permission.subscribed_chat,
                            "subscribed_chat_default": subscribed_chat_default,
                            "inactive_account": user_permission.inactive_account,
                            "last_modification_user_id": user_permission.last_modification_user_id,
                            "last_modification_user_name": user_permission.last_modification_user_name,
                            "updated_at": user_permission.updated_at
                        },
                        "user_billing_information": {
                            "is_company": user_billing_information.is_company,
                            "first_name": user_billing_information.first_name,
                            "last_name": user_billing_information.last_name,
                            "company_name": user_billing_information.company_name,
                            "company_tax": user_billing_information.company_tax,
                            "phone": user_billing_information.phone,
                            "email": user_billing_information.email,
                            "country": user_billing_information.country,
                            "country_vat": user_billing_information.country_vat,
                            "payment_country_vat": user_billing_information.payment_country_vat,
                            "zip_number": user_billing_information.zip_number,
                            "place": user_billing_information.place,
                            "street": user_billing_information.street,
                            "currency": user_billing_information.currency,
                            "eur1_to_net": eur1_to_net,
                            "eur1_to_gross": eur1_to_total,
                            "eur1_to_net_currency": eur1_to_net_currency,
                            "eur1_to_gross_currency": eur1_to_total_currency,
                            "is_shipping_address": user_billing_information.is_shipping_address,
                            "billingo_partner_id": user_billing_information.billingo_partner_id,
                            "completed": user_billing_information.completed,
                            "last_modification_user_id": user_billing_information.last_modification_user_id,
                            "last_modification_user_name": user_billing_information.last_modification_user_name,
                            "created_at": user_billing_information.created_at,
                            "updated_at": user_billing_information.updated_at
                        },
                        "user_shipping_information": {
                            "first_name": user_shipping_information.first_name,
                            "last_name": user_shipping_information.last_name,
                            "company_name": user_shipping_information.company_name,
                            "phone": user_shipping_information.phone,
                            "email": user_shipping_information.email,
                            "country": user_shipping_information.country,
                            "zip_number": user_shipping_information.zip_number,
                            "place": user_shipping_information.place,
                            "street": user_shipping_information.street,
                            "currency": user_billing_information.currency,
                        },
                        "user_secondary_email": {
                            "email": user_secondary_email.email
                        },
                        "messages_received": {
                            "received": messages_received
                        }
                    }

                    data = {"status": "success", "payload": payload}
                    return make_response(jsonify(data), 200)
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(GetApiStatus, '/get-api-status')
api.add_resource(GetUserData, '/get-user-data')

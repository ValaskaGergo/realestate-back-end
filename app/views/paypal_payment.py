# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify, json
from app.models.models import User, AdminSettings, PayPalPayment, UserPermission, UserBillingInformation
from flask_restful import Api, Resource, reqparse
import requests
from app.views.utilities.utility import SecretKey, PayPal, VatLayer
from datetime import datetime, timedelta
from dateutil import parser

mod = Blueprint('paypal_payment_module', __name__)
api = Api(mod)

paypal_payment_start = reqparse.RequestParser()
paypal_payment_start.add_argument('email', required=True)
paypal_payment_start.add_argument('payment_data', required=True)
paypal_payment_start.add_argument('payment_country_vat', required=True)
paypal_payment_start.add_argument('eur1_to_net', required=True)
paypal_payment_start.add_argument('eur1_to_gross', required=True)
paypal_payment_start.add_argument('eur1_to_net_currency', required=True)
paypal_payment_start.add_argument('eur1_to_gross_currency', required=True)
paypal_payment_start.add_argument('billingo_partner_id', required=True)

paypal_payment_id_info = reqparse.RequestParser()
paypal_payment_id_info.add_argument('payment_id', required=True)


class PayPalPaymentStart(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = paypal_payment_start.parse_args()

        email = data['email']
        payment_data = json.loads(data['payment_data'])
        admin_settings_id = payment_data['admin_settings_id']
        payment_country_vat = data['payment_country_vat']
        eur1_to_net = float(data['eur1_to_net'])
        eur1_to_gross = float(data['eur1_to_gross'])
        eur1_to_net_currency = float(data['eur1_to_net_currency'])
        eur1_to_gross_currency = float(data['eur1_to_gross_currency'])
        billingo_partner_id = data['billingo_partner_id']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    admin_settings_query = AdminSettings.query.filter_by(id=admin_settings_id).first()

                    price = float(admin_settings_query.settings_value)
                    account_month = None
                    account_day = None
                    eur_net = None
                    eur_gross = None

                    if admin_settings_id == 1:
                        account_month = 1
                        account_day = 30.4368499
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 2:
                        account_month = 1
                        account_day = 30.4368499
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 3:
                        account_month = 1
                        account_day = 30.4368499
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 4:
                        account_month = 3
                        account_day = 91.3105499
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 5:
                        account_month = 3
                        account_day = 91.3105499
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 6:
                        account_month = 3
                        account_day = 91.3105499
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 7:
                        account_month = 12
                        account_day = 365.242199
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 8:
                        account_month = 12
                        account_day = 365.242199
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if admin_settings_id == 9:
                        account_month = 12
                        account_day = 365.242199
                        eur_net = price * eur1_to_net
                        eur_gross = price * eur1_to_gross
                        currency_net = price * eur1_to_net_currency
                        currency_gross = price * eur1_to_gross_currency
                    if payment_country_vat == "0":
                        price_total = eur_net
                    else:
                        price_total = eur_gross

                    url = app.config['PAYPAL_API_URL'] + "/v2/checkout/orders"
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + PayPal.generate_token(),
                        'Prefer': 'return=representation'
                    }
                    payload = json.dumps({
                        "intent": "CAPTURE",
                        "purchase_units": [
                            {
                                "reference_id": SecretKey.secret_key(32),
                                "description": "account-day-" + str(account_day),
                                "amount": {
                                    "currency_code": "EUR",
                                    "value": round(price_total, 2)
                                }
                            }
                        ],
                        "application_context": {
                            "return_url": app.config['SERVER_URL'] + "/account-payment",
                            "cancel_url": app.config['SERVER_URL'] + "/account-payment",
                            "brand_name": app.config['BRAND_NAME']
                        }
                    })
                    r = requests.post(url, headers=headers, data=payload, verify=app.config['TLS_VERIFY'])

                    if r.status_code == 201:
                        data = r.json()

                        url = app.config['PAYPAL_URL'] + "/checkoutnow?token=" + data['id']
                        data = {"status": 'success', 'payment': 'paypal', 'url': url, 'message': r.json()}

                        paypal_payment_payload = PayPalPayment(
                            user_id=user.id,
                            payment_type="account",
                            payment_id=data['message']['id'],
                            payment_request_id=data['message']['purchase_units'][0]['reference_id'],
                            status=data['message']['status'],
                            price=round(eur_net, 2),
                            vat=payment_country_vat,
                            total=round(price_total, 2),
                            account_type=admin_settings_id
                        )

                        paypal_payment_payload.paypal_payment_backref.append(user)
                        paypal_payment_payload.db_post()

                        return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class PayPalPaymentIdStatus(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = paypal_payment_id_info.parse_args()

        payment_id = data['payment_id']

        if api_key == app.config['API_KEY']:
            try:
                url = app.config['PAYPAL_API_URL'] + "/v2/checkout/orders/" + payment_id
                headers = {
                    'Authorization': 'Bearer ' + PayPal.generate_token(),
                    "Content-Type": "application/json"
                }
                r = requests.get(url, headers=headers, verify=app.config['TLS_VERIFY'])

                if r.status_code == 200:
                    data = r.json()
                    status = data['status']

                    paypal_payment_query = PayPalPayment.query.filter_by(payment_id=data['id']).first()

                    if paypal_payment_query is not None:
                        if status == "CREATED":
                            paypal_payment_query.db_delete()

                            data = {"status": 'success', 'message': {"status": "CREATED"}}
                            return make_response(jsonify(data), 200)
                        if status == "APPROVED":
                            user_permission = UserPermission \
                                .query.join(User.permission) \
                                .filter(User.id == paypal_payment_query.user_id).first()

                            paypal_payment_query.order_number = data['purchase_units'][0]['description']
                            paypal_payment_query.status = data['status']
                            paypal_payment_query.funding_source = "PayPal"
                            paypal_payment_query.completed_at = data['create_time']
                            paypal_payment_query.transaction_id = data['purchase_units'][0]['reference_id']
                            paypal_payment_query.total = data['purchase_units'][0]['amount']['value']
                            paypal_payment_query.currency = data['purchase_units'][0]['amount'][
                                'currency_code']
                            paypal_payment_query.db_post()

                            days = data['purchase_units'][0]['description'].split("-")[2]
                            completed_at_parse = parser.parse(data['create_time'])
                            if app.config['ENV'] == 'production':
                                end_date = completed_at_parse + timedelta(days=float(days))
                            else:
                                # end_date = completed_at_parse + timedelta(minutes=int(app.config['ACCOUNT_MINUTE']))
                                end_date = completed_at_parse + timedelta(days=float(days))

                            user_permission.subscribed_type = None
                            user_permission.subscribed_monthly = None
                            user_permission.subscribed_ads = None
                            user_permission.subscribed_chat = None

                            if paypal_payment_query.account_type == 1:
                                user_permission.subscribed_type = 1
                                user_permission.subscribed_monthly = 1
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=10).first().settings_value
                                user_permission.subscribed_chat = AdminSettings.query.filter_by(
                                    id=13).first().settings_value
                            elif paypal_payment_query.account_type == 2:
                                user_permission.subscribed_type = 2
                                user_permission.subscribed_monthly = 1
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=11).first().settings_value
                                user_permission.subscribed_chat = AdminSettings.query.filter_by(
                                    id=14).first().settings_value
                            elif paypal_payment_query.account_type == 3:
                                user_permission.subscribed_type = 3
                                user_permission.subscribed_monthly = 1
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=12).first().settings_value
                                user_permission.subscribed_chat = AdminSettings.query.filter_by(
                                    id=15).first().settings_value
                            elif paypal_payment_query.account_type == 4:
                                user_permission.subscribed_type = 4
                                user_permission.subscribed_monthly = 3
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=10).first().settings_value
                                user_permission.subscribed_chat = int(AdminSettings.query.filter_by(id=13).first().settings_value) * 3
                            elif paypal_payment_query.account_type == 5:
                                user_permission.subscribed_type = 5
                                user_permission.subscribed_monthly = 3
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=11).first().settings_value
                                user_permission.subscribed_chat = int(AdminSettings.query.filter_by(id=14).first().settings_value) * 3
                            elif paypal_payment_query.account_type == 6:
                                user_permission.subscribed_type = 6
                                user_permission.subscribed_monthly = 3
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=12).first().settings_value
                                user_permission.subscribed_chat = AdminSettings.query.filter_by(
                                    id=15).first().settings_value
                            elif paypal_payment_query.account_type == 7:
                                user_permission.subscribed_type = 7
                                user_permission.subscribed_monthly = 12
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=10).first().settings_value
                                user_permission.subscribed_chat = int(AdminSettings.query.filter_by(id=13).first().settings_value) * 12
                            elif paypal_payment_query.account_type == 8:
                                user_permission.subscribed_type = 8
                                user_permission.subscribed_monthly = 12
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=11).first().settings_value
                                user_permission.subscribed_chat = int(AdminSettings.query.filter_by(id=14).first().settings_value) * 12
                            elif paypal_payment_query.account_type == 9:
                                user_permission.subscribed_type = 9
                                user_permission.subscribed_monthly = 12
                                user_permission.subscribed_ads = AdminSettings.query.filter_by(
                                    id=12).first().settings_value
                                user_permission.subscribed_chat = AdminSettings.query.filter_by(
                                    id=15).first().settings_value

                            user_permission.subscribed = "True"
                            # user_permission.subscribed_start = data['create_time']
                            user_permission.subscribed_start = datetime.now()
                            user_permission.subscribed_end = end_date
                            user_permission.db_post()

                    data = {"status": 'success', 'message': r.json()}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


@mod.route('/paypal-account-payment-webhook', methods=['POST'])
def paypal_account_payment_webhook():
    data = request.json
    status = data['resource']['status']

    paypal_payment_query = PayPalPayment.query.filter_by(payment_id=data['resource']['id']).first()

    if paypal_payment_query is not None:
        if status == "APPROVED":
            user_permission = UserPermission \
                .query.join(User.permission) \
                .filter(User.id == paypal_payment_query.user_id).first()

            paypal_payment_query.order_number = data['resource']['purchase_units'][0]['description']
            paypal_payment_query.status = data['resource']['status']
            paypal_payment_query.funding_source = "PayPal"
            paypal_payment_query.completed_at = data['resource']['create_time']
            paypal_payment_query.transaction_id = data['resource']['purchase_units'][0]['reference_id']
            paypal_payment_query.total = data['resource']['purchase_units'][0]['amount']['value']
            paypal_payment_query.currency = data['resource']['purchase_units'][0]['amount'][
                'currency_code']
            paypal_payment_query.db_post()

            days = data['resource']['purchase_units'][0]['description'].split("-")[2]
            completed_at_parse = parser.parse(data['resource']['create_time'])
            if app.config['ENV'] == 'production':
                end_date = completed_at_parse + timedelta(days=float(days))
            else:
                # end_date = completed_at_parse + timedelta(minutes=int(app.config['ACCOUNT_MINUTE']))
                end_date = completed_at_parse + timedelta(days=float(days))

            user_permission.subscribed = "True"
            # user_permission.subscribed_start = data['resource']['create_time']
            user_permission.subscribed_start = datetime.now()
            user_permission.subscribed_end = end_date
            user_permission.db_post()

            #  Start Billingo Documents
            user_billing_information = UserBillingInformation \
                .query.join(User.billing_information) \
                .filter(User.id == paypal_payment_query.user_id).first()

            now = datetime.now()

            days = int(paypal_payment_query.order_number.split("-")[2].split(".")[0])
            if days == 365.242199:
                month = 12
            elif days == 91.3105499:
                month = 6
            elif days == 30.4368499:
                month = 1
            else:
                month = 1

            if user_billing_information.country == "HU":
                name = app.config['BRAND_NAME'] + " fiók " + str(month) + " hónap"
                language = "hu"
                unit = "darab"
            else:
                name = app.config['BRAND_NAME'] + " account " + str(month) + " month"
                language = "en"
                unit = "piece"

            if VatLayer.is_ue_country(
                    user_billing_information.country) is True and \
                    user_billing_information.payment_country_vat == "0":
                entitlement = ""
                vat = "EU"
            elif VatLayer.is_ue_country(
                    user_billing_information.country) is False and paypal_payment_query.vat == "0":
                entitlement = "TAM"
                vat = str(paypal_payment_query.vat) + "%"
            else:
                entitlement = ""
                vat = str(paypal_payment_query.vat) + "%"

            url = app.config['BILLINGO_API_URL'] + "/documents"
            headers = {
                'accept': 'application/json',
                'X-API-KEY': app.config['BILLINGO_API_KEY'],
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "partner_id": int(user_billing_information.billingo_partner_id),
                "block_id": 0,
                "type": app.config['BILLINGO_DOCUMENTS_TYPE'],
                "fulfillment_date": now.strftime("%Y-%m-%d"),
                "due_date": now.strftime("%Y-%m-%d"),
                "payment_method": "barion",
                "language": language.lower(),
                "currency": "EUR",
                "conversion_rate": 1,
                "paid": bool(True),
                "items": [
                    {
                        "name": name,
                        "unit_price": paypal_payment_query.price,
                        "unit_price_type": "net",
                        "quantity": 1,
                        "unit": unit,
                        "vat": vat,
                        "entitlement": entitlement
                    }
                ]
            })
            r = requests.post(url, headers=headers, data=payload, verify=app.config['TLS_VERIFY'])
            if r.status_code == 201:
                data = r.json()
                url = app.config['BILLINGO_API_URL'] + "/documents/" + str(data['id']) + "/public-url"
                headers = {
                    'accept': 'application/json',
                    'X-API-KEY': app.config['BILLINGO_API_KEY']
                }
                r = requests.get(url, headers=headers, data=None, verify=app.config['TLS_VERIFY'])
                if r.status_code == 200:
                    data = r.json()
                    paypal_payment_query.billing_url = data['public_url']
                    paypal_payment_query.db_post()
            #  End Billingo Documents

    data = {"status": 'success'}
    return make_response(jsonify(data), 200)


api.add_resource(PayPalPaymentStart, '/paypal-payment-start')
api.add_resource(PayPalPaymentIdStatus, '/paypal-payment-id-status')

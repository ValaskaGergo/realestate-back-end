# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify, json
from flask_restful import Api, Resource, reqparse
from .utilities.validators import Validation
from .utilities.utility import VatLayer
import phonenumbers
from app.models.models import User, UserBillingInformation, UserShippingInformation, UserProfile
import requests

mod = Blueprint('billing_and_shipping_address_module', __name__)
api = Api(mod)

post_billing_and_shipping_address = reqparse.RequestParser()
post_billing_and_shipping_address.add_argument('email', required=True)
post_billing_and_shipping_address.add_argument('billing_is_company', required=True)
post_billing_and_shipping_address.add_argument('billing_email', required=True)
post_billing_and_shipping_address.add_argument('billing_first_name', required=True)
post_billing_and_shipping_address.add_argument('billing_last_name', required=True)
post_billing_and_shipping_address.add_argument('billing_company_name', required=True)
post_billing_and_shipping_address.add_argument('billing_company_tax', required=True)
post_billing_and_shipping_address.add_argument('billing_phone', required=True)
post_billing_and_shipping_address.add_argument('billing_country', required=True)
post_billing_and_shipping_address.add_argument('billing_zip_number', required=True)
post_billing_and_shipping_address.add_argument('billing_place', required=True)
post_billing_and_shipping_address.add_argument('billing_street', required=True)
post_billing_and_shipping_address.add_argument('billing_currency', required=False)
post_billing_and_shipping_address.add_argument('billing_is_shipping_address', required=True)
post_billing_and_shipping_address.add_argument('last_modification_user_id', required=True)
post_billing_and_shipping_address.add_argument('last_modification_user_name', required=True)

post_billing_and_shipping_address.add_argument('shipping_email', required=True)
post_billing_and_shipping_address.add_argument('shipping_first_name', required=True)
post_billing_and_shipping_address.add_argument('shipping_last_name', required=True)
post_billing_and_shipping_address.add_argument('shipping_company_name', required=True)
post_billing_and_shipping_address.add_argument('shipping_phone', required=True)
post_billing_and_shipping_address.add_argument('shipping_country', required=True)
post_billing_and_shipping_address.add_argument('shipping_zip_number', required=True)
post_billing_and_shipping_address.add_argument('shipping_place', required=True)
post_billing_and_shipping_address.add_argument('shipping_street', required=True)
post_billing_and_shipping_address.add_argument('shipping_currency', required=False)


class BillingAndShippingAddress(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = post_billing_and_shipping_address.parse_args()

        email = data['email']
        billing_is_company = data['billing_is_company']
        billing_email = data['billing_email']
        billing_first_name = data['billing_first_name']
        billing_last_name = data['billing_last_name']
        billing_company_name = data['billing_company_name']
        billing_company_tax = data['billing_company_tax']
        billing_phone = data['billing_phone']
        billing_country = data['billing_country']
        billing_zip_number = data['billing_zip_number']
        billing_place = data['billing_place']
        billing_street = data['billing_street']
        billing_is_shipping_address = data['billing_is_shipping_address']
        billing_currency = data['billing_currency']
        last_modification_user_id = data['last_modification_user_id']
        last_modification_user_name = data['last_modification_user_name']

        shipping_email = data['shipping_email']
        shipping_first_name = data['shipping_first_name']
        shipping_last_name = data['shipping_last_name']
        shipping_company_name = data['shipping_company_name']
        shipping_phone = data['shipping_phone']
        shipping_country = data['shipping_country']
        shipping_zip_number = data['shipping_zip_number']
        shipping_place = data['shipping_place']
        shipping_street = data['shipping_street']
        shipping_currency = data['shipping_currency']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.billing_and_shipping_address(
                    email,
                    billing_is_company,
                    billing_first_name,
                    billing_last_name,
                    billing_phone,
                    billing_email,
                    billing_company_name,
                    billing_company_tax,
                    billing_country,
                    billing_zip_number,
                    billing_place,
                    billing_street,
                    billing_is_shipping_address,
                    shipping_first_name,
                    shipping_last_name,
                    shipping_phone,
                    shipping_email,
                    shipping_country,
                    shipping_zip_number,
                    shipping_place,
                    shipping_street
                )

                if validation['status'] == "success":
                    billing_phone = phonenumbers.parse(billing_phone, None)
                    billing_phone = phonenumbers.format_number(billing_phone, phonenumbers.PhoneNumberFormat.E164)

                    if billing_is_shipping_address == "False":
                        shipping_phone = phonenumbers.parse(shipping_phone, None)
                        shipping_phone = phonenumbers.format_number(shipping_phone, phonenumbers.PhoneNumberFormat.E164)

                    user = User.query.filter_by(email=email).first()

                    user_profile = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == user.id).first()

                    if user is not None:
                        user_billing_information = UserBillingInformation \
                            .query.join(User.billing_information) \
                            .filter(User.id == user.id).first()

                        user_shipping_information = UserShippingInformation \
                            .query.join(User.shipping_information) \
                            .filter(User.id == user.id).first()

                        user_billing_information.is_company = billing_is_company
                        user_billing_information.first_name = billing_first_name
                        user_billing_information.last_name = billing_last_name
                        if billing_is_company == "True":
                            user_billing_information.company_name = billing_company_name
                            user_billing_information.company_tax = billing_company_tax
                        else:
                            user_billing_information.company_name = None
                            user_billing_information.company_tax = None
                        user_billing_information.phone = billing_phone
                        user_billing_information.email = billing_email
                        user_billing_information.country = billing_country
                        country_vat_list = VatLayer.get_vat(billing_is_company, billing_company_tax,
                                                            billing_country)
                        user_billing_information.country_vat = country_vat_list[0]
                        user_billing_information.payment_country_vat = country_vat_list[1]
                        user_billing_information.zip_number = billing_zip_number
                        user_billing_information.place = billing_place
                        user_billing_information.street = billing_street
                        user_billing_information.is_shipping_address = billing_is_shipping_address
                        user_billing_information.currency = billing_currency
                        user_billing_information.completed = "True"

                        user_billing_information.last_modification_user_id = last_modification_user_id
                        user_billing_information.last_modification_user_name = last_modification_user_name

                        if billing_is_shipping_address == "False":
                            user_shipping_information.first_name = shipping_first_name
                            user_shipping_information.last_name = shipping_last_name
                            if billing_is_company == "True":
                                user_shipping_information.company_name = shipping_company_name
                            else:
                                user_shipping_information.company_name = None
                            user_shipping_information.phone = shipping_phone
                            user_shipping_information.email = shipping_email
                            user_shipping_information.country = shipping_country
                            user_shipping_information.zip_number = shipping_zip_number
                            user_shipping_information.place = shipping_place
                            user_shipping_information.street = shipping_street
                            user_shipping_information.currency = shipping_currency
                        else:
                            user_shipping_information.first_name = None
                            user_shipping_information.last_name = None
                            user_shipping_information.company_name = None
                            user_shipping_information.phone = None
                            user_shipping_information.email = None
                            user_shipping_information.country = None
                            user_shipping_information.zip_number = None
                            user_shipping_information.place = None
                            user_shipping_information.street = None
                            user_shipping_information.currency = None

                        user_billing_information.db_post()
                        user_shipping_information.db_post()

                        #  Start Billingo
                        url = app.config['BILLINGO_API_URL'] + "/partners"
                        headers = {
                            'Content-Type': 'application/json',
                            'X-API-KEY': app.config['BILLINGO_API_KEY']
                        }

                        if billing_is_company == "True":
                            name = billing_company_name
                            taxcode = billing_company_tax
                            if billing_country == "HU":
                                tax_type = "HAS_TAX_NUMBER"
                            else:
                                tax_type = "FOREIGN"
                            payload = json.dumps({
                                "name": name,
                                "address": {
                                    "country_code": billing_country,
                                    "post_code": billing_zip_number,
                                    "city": billing_place,
                                    "address": billing_street
                                },
                                "emails": [billing_email],
                                "taxcode": taxcode,
                                "phone": billing_phone,
                                "tax_type": tax_type
                            })
                        else:
                            name = billing_first_name + " " + billing_last_name
                            taxcode = None
                            tax_type = "NO_TAX_NUMBER"
                            payload = json.dumps({
                                "name": name,
                                "address": {
                                    "country_code": billing_country,
                                    "post_code": billing_zip_number,
                                    "city": billing_place,
                                    "address": billing_street
                                },
                                "emails": [billing_email],
                                "phone": billing_phone,
                                "tax_type": tax_type
                            })

                        if user_billing_information.billingo_partner_id is None:
                            r = requests.post(url, headers=headers, data=payload, verify=app.config['TLS_VERIFY'])
                            if r.status_code == 201:
                                data = r.json()
                                user_billing_information.billingo_partner_id = data['id']
                                user_billing_information.db_post()
                        elif user_billing_information.billingo_partner_id is not None:
                            url = app.config[
                                      'BILLINGO_API_URL'] + "/partners/" + str(
                                user_billing_information.billingo_partner_id)
                            r = requests.put(url, headers=headers, data=payload, verify=app.config['TLS_VERIFY'])
                            if r.status_code == 201:
                                pass

                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(BillingAndShippingAddress, '/billing-and-shipping-address')

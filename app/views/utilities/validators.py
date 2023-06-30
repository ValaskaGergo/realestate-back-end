# -*- coding: utf-8 -*-
import re
from app import app
from app.models.models import User, UserSecondaryEmail, UserPermission
from app.views.utilities.utility import VerificationCode, EncodedJWT, DecodeJWT, RegExp, SecretKey
import phonenumbers
import urllib.parse


class Validation(object):
    @staticmethod
    def sign_up(email):
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        email_user = User.query.filter_by(email=email).first()

        payload = {"status": "", "message": {"email": ""}}

        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        elif email_user is not None:
            payload["message"]["email"] = "email_hasznalatban"
        else:
            del payload["message"]["email"]

        if payload.get("message", {}).get("email"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def sign_up_pin(email, pin, code):
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        email_user = User.query.filter_by(email=email).first()

        pin_pattern = RegExp.pin()
        pin_result = re.match(pin_pattern, pin)

        decode_code = DecodeJWT.decode(code)

        payload = {"status": "", "message": {"email": "", "pin": ""}}

        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        elif email_user is not None:
            payload["message"]["email"] = "email_hasznalatban"
        else:
            del payload["message"]["email"]

        if pin_result is None:
            payload["message"]["pin"] = "anlihouse-A17"
        elif email != decode_code['email'] or pin != decode_code['pin']:
            payload["message"]["pin"] = "anlihouse-A17"
        else:
            del payload["message"]["pin"]

        if payload.get("message", {}).get("email") or payload.get("message", {}).get("pin"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def sign_up_data(email, code, username, password, password_confirm, privacy):
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        email_user = User.query.filter_by(email=email).first()

        decode_code = DecodeJWT.decode(code)

        username_result = bool(username and username.strip())

        password_pattern = RegExp.password()
        password_result = re.match(password_pattern, password)

        password_confirm_pattern = RegExp.password()
        password_confirm_result = re.match(password_confirm_pattern, password_confirm)

        payload = {"status": "",
                   "message": {"email": "", "code": "", "username": "", "password": "", "password_confirm": "",
                               "privacy": ""}}

        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        elif email_user is not None:
            payload["message"]["email"] = "email_hasznalatban"
        else:
            del payload["message"]["email"]

        if email != decode_code['email']:
            payload["message"]["code"] = "anlihouse-A17"
        else:
            del payload["message"]["code"]

        if username_result is not True:
            payload["message"]["username"] = "anlihouse-A17"
        else:
            del payload["message"]["username"]

        if password_result is None:
            payload["message"]["password"] = "anlihouse-A17"
        else:
            del payload["message"]["password"]

        if password_confirm_result is None:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        elif password != password_confirm:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        else:
            del payload["message"]["password_confirm"]

        if privacy == "False":
            payload["message"]["privacy"] = "readAndAccept"
        else:
            del payload["message"]["privacy"]

        if payload.get("message", {}).get("email") \
                or payload.get("message", {}).get("code") \
                or payload.get("message", {}).get("username") \
                or payload.get("message", {}).get("password") \
                or payload.get("message", {}).get("password_confirm") \
                or payload.get("message", {}).get("privacy"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def sign_in(email, password):
        user = User.query.filter_by(email=email).first()

        if user is not None:
            user_permission = UserPermission \
                .query.join(User.permission) \
                .filter(User.id == user.id).first()

            inactive_account = user_permission.inactive_account
        else:
            inactive_account = "True"

        email_result = bool(email and email.strip())
        password_result = bool(password and password.strip())

        payload = {"status": "", "message": {"email": "", "password": ""}}

        if email_result is not True:
            payload["message"]["email"] = "anlihouse-A17"
        elif user is None or inactive_account == "True" or user.deleted == "True":
            payload["message"]["email"] = "failed"
        elif user is not None and password_result is True:
            if not user.password_verify(password, user.password):
                payload["message"]["email"] = "failed"
        else:
            del payload["message"]["email"]

        if password_result is not True:
            payload["message"]["password"] = "anlihouse-A17"
        else:
            del payload["message"]["password"]

        if payload.get("message", {}).get("email") or payload.get("message", {}).get("password"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
            payload['email'] = email
            token = EncodedJWT.encoded(payload)
            payload['token'] = token
        return payload

    @staticmethod
    def password_reset(email):
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        email_user = User.query.filter_by(email=email).first()

        payload = {"status": "", "message": {"email": ""}}

        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        elif email_user is None:
            payload["message"]["email"] = "anlihouse-A41"
        else:
            del payload["message"]["email"]

        if payload.get("message", {}).get("email"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def password_reset_pin(email, pin, code):
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        email_user = User.query.filter_by(email=email).first()

        pin_pattern = RegExp.pin()
        pin_result = re.match(pin_pattern, pin)

        decode_code = DecodeJWT.decode(code)

        payload = {"status": "", "message": {"email": "", "pin": ""}}

        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        else:
            del payload["message"]["email"]

        if pin_result is None:
            payload["message"]["pin"] = "anlihouse-A17"
        elif email != decode_code['email'] or pin != decode_code['pin']:
            payload["message"]["pin"] = "anlihouse-A17"
        else:
            del payload["message"]["pin"]

        if payload.get("message", {}).get("email") or payload.get("message", {}).get("pin"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def password_reset_data(email, code, password, password_confirm):
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        email_user = User.query.filter_by(email=email).first()

        decode_code = DecodeJWT.decode(code)

        password_pattern = RegExp.password()
        password_result = re.match(password_pattern, password)

        password_confirm_pattern = RegExp.password()
        password_confirm_result = re.match(password_confirm_pattern, password_confirm)

        payload = {"status": "",
                   "message": {"email": "", "code": "", "password": "", "password_confirm": ""}}

        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        else:
            del payload["message"]["email"]

        if email != decode_code['email']:
            payload["message"]["code"] = "anlihouse-A17"
        else:
            del payload["message"]["code"]

        if password_result is None:
            payload["message"]["password"] = "anlihouse-A17"
        else:
            del payload["message"]["password"]

        if password_confirm_result is None:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        elif password != password_confirm:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        else:
            del payload["message"]["password_confirm"]

        if payload.get("message", {}).get("email") \
                or payload.get("message", {}).get("code") \
                or payload.get("message", {}).get("password") \
                or payload.get("message", {}).get("password_confirm"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def add_settings(settings_name, settings_type, settings_value):
        payload = {"status": "", "message": {"settings_name": "", "settings_type": "", "settings_value": ""}}

        settings_name_result = bool(settings_name and settings_name.strip())
        settings_type_result = bool(settings_type and settings_type.strip())
        settings_value_result = bool(settings_value and settings_value.strip())

        if settings_name_result is not True:
            payload["message"]["settings_name"] = "anlihouse-A17"
        else:
            del payload["message"]["settings_name"]

        if settings_type_result is not True:
            payload["message"]["settings_type"] = "anlihouse-A17"
        else:
            del payload["message"]["settings_type"]

        if settings_value_result is not True:
            payload["message"]["settings_value"] = "anlihouse-A17"
        else:
            del payload["message"]["settings_value"]

        if payload.get("message", {}).get("email") \
                or payload.get("message", {}).get("settings_name") \
                or payload.get("message", {}).get("settings_type") \
                or payload.get("message", {}).get("settings_value"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"

        return payload

    @staticmethod
    def billing_and_shipping_address(
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
    ):
        payload = {"status": "", "message": {
            "email": "",
            "billing_first_name": "",
            "billing_last_name": "",
            "billing_phone": "",
            "billing_email": "",
            "billing_company_name": "",
            "billing_company_tax": "",
            "billing_country": "",
            "billing_zip_number": "",
            "billing_place": "",
            "billing_street": "",
            "shipping_first_name": "",
            "shipping_last_name": "",
            "shipping_phone": "",
            "shipping_email": "",
            "shipping_country": "",
            "shipping_zip_number": "",
            "shipping_place": "",
            "shipping_street": ""
        }}

        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        billing_first_name_result = bool(billing_first_name and billing_first_name.strip())
        billing_last_name_result = bool(billing_last_name and billing_last_name.strip())
        billing_email_result = re.match(email_pattern, billing_email)
        billing_company_name_result = bool(billing_company_name and billing_company_name.strip())
        billing_company_tax_result = bool(billing_company_tax and billing_company_tax.strip())
        billing_country_result = bool(billing_country and billing_country.strip())
        billing_zip_number_result = bool(billing_zip_number and billing_zip_number.strip())
        billing_place_result = bool(billing_place and billing_place.strip())
        billing_street_result = bool(billing_street and billing_street.strip())

        shipping_first_name_result = bool(shipping_first_name and shipping_first_name.strip())
        shipping_last_name_result = bool(shipping_last_name and shipping_last_name.strip())
        shipping_email_result = re.match(email_pattern, shipping_email)
        shipping_country_result = bool(shipping_country and shipping_country.strip())
        shipping_zip_number_result = bool(shipping_zip_number and shipping_zip_number.strip())
        shipping_place_result = bool(shipping_place and shipping_place.strip())
        shipping_street_result = bool(shipping_street and shipping_street.strip())

        #  Start Billing
        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        else:
            del payload["message"]["email"]

        if billing_first_name_result is not True:
            payload["message"]["billing_first_name"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_first_name"]

        if billing_last_name_result is not True:
            payload["message"]["billing_last_name"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_last_name"]

        try:
            billing_phone_result = phonenumbers.parse(billing_phone, None)
            if phonenumbers.is_valid_number(billing_phone_result) is not True:
                payload["message"]["billing_phone"] = "anlihouse-A17"
            else:
                del payload["message"]["billing_phone"]
        except:
            payload["message"]["billing_phone"] = "anlihouse-A17"

        if billing_email_result is None:
            payload["message"]["billing_email"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_email"]

        if billing_is_company == "True" and billing_company_name_result is not True:
            payload["message"]["billing_company_name"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_company_name"]

        if billing_is_company == "True" and billing_company_tax_result is not True:
            payload["message"]["billing_company_tax"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_company_tax"]

        if billing_country_result is not True:
            payload["message"]["billing_country"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_country"]

        if billing_zip_number_result is not True:
            payload["message"]["billing_zip_number"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_zip_number"]

        if billing_place_result is not True:
            payload["message"]["billing_place"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_place"]

        if billing_street_result is not True:
            payload["message"]["billing_street"] = "anlihouse-A17"
        else:
            del payload["message"]["billing_street"]

        #  End Billing
        #  Start Shipping
        if billing_is_shipping_address == "False" and shipping_first_name_result is not True:
            payload["message"]["shipping_first_name"] = "anlihouse-A17"
        else:
            del payload["message"]["shipping_first_name"]

        if billing_is_shipping_address == "False" and shipping_last_name_result is not True:
            payload["message"]["shipping_last_name"] = "anlihouse-A17"
        else:
            del payload["message"]["shipping_last_name"]

        try:
            shipping_phone_result = phonenumbers.parse(shipping_phone, None)
            if billing_is_shipping_address == "False" and phonenumbers.is_valid_number(
                    shipping_phone_result) is not True:
                payload["message"]["shipping_phone"] = "anlihouse-A17"
            else:
                del payload["message"]["shipping_phone"]
        except:
            if billing_is_shipping_address == "False":
                payload["message"]["shipping_phone"] = "anlihouse-A17"
            else:
                del payload["message"]["shipping_phone"]

        if billing_is_shipping_address == "False" and shipping_email_result is None:
            payload["message"]["shipping_email"] = "anlihouse-A17"
        else:
            del payload["message"]["shipping_email"]

        if billing_is_shipping_address == "False" and shipping_country_result is not True:
            payload["message"]["shipping_country"] = "anlihouse-A17"
        else:
            del payload["message"]["shipping_country"]

        if billing_is_shipping_address == "False" and shipping_zip_number_result is not True:
            payload["message"]["shipping_zip_number"] = "anlihouse-A17"
        else:
            del payload["message"]["shipping_zip_number"]

        if billing_is_shipping_address == "False" and shipping_place_result is not True:
            payload["message"]["shipping_place"] = "anlihouse-A17"
        else:
            del payload["message"]["shipping_place"]

        if billing_is_shipping_address == "False" and shipping_street_result is not True:
            payload["message"]["shipping_street"] = "anlihouse-A17"
        else:
            del payload["message"]["shipping_street"]

        #  End Shipping

        if payload.get("message", {}).get("email") \
                or payload.get("message", {}).get("billing_first_name") \
                or payload.get("message", {}).get("billing_last_name") \
                or payload.get("message", {}).get("billing_phone") \
                or payload.get("message", {}).get("billing_email") \
                or payload.get("message", {}).get("billing_company_name") \
                or payload.get("message", {}).get("billing_company_tax") \
                or payload.get("message", {}).get("billing_country") \
                or payload.get("message", {}).get("billing_zip_number") \
                or payload.get("message", {}).get("billing_place") \
                or payload.get("message", {}).get("billing_street") \
                or payload.get("message", {}).get("shipping_last_name") \
                or payload.get("message", {}).get("shipping_phone") \
                or payload.get("message", {}).get("shipping_email") \
                or payload.get("message", {}).get("shipping_country") \
                or payload.get("message", {}).get("shipping_zip_number") \
                or payload.get("message", {}).get("shipping_place") \
                or payload.get("message", {}).get("shipping_street"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"

        return payload

    @staticmethod
    def security_password(email, current_password, password, password_confirm):
        user = User.query.filter_by(email=email).first()

        current_password_result = bool(current_password and current_password.strip())
        password_result = bool(password and password.strip())
        password_confirm_pattern = RegExp.password()
        password_confirm_result = re.match(password_confirm_pattern, password_confirm)

        payload = {"status": "",
                   "message": {"current_password": "", "password": "", "password_confirm": ""}}

        if current_password_result is not True:
            payload["message"]["current_password"] = "anlihouse-A17"
        elif user is not None and not user.password_verify(current_password, user.password):
            payload["message"]["current_password"] = "failed"
        else:
            del payload["message"]["current_password"]

        if password_result is not True:
            payload["message"]["password"] = "anlihouse-A17"
        else:
            del payload["message"]["password"]

        if password_confirm_result is None:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        elif password != password_confirm:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        else:
            del payload["message"]["password_confirm"]

        if payload.get("message", {}).get("current_password") \
                or payload.get("message", {}).get("password") \
                or payload.get("message", {}).get("password_confirm"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def security_email(current_email, email, secret_key):
        user = User.query.filter_by(email=current_email).first()
        check_email = User.query.filter_by(email=email).first()

        current_email_pattern = RegExp.email()
        current_email_result = re.match(current_email_pattern, current_email)
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        secret_key_result = bool(secret_key and secret_key.strip())

        payload = {"status": "", "message": {"user_email": "", "check_email": "", "email": "", "sign-in": ""}}

        if user is not None:

            if current_email == email:
                payload["message"]["user_email"] = "anlihouse-A99"
            else:
                del payload["message"]["user_email"]

            if check_email is not None and current_email != email:
                payload["message"]["check_email"] = "email_hasznalatban"
            else:
                del payload["message"]["check_email"]

            if email_result is None:
                payload["message"]["email"] = "anlihouse-A17"
            else:
                del payload["message"]["email"]

            if payload.get("message", {}).get("user_email") \
                    or payload.get("message", {}).get("check_email") \
                    or payload.get("message", {}).get("email"):
                payload["status"] = "error"
            else:
                payload["status"] = "success"
            return payload

    @staticmethod
    def add_category(name_hu, name_en, name_de, name_fr, name_es):
        payload = {"status": "", "message": {"name_hu": "", "name_en": "", "name_de": "", "name_fr": "", "name_es": ""}}

        name_hu_result = bool(name_hu and name_hu.strip())
        name_en_result = bool(name_en and name_en.strip())
        name_de_result = bool(name_de and name_de.strip())
        name_fr_result = bool(name_fr and name_fr.strip())
        name_es_result = bool(name_es and name_es.strip())

        if name_hu_result is not True:
            payload["message"]["name_hu"] = "anlihouse-A17"
        else:
            del payload["message"]["name_hu"]

        if name_en_result is not True:
            payload["message"]["name_en"] = "anlihouse-A17"
        else:
            del payload["message"]["name_en"]

        if name_de_result is not True:
            payload["message"]["name_de"] = "anlihouse-A17"
        else:
            del payload["message"]["name_de"]

        if name_fr_result is not True:
            payload["message"]["name_fr"] = "anlihouse-A17"
        else:
            del payload["message"]["name_fr"]

        if name_es_result is not True:
            payload["message"]["name_es"] = "anlihouse-A17"
        else:
            del payload["message"]["name_es"]

        if payload.get("message", {}).get("name_hu") \
                or payload.get("message", {}).get("name_en") \
                or payload.get("message", {}).get("name_de") \
                or payload.get("message", {}).get("name_fr") \
                or payload.get("message", {}).get("name_es"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"

        return payload

    @staticmethod
    def add_subcategory(category_id_select, name_hu, name_en, name_de, name_fr, name_es, description_hu, description_en,
                        description_de, description_fr,
                        description_es):
        payload = {"status": "",
                   "message": {"category_id_select": "",
                               "name_hu": "",
                               "name_en": "",
                               "name_de": "",
                               "name_fr": "",
                               "name_es": "",
                               "description_hu": "",
                               "description_en": "",
                               "description_de": "",
                               "description_fr": "",
                               "description_es": "",
                               }}

        category_id_select_result = bool(category_id_select and category_id_select.strip())
        name_hu_result = bool(name_hu and name_hu.strip())
        name_en_result = bool(name_en and name_en.strip())
        name_de_result = bool(name_de and name_de.strip())
        name_fr_result = bool(name_fr and name_fr.strip())
        name_es_result = bool(name_es and name_es.strip())
        description_hu_result = bool(description_hu and description_hu.strip())
        description_en_result = bool(description_en and description_en.strip())
        description_de_result = bool(description_de and description_de.strip())
        description_fr_result = bool(description_fr and description_fr.strip())
        description_es_result = bool(description_es and description_es.strip())

        if category_id_select_result is not True:
            payload["message"]["category_id_select"] = "anlihouse-A17"
        else:
            del payload["message"]["category_id_select"]

        if name_hu_result is not True:
            payload["message"]["name_hu"] = "anlihouse-A17"
        else:
            del payload["message"]["name_hu"]

        if name_en_result is not True:
            payload["message"]["name_en"] = "anlihouse-A17"
        else:
            del payload["message"]["name_en"]

        if name_de_result is not True:
            payload["message"]["name_de"] = "anlihouse-A17"
        else:
            del payload["message"]["name_de"]

        if name_fr_result is not True:
            payload["message"]["name_fr"] = "anlihouse-A17"
        else:
            del payload["message"]["name_fr"]

        if name_es_result is not True:
            payload["message"]["name_es"] = "anlihouse-A17"
        else:
            del payload["message"]["name_es"]

        if description_hu_result is not True:
            payload["message"]["description_hu"] = "anlihouse-A17"
        else:
            del payload["message"]["description_hu"]

        if description_en_result is not True:
            payload["message"]["description_en"] = "anlihouse-A17"
        else:
            del payload["message"]["description_en"]

        if description_de_result is not True:
            payload["message"]["description_de"] = "anlihouse-A17"
        else:
            del payload["message"]["description_de"]

        if description_fr_result is not True:
            payload["message"]["description_fr"] = "anlihouse-A17"
        else:
            del payload["message"]["description_fr"]

        if description_es_result is not True:
            payload["message"]["description_es"] = "anlihouse-A17"
        else:
            del payload["message"]["description_es"]

        if payload.get("message", {}).get("category_id_select") \
                or payload.get("message", {}).get("name_hu") \
                or payload.get("message", {}).get("name_en") \
                or payload.get("message", {}).get("name_de") \
                or payload.get("message", {}).get("name_fr") \
                or payload.get("message", {}).get("name_es") \
                or payload.get("message", {}).get("description_hu") \
                or payload.get("message", {}).get("description_en") \
                or payload.get("message", {}).get("description_de") \
                or payload.get("message", {}).get("description_fr") \
                or payload.get("message", {}).get("description_es"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"

        return payload

    @staticmethod
    def uploading_animal(category_id, subcategory_id, name, chip, height, age_year, age_month, age_day, country_origin,
                         country_residence, is_be_used_for,
                         be_used_for_hu, be_used_for_en, be_used_for_de, be_used_for_fr,
                         be_used_for_es, is_gender, gender_hu,
                         gender_en, gender_de, gender_fr, gender_es, is_color, color_hu,
                         color_en, color_de, color_fr, color_es, brief_description, description, mother,
                         mother_mother, mother_mother_mother, mother_mother_father,
                         mother_father, mother_father_mother, mother_father_father,
                         father, father_mother, father_mother_mother,
                         father_mother_father, father_father, father_father_mother,
                         father_father_father, img_01_data, img_02_data, img_03_data,
                         img_04_data, video_01_data, url_01, url_02, medical_paper_data, breed_registry_data,
                         x_ray_data, price):

        payload = {"status": "", "message": {
            "category_id": "",
            "subcategory_id": "",
            "name": "",
            "chip": "",
            "height": "",
            "age_year": "",
            "age_month": "",
            "age_day": "",
            "country_origin": "",
            "country_residence": "",
            "be_used_for": "",
            "gender": "",
            "color": "",
            "brief_description": "",
            "description": "",
            "mother": "",
            "mother_mother": "",
            "mother_mother_mother": "",
            "mother_mother_father": "",
            "mother_father": "",
            "mother_father_mother": "",
            "mother_father_father": "",
            "father": "",
            "father_mother": "",
            "father_mother_mother": "",
            "father_mother_father": "",
            "father_father": "",
            "father_father_mother": "",
            "father_father_father": "",
            "img_01_data": "",
            "img_02_data": "",
            "img_03_data": "",
            "img_04_data": "",
            "video_01_data": "",
            "url_01": "",
            "url_02": "",
            "medical_paper_data": "",
            "breed_registry_data": "",
            "x_ray_data": "",
            "price": ""
        }}

        category_id_result = bool(category_id and category_id.strip())
        subcategory_id_result = bool(subcategory_id and subcategory_id.strip())
        name_result = bool(name and name.strip())
        chip_result = bool(chip and chip.strip())
        height_pattern = RegExp.numeric()
        height_result = re.match(height_pattern, height)
        age_year_result = bool(age_year and age_year.strip())
        age_month_result = bool(age_month and age_month.strip())
        age_day_result = bool(age_day and age_day.strip())
        country_origin_result = bool(country_origin and country_origin.strip())
        country_residence_result = bool(country_residence and country_residence.strip())
        be_used_for_hu_result = bool(be_used_for_hu and be_used_for_hu.strip())
        be_used_for_en_result = bool(be_used_for_en and be_used_for_en.strip())
        be_used_for_de_result = bool(be_used_for_de and be_used_for_de.strip())
        be_used_for_fr_result = bool(be_used_for_fr and be_used_for_fr.strip())
        be_used_for_es_result = bool(be_used_for_es and be_used_for_es.strip())
        gender_hu_result = bool(gender_hu and gender_hu.strip())
        gender_en_result = bool(gender_en and gender_en.strip())
        gender_de_result = bool(gender_de and gender_de.strip())
        gender_fr_result = bool(gender_fr and gender_fr.strip())
        gender_es_result = bool(gender_es and gender_es.strip())
        color_hu_result = bool(color_hu and color_hu.strip())
        color_en_result = bool(color_en and color_en.strip())
        color_de_result = bool(color_de and color_de.strip())
        color_fr_result = bool(color_fr and color_fr.strip())
        color_es_result = bool(color_es and color_es.strip())
        brief_description_result = bool(brief_description and brief_description.strip())
        description_result = bool(description and description.strip())
        mother_result = bool(mother and mother.strip())
        mother_mother_result = bool(mother_mother and mother_mother.strip())
        mother_mother_mother_result = bool(mother_mother_mother and mother_mother_mother.strip())
        mother_mother_father_result = bool(mother_mother_father and mother_mother_father.strip())
        mother_father_result = bool(mother_father and mother_father.strip())
        mother_father_mother_result = bool(mother_father_mother and mother_father_mother.strip())
        mother_father_father_result = bool(mother_father_father and mother_father_father.strip())
        father_result = bool(father and father.strip())
        father_mother_result = bool(father_mother and father_mother.strip())
        father_mother_mother_result = bool(father_mother_mother and father_mother_mother.strip())
        father_mother_father_result = bool(father_mother_father and father_mother_father.strip())
        father_father_result = bool(father_father and father_father.strip())
        father_father_mother_result = bool(father_father_mother and father_father_mother.strip())
        father_father_father_result = bool(father_father_father and father_father_father.strip())
        img_01_data_result = bool(img_01_data and img_01_data.strip())
        img_02_data_result = bool(img_02_data and img_02_data.strip())
        img_03_data_result = bool(img_03_data and img_03_data.strip())
        img_04_data_result = bool(img_04_data and img_04_data.strip())
        video_01_data_result = bool(video_01_data and video_01_data.strip())
        url_01_result = bool(url_01 and url_01.strip())
        url_02_result = bool(url_02 and url_02.strip())
        medical_paper_data_result = bool(medical_paper_data and medical_paper_data.strip())
        breed_registry_data_result = bool(breed_registry_data and breed_registry_data.strip())
        x_ray_data_result = bool(x_ray_data and x_ray_data.strip())
        price_pattern = RegExp.numeric()
        price_result = re.match(price_pattern, price)

        if category_id_result is not True:
            payload["message"]["category_id"] = "anlihouse-A17"
        else:
            del payload["message"]["category_id"]

        if subcategory_id_result is not True:
            payload["message"]["subcategory_id"] = "anlihouse-A17"
        else:
            del payload["message"]["subcategory_id"]

        if name_result is not True:
            payload["message"]["name"] = "anlihouse-A17"
        else:
            del payload["message"]["name"]

        if chip_result is not True:
            payload["message"]["chip"] = "anlihouse-A17"
        else:
            del payload["message"]["chip"]

        if height_result is None:
            payload["message"]["height"] = "anlihouse-A17"
        else:
            del payload["message"]["height"]

        if age_year_result is not True:
            payload["message"]["age_year"] = "anlihouse-A17"
        else:
            del payload["message"]["age_year"]

        if age_month_result is not True:
            payload["message"]["age_month"] = "anlihouse-A17"
        else:
            del payload["message"]["age_month"]

        if age_day_result is not True:
            payload["message"]["age_day"] = "anlihouse-A17"
        else:
            del payload["message"]["age_day"]

        if country_origin_result is not True:
            payload["message"]["country_origin"] = "anlihouse-A17"
        else:
            del payload["message"]["country_origin"]

        if country_residence_result is not True:
            payload["message"]["country_residence"] = "anlihouse-A17"
        else:
            del payload["message"]["country_residence"]

        if is_be_used_for != "False":
            if be_used_for_hu_result is not True \
                    and be_used_for_en_result is not True \
                    and be_used_for_de_result is not True \
                    and be_used_for_fr_result is not True \
                    and be_used_for_es_result is not True:
                payload["message"]["be_used_for"] = "anlihouse-A17"
            else:
                del payload["message"]["be_used_for"]
        else:
            del payload["message"]["be_used_for"]

        if is_gender != "False":
            if gender_hu_result is not True \
                    and gender_en_result is not True \
                    and gender_de_result is not True \
                    and gender_fr_result is not True \
                    and gender_es_result is not True:
                payload["message"]["gender"] = "anlihouse-A17"
            else:
                del payload["message"]["gender"]
        else:
            del payload["message"]["gender"]

        if is_color != "False":
            if color_hu_result is not True \
                    and color_en_result is not True \
                    and color_de_result is not True \
                    and color_fr_result is not True \
                    and color_es_result is not True:
                payload["message"]["color"] = "anlihouse-A17"
            else:
                del payload["message"]["color"]
        else:
            del payload["message"]["color"]

        if brief_description_result is not True:
            payload["message"]["brief_description"] = "anlihouse-A17"
        else:
            del payload["message"]["brief_description"]

        if description_result is not True:
            payload["message"]["description"] = "anlihouse-A17"
        else:
            del payload["message"]["description"]

        if mother_result is not True:
            payload["message"]["mother"] = "anlihouse-A17"
        else:
            del payload["message"]["mother"]

        if mother_mother_result is not True:
            payload["message"]["mother_mother"] = "anlihouse-A17"
        else:
            del payload["message"]["mother_mother"]

        if mother_mother_mother_result is not True:
            payload["message"]["mother_mother_mother"] = "anlihouse-A17"
        else:
            del payload["message"]["mother_mother_mother"]

        if mother_mother_father_result is not True:
            payload["message"]["mother_mother_father"] = "anlihouse-A17"
        else:
            del payload["message"]["mother_mother_father"]

        if mother_father_result is not True:
            payload["message"]["mother_father"] = "anlihouse-A17"
        else:
            del payload["message"]["mother_father"]

        if mother_father_mother_result is not True:
            payload["message"]["mother_father_mother"] = "anlihouse-A17"
        else:
            del payload["message"]["mother_father_mother"]

        if mother_father_father_result is not True:
            payload["message"]["mother_father_father"] = "anlihouse-A17"
        else:
            del payload["message"]["mother_father_father"]

        if father_result is not True:
            payload["message"]["father"] = "anlihouse-A17"
        else:
            del payload["message"]["father"]

        if father_mother_result is not True:
            payload["message"]["father_mother"] = "anlihouse-A17"
        else:
            del payload["message"]["father_mother"]

        if father_mother_mother_result is not True:
            payload["message"]["father_mother_mother"] = "anlihouse-A17"
        else:
            del payload["message"]["father_mother_mother"]

        if father_mother_father_result is not True:
            payload["message"]["father_mother_father"] = "anlihouse-A17"
        else:
            del payload["message"]["father_mother_father"]

        if father_father_result is not True:
            payload["message"]["father_father"] = "anlihouse-A17"
        else:
            del payload["message"]["father_father"]

        if father_father_mother_result is not True:
            payload["message"]["father_father_mother"] = "anlihouse-A17"
        else:
            del payload["message"]["father_father_mother"]

        if father_father_father_result is not True:
            payload["message"]["father_father_father"] = "anlihouse-A17"
        else:
            del payload["message"]["father_father_father"]

        if img_01_data_result is not True:
            payload["message"]["img_01_data"] = "anlihouse-A17"
        else:
            del payload["message"]["img_01_data"]

        if img_02_data_result is not True:
            payload["message"]["img_02_data"] = "anlihouse-A17"
        else:
            del payload["message"]["img_02_data"]

        if img_03_data_result is not True:
            payload["message"]["img_03_data"] = "anlihouse-A17"
        else:
            del payload["message"]["img_03_data"]

        if img_04_data_result is not True:
            payload["message"]["img_04_data"] = "anlihouse-A17"
        else:
            del payload["message"]["img_04_data"]

        if video_01_data_result is not True:
            del payload["message"]["video_01_data"]
            # payload["message"]["video_01_data"] = "anlihouse-A17"
        else:
            del payload["message"]["video_01_data"]

        if url_01_result is True:
            domain = urllib.parse.urlsplit(url_01)
            if domain.netloc == "www.horsetelex.com" or domain.netloc == "horsetelex.com":
                del payload["message"]["url_01"]
            else:
                payload["message"]["url_01"] = "anlihouse-A17"
        else:
            del payload["message"]["url_01"]

        if url_02_result is True:
            domain = urllib.parse.urlsplit(url_02)
            if domain.netloc == "www.hippomundo.com" or domain.netloc == "hippomundo.com":
                del payload["message"]["url_02"]
            else:
                payload["message"]["url_02"] = "anlihouse-A17"
        else:
            del payload["message"]["url_02"]

        if medical_paper_data_result is not True:
            payload["message"]["medical_paper_data"] = "anlihouse-A17"
        else:
            del payload["message"]["medical_paper_data"]

        if breed_registry_data_result is not True:
            payload["message"]["breed_registry_data"] = "anlihouse-A17"
        else:
            del payload["message"]["breed_registry_data"]

        if x_ray_data_result is not True:
            payload["message"]["x_ray_data"] = "anlihouse-A17"
        else:
            del payload["message"]["x_ray_data"]

        if price_result is None:
            payload["message"]["price"] = "anlihouse-A17"
        else:
            del payload["message"]["price"]

        if payload.get("message", {}).get("category_id") \
                or payload.get("message", {}).get("subcategory_id") \
                or payload.get("message", {}).get("name") \
                or payload.get("message", {}).get("chip") \
                or payload.get("message", {}).get("height") \
                or payload.get("message", {}).get("age_year") \
                or payload.get("message", {}).get("age_month") \
                or payload.get("message", {}).get("age_day") \
                or payload.get("message", {}).get("country_origin") \
                or payload.get("message", {}).get("country_residence") \
                or payload.get("message", {}).get("be_used_for") \
                or payload.get("message", {}).get("gender") \
                or payload.get("message", {}).get("color") \
                or payload.get("message", {}).get("description") \
                or payload.get("message", {}).get("mother") \
                or payload.get("message", {}).get("mother_mother") \
                or payload.get("message", {}).get("mother_mother_mother") \
                or payload.get("message", {}).get("mother_mother_father") \
                or payload.get("message", {}).get("mother_father") \
                or payload.get("message", {}).get("mother_father_mother") \
                or payload.get("message", {}).get("mother_father_father") \
                or payload.get("message", {}).get("father") \
                or payload.get("message", {}).get("father_mother") \
                or payload.get("message", {}).get("father_mother_mother") \
                or payload.get("message", {}).get("father_mother_father") \
                or payload.get("message", {}).get("father_father") \
                or payload.get("message", {}).get("father_father_mother") \
                or payload.get("message", {}).get("father_father_father") \
                or payload.get("message", {}).get("img_01_data") \
                or payload.get("message", {}).get("img_02_data") \
                or payload.get("message", {}).get("img_03_data") \
                or payload.get("message", {}).get("img_04_data") \
                or payload.get("message", {}).get("video_01_data") \
                or payload.get("message", {}).get("url_01") \
                or payload.get("message", {}).get("url_02") \
                or payload.get("message", {}).get("medical_paper_data") \
                or payload.get("message", {}).get("breed_registry_data") \
                or payload.get("message", {}).get("x_ray_data") \
                or payload.get("message", {}).get("price"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def add_user(email, name, password, password_confirm):
        email_pattern = RegExp.email()
        email_result = re.match(email_pattern, email)
        email_user = User.query.filter_by(email=email).first()

        name_result = bool(name and name.strip())

        password_pattern = RegExp.password()
        password_result = re.match(password_pattern, password)

        password_confirm_pattern = RegExp.password()
        password_confirm_result = re.match(password_confirm_pattern, password_confirm)

        payload = {"status": "", "message": {"email": "", "name": "", "password": "", "password_confirm": ""}}

        if email_result is None:
            payload["message"]["email"] = "anlihouse-A17"
        elif email_user is not None:
            payload["message"]["email"] = "email_hasznalatban"
        else:
            del payload["message"]["email"]

        if name_result is not True:
            payload["message"]["name"] = "anlihouse-A17"
        else:
            del payload["message"]["name"]

        if password_result is None:
            payload["message"]["password"] = "anlihouse-A17"
        else:
            del payload["message"]["password"]

        if password_confirm_result is None:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        elif password != password_confirm:
            payload["message"]["password_confirm"] = "anlihouse-A28"
        else:
            del payload["message"]["password_confirm"]

        if payload.get("message", {}).get("email") \
                or payload.get("message", {}).get("name") \
                or payload.get("message", {}).get("password") \
                or payload.get("message", {}).get("password_confirm"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def question(question):
        question_result = bool(question and question.strip())

        payload = {"status": "", "message": {"question": ""}}

        if question_result is not True:
            payload["message"]["question"] = "anlihouse-A17"
        elif len(question) < 64:
            payload["message"]["question"] = "anlihouse-A328"
        elif len(question) > 256:
            payload["message"]["question"] = "anlihouse-A329"
        else:
            del payload["message"]["question"]

        if payload.get("message", {}).get("question"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def answer(answer):
        answer_result = bool(answer and answer.strip())

        payload = {"status": "", "message": {"answer": ""}}

        if answer_result is not True:
            payload["message"]["answer"] = "anlihouse-A17"
        elif len(answer) < 64:
            payload["message"]["answer"] = "anlihouse-A334"
        elif len(answer) > 512:
            payload["message"]["answer"] = "anlihouse-A335"
        else:
            del payload["message"]["answer"]

        if payload.get("message", {}).get("answer"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def question_deleted(question):
        payload = {"status": "success"}
        return payload

    @staticmethod
    def question_edit(question):
        question_result = bool(question and question.strip())

        payload = {"status": "", "message": {"question": ""}}

        if question_result is not True:
            payload["message"]["question"] = "anlihouse-A17"
        elif len(question) < 64:
            payload["message"]["question"] = "anlihouse-A328"
        elif len(question) > 256:
            payload["message"]["question"] = "anlihouse-A329"
        else:
            del payload["message"]["question"]

        if payload.get("message", {}).get("question"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def answer_deleted(question):
        payload = {"status": "success"}
        return payload

    @staticmethod
    def answer_edit(answer):
        answer_result = bool(answer and answer.strip())

        payload = {"status": "", "message": {"answer": ""}}

        if answer_result is not True:
            payload["message"]["answer"] = "anlihouse-A17"
        elif len(answer) < 64:
            payload["message"]["answer"] = "anlihouse-A334"
        elif len(answer) > 512:
            payload["message"]["answer"] = "anlihouse-A335"
        else:
            del payload["message"]["answer"]

        if payload.get("message", {}).get("answer"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def talking(talking):
        talking_result = bool(talking and talking.strip())

        payload = {"status": "", "message": {"talking": ""}}

        if talking_result is not True:
            payload["message"]["talking"] = "anlihouse-A17"
        elif len(talking) < 64:
            payload["message"]["talking"] = "anlihouse-A355"
        elif len(talking) > 2048:
            payload["message"]["talking"] = "anlihouse-A356"
        else:
            del payload["message"]["talking"]

        if payload.get("message", {}).get("talking"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def talking_deleted(experience):
        payload = {"status": "success"}
        return payload

    @staticmethod
    def talking_edit(talking):
        talking_result = bool(talking and talking.strip())

        payload = {"status": "", "message": {"talking": ""}}

        if talking_result is not True:
            payload["message"]["talking"] = "anlihouse-A17"
        elif len(talking) < 64:
            payload["message"]["talking"] = "anlihouse-A355"
        elif len(talking) > 2048:
            payload["message"]["talking"] = "anlihouse-A356"
        else:
            del payload["message"]["talking"]

        if payload.get("message", {}).get("talking"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def talking_history(talking_id):
        payload = {"status": "success"}
        return payload

    @staticmethod
    def talking_answer(answer):
        answer_result = bool(answer and answer.strip())

        payload = {"status": "", "message": {"answer": ""}}

        if answer_result is not True:
            payload["message"]["answer"] = "anlihouse-A17"
        elif len(answer) < 64:
            payload["message"]["answer"] = "anlihouse-A334"
        elif len(answer) > 1024:
            payload["message"]["answer"] = "anlihouse-A360"
        else:
            del payload["message"]["answer"]

        if payload.get("message", {}).get("answer"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def talking_answer_deleted(experience):
        payload = {"status": "success"}
        return payload

    @staticmethod
    def talking_answer_edit(answer):
        answer_result = bool(answer and answer.strip())

        payload = {"status": "", "message": {"answer": ""}}

        if answer_result is not True:
            payload["message"]["answer"] = "anlihouse-A17"
        elif len(answer) < 64:
            payload["message"]["answer"] = "anlihouse-A334"
        elif len(answer) > 2048:
            payload["message"]["answer"] = "anlihouse-A360"
        else:
            del payload["message"]["answer"]

        if payload.get("message", {}).get("answer"):
            payload["status"] = "error"
        else:
            payload["status"] = "success"
        return payload

    @staticmethod
    def talking_answer_history(talking_answer_id):
        payload = {"status": "success"}
        return payload

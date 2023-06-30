# -*- coding: utf-8 -*-
import json
import re
from app import app
from flask import session
from random import choice
from string import digits
import jwt
import secrets
import requests
import io
from pyjsonq import JsonQ
from config import _model
from datetime import datetime, time, timezone


class VerificationCode(object):
    @staticmethod
    def generate_pin(pin=None):
        if pin is None:
            pin = 8
        pin_code = list()
        for i in range(pin):
            pin_code.append(choice(digits))
        return "".join(pin_code)

    @staticmethod
    def generate_timestamp_pin():
        timestamp = int(datetime.now(timezone.utc).timestamp())
        return timestamp


class EncodedJWT(object):
    @staticmethod
    def encoded(data):
        encoded = jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')
        return encoded


class DecodeJWT(object):
    @staticmethod
    def decode(data):
        decode = jwt.decode(data, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decode


class SecretKey(object):
    @staticmethod
    def secret_key(number):
        return secrets.token_hex(number)


class RegExp(object):
    @staticmethod
    def email():
        return re.compile(r"[a-zA-Z0-9]+([-._][a-zA-Z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}")

    @staticmethod
    def password():
        return re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[?!%-/._#&*$^@]).{8,}$")

    @staticmethod
    def pin():
        return re.compile(r"[0-9]{6}$")

    @staticmethod
    def numeric():
        return re.compile(r"[1-9][0-9]*$")


class VatLayer(object):
    @staticmethod
    def is_ue_country(country):
        url = app.config['VATLAYER_API_URL'] + "/rate_list?access_key=" + app.config['VATLAYER_API_KEY']
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()

            if 'GB' in data['rates']:
                del data['rates']['GB']

            if country in data['rates']:
                if country != "HU":
                    return True
                else:
                    return False
            else:
                return False

    @staticmethod
    def get_standard_vat(country_code):
        url = app.config['VATLAYER_API_URL'] + "/rate?access_key=" + app.config[
            'VATLAYER_API_KEY'] + "&country_code=" + country_code
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return data['standard_rate']

    @staticmethod
    def get_vat(is_company, tax, country):
        url = app.config['VATLAYER_API_URL'] + "/validate?access_key=" + app.config[
            'VATLAYER_API_KEY'] + "&vat_number=" + tax
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()

            if "valid" in data and data['valid'] is True:  # Valid EU Tax
                if data['country_code'] != "HU":
                    return [VatLayer.get_standard_vat(country), 0]
                if data['country_code'] == "HU":
                    return [VatLayer.get_standard_vat("HU"), VatLayer.get_standard_vat("HU")]
            else:  # Not Valid EU Tax
                if is_company == "True":  # Company
                    if VatLayer.is_ue_country(country):  # Company EU Country Vat
                        return [VatLayer.get_standard_vat(country), VatLayer.get_standard_vat(country)]
                    else:  # Not Company EU Country Vat
                        if country == "HU":
                            return [VatLayer.get_standard_vat(country), VatLayer.get_standard_vat(country)]
                        else:
                            return [VatLayer.get_standard_vat(country), 0]
                else:  # Person
                    if VatLayer.is_ue_country(country):  # Person EU Country Vat
                        return [VatLayer.get_standard_vat(country), VatLayer.get_standard_vat(country)]
                    else:  # Person Not EU Country Vat
                        if country == "HU":
                            return [VatLayer.get_standard_vat(country), VatLayer.get_standard_vat(country)]
                        else:
                            return [VatLayer.get_standard_vat(country), 0]


class Pagination(object):
    @staticmethod
    def create(pagination_count, page_number):
        assert (0 < pagination_count)
        assert (0 < page_number <= pagination_count)

        if pagination_count <= 10:
            pages = set(range(1, pagination_count + 1))
        else:
            pages = (set(range(1, 4))
                     | set(range(max(1, page_number - 2), min(page_number + 3, pagination_count + 1)))
                     | set(range(pagination_count - 2, pagination_count + 1)))

        def display():
            last_page = 0
            for p in sorted(pages):
                if p != last_page + 1: yield '...'
                yield ('{0}' if p == page_number else '{0}').format(p)
                last_page = p

        li = list(' '.join(display()).split(" "))
        return li


class PayPal(object):
    @staticmethod
    def generate_token():
        if session.get('paypal_token') is None:
            session['paypal_token'] = "foo"

        url = app.config['PAYPAL_API_URL'] + "/v2/checkout/orders"  # Test Token
        headers = {
            'Authorization': 'Bearer ' + session['paypal_token'],
            'Content-Type': 'application/json'
        }
        payload = {}
        r = requests.post(url, headers=headers, data=payload, verify=app.config['TLS_VERIFY'])

        if r.status_code == 200:
            return session['paypal_token']
        else:
            url = app.config['PAYPAL_API_URL'] + "/v1/oauth2/token"
            headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en_US',
            }
            payload = "grant_type=client_credentials"
            r = requests.post(
                url,
                headers=headers,
                data=payload,
                auth=(app.config['PAYPAL_CLIENT_ID'], app.config['PAYPAL_SECRET']),
                verify=app.config['TLS_VERIFY'])

            if r.status_code == 200:
                data = r.json()
                session['paypal_token'] = data['access_token']
                return session['paypal_token']


class StringToList(object):
    @staticmethod
    def list(data):
        data_list = []
        data = data.split(",")
        for i in data:
            data_list.append(i.lstrip().capitalize())
        return str(data_list)

    @staticmethod
    def string(data):
        res = data.strip('][').split(', ')
        data_string = ', '.join([str(elem) for elem in res])
        return data_string.replace("'", "")


class CountryCodeToLangCode(object):
    @staticmethod
    def c_to_l(data):
        try:
            data = data.upper()
            countries_json = io.open(_model + "/json/countries.en.json", 'r', encoding='utf8')
            countries_read = json.loads(countries_json.read())
            countries = countries_read

            jq = JsonQ(data=countries)
            countries = jq.at("data").where("country_code", "=", data).get()

            lang_code = countries[0]['lang']
        except AttributeError:
            lang_code = "en"
        except IndexError:
            lang_code = "en"

        return lang_code


class BoolStr(object):
    @staticmethod
    def bool(data):
        return {"True": True, "true": True}.get(data, False)


class Difference(object):
    @staticmethod
    def diff_from(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        item = {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }
        return item

    @staticmethod
    def diff_to(dt2, dt1):
        return round((dt2 - dt1).total_seconds())

# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from .utilities.validators import Validation
from .utilities.utility import VerificationCode, EncodedJWT, DecodeJWT
from app.models.models import User

mod = Blueprint('password_reset_module', __name__)
api = Api(mod)

password_reset = reqparse.RequestParser()
password_reset.add_argument('email', required=True)

password_reset_pin = reqparse.RequestParser()
password_reset_pin.add_argument('code', required=True)
password_reset_pin.add_argument('email', required=True)
password_reset_pin.add_argument('pin', required=True)

password_reset_data = reqparse.RequestParser()
password_reset_data.add_argument('code', required=True)
password_reset_data.add_argument('email', required=True)
password_reset_data.add_argument('password', required=True)
password_reset_data.add_argument('password_confirm', required=True)


class PasswordReset(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = password_reset.parse_args()

        email = data['email']
        pin = VerificationCode.generate_pin(6)

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.password_reset(email)
                if validation['status'] == "success":
                    payload = {
                        "email": email,
                        "pin": pin
                    }
                    data = {"status": 'success', "email": email, "pin": pin, "code": EncodedJWT.encoded(payload)}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class SignUpPin(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = password_reset_pin.parse_args()

        code = data['code']
        email = data['email']
        pin = data['pin']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.password_reset_pin(email, pin, code)
                if validation['status'] == "success":
                    data = {"status": 'success', "email": email, "code": code}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class PasswordResetData(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = password_reset_data.parse_args()

        code = data['code']
        email = data['email']
        password = data['password']
        password_confirm = data['password_confirm']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.password_reset_data(email, code, password, password_confirm)
                if validation['status'] == "success":

                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        user.password_hash(data['password'])
                        user.db_put()
                        data = {"status": 'success', "email": email, "code": code}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(PasswordReset, '/password-reset')
api.add_resource(SignUpPin, '/password-reset-pin')
api.add_resource(PasswordResetData, '/password-reset-data')

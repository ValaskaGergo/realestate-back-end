# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify, json
from flask_restful import Api, Resource, reqparse
from .utilities.validators import Validation
from .utilities.utility import VerificationCode, EncodedJWT, DecodeJWT, SecretKey
from app.models.models import User, UserSecondaryEmail, UserSessionHistoryLogin
from datetime import datetime, timedelta
from dateutil.parser import parse

mod = Blueprint('security_module', __name__)
api = Api(mod)

security_password = reqparse.RequestParser()
security_password.add_argument('email', required=True)
security_password.add_argument('current_password', required=True)
security_password.add_argument('password', required=True)
security_password.add_argument('password_confirm', required=True)

security_email = reqparse.RequestParser()
security_email.add_argument('current_email', required=True)
security_email.add_argument('email', required=True)
security_email.add_argument('secret_key')

get_security_login_history = reqparse.RequestParser()
get_security_login_history.add_argument('email', required=True)

security_delete_user = reqparse.RequestParser()
security_delete_user.add_argument('email', required=True)
security_delete_user.add_argument('password', required=True)


class SecurityPassword(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = security_password.parse_args()

        email = data['email']
        current_password = data['current_password']
        password = data['password']
        password_confirm = data['password_confirm']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.security_password(email, current_password, password, password_confirm)
                if validation['status'] == "success":

                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        user.password_hash(password)
                        user.db_put()
                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class SecurityEmail(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = security_email.parse_args()

        current_email = data['current_email']
        email = data['email']
        secret_key = data['secret_key']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.security_email(current_email, email, secret_key)
                if validation['status'] == "success":
                    user = User.query.filter_by(email=current_email).first()
                    user_secondary_email = UserSecondaryEmail \
                        .query.join(User.secondary_email) \
                        .filter(User.id == user.id).first()

                    if secret_key == "":
                        now = datetime.now()
                        updated_at24 = user_secondary_email.updated_at + timedelta(minutes=60)
                        difference = updated_at24 - now
                        count = user_secondary_email.count
                        send_mail = False

                        if count == 3:
                            if now > updated_at24:
                                user_secondary_email.count = 0
                                send_mail = True
                        elif count < 3:
                            send_mail = True

                        if send_mail is True:
                            user_secondary_email.email = email
                            user_secondary_email.secret_key = SecretKey.secret_key(16)
                            user_secondary_email.count += 1
                            user_secondary_email.db_put()
                            payload = {
                                "secondary_email": user_secondary_email.email,
                                "secret_key": user_secondary_email.secret_key
                            }
                            data = {"status": "success", "payload": payload}
                            return make_response(jsonify(data), 200)
                        else:
                            data = {"status": "error", "seconds": difference.seconds}
                            return make_response(jsonify(data), 401)
                    elif secret_key != "":
                        if email == user_secondary_email.email and secret_key == user_secondary_email.secret_key:
                            user_secondary_email.email = None
                            user_secondary_email.secret_key = None
                            user_secondary_email.count = 0
                            user_secondary_email.db_put()
                            user.email = email
                            now = datetime.now()
                            user.email_control = now
                            user.db_put()
                            payload = {"sign-in": "True"}
                            data = {"status": "success", "payload": payload}
                            return make_response(jsonify(data), 200)
                        else:
                            payload = {"status": "error", "message": {"secret_key": "anlihouse-A96"}}
                            return make_response(jsonify(payload), 400)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetSecurityLoginHistory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_security_login_history.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()
                if user is not None:
                    user_login_history = UserSessionHistoryLogin \
                        .query.join(User.session_history_login) \
                        .filter(User.id == user.id).order_by(UserSessionHistoryLogin.updated_at.desc()).all()
                    session_history_login = []
                    current_count = 0
                    for items in user_login_history:
                        if current_count == 0:
                            current = True
                        else:
                            current = False
                        current_count += 1
                        item = {
                            "current": current,
                            "country_name": items.country_name,
                            "country_code": items.country_code,
                            "ip": items.ip,
                            "browser_name": items.browser_name,
                            "browser_version": items.browser_version,
                            "os_name": items.os_name,
                            "platform_type": items.platform_type,
                            "updated_at": items.updated_at
                        }
                        session_history_login.append(item)
                    data = {
                        "data": sorted(session_history_login, key=lambda x: parse(str(x['updated_at'])), reverse=True)}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class SecurityDeleteUser(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = security_delete_user.parse_args()

        email = data['email']
        password = data['password']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.sign_in(email, password)
                if validation['status'] == "success":

                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        user.deleted = "True"
                        user.email = user.email[::-1]
                        user.db_post()
                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(SecurityPassword, '/security-password')
api.add_resource(SecurityEmail, '/security-email')
api.add_resource(GetSecurityLoginHistory, '/get-security-login-history')
api.add_resource(SecurityDeleteUser, '/security-delete-user')

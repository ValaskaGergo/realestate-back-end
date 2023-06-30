# -*- coding: utf-8 -*-
from app import app, db
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
from .utilities.validators import Validation
import requests
from app.models.models import User, UserSessionHistoryLogin

mod = Blueprint('signin_module', __name__)
api = Api(mod)

sign_in = reqparse.RequestParser()
sign_in.add_argument('email', required=True)
sign_in.add_argument('password', required=True)
sign_in.add_argument('browser_name', required=False)
sign_in.add_argument('browser_version', required=False)
sign_in.add_argument('os_name', required=False)
sign_in.add_argument('platform_type', required=False)


class SignIn(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = sign_in.parse_args()

        email = data['email']
        password = data['password']
        browser_name = data['browser_name']
        browser_version = data['browser_version']
        os_name = data['os_name']
        platform_type = data['platform_type']

        expire_date = datetime.now()
        expire_date = expire_date + timedelta(minutes=15)

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.sign_in(email, password)

                if validation['status'] == "success":

                    if app.config['ENV'] == 'production':
                        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                            ip = request.environ['REMOTE_ADDR']
                        else:
                            ip = request.environ['HTTP_X_FORWARDED_FOR']
                    else:
                        ip = "78.92.123.32"
                        """
                        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                            ip = request.environ['REMOTE_ADDR']
                        else:
                            ip = request.environ['HTTP_X_FORWARDED_FOR']
                        """

                    url = app.config['VATLAYER_API_URL'] + "/rate?access_key=" + app.config[
                        'VATLAYER_API_KEY'] + "&ip_address=" + ip
                    headers = {"Content-Type": "application/json"}
                    r = requests.get(url, headers=headers, verify=app.config['TLS_VERIFY'])

                    if r.status_code == 200:
                        data = r.json()
                        user = User.query.filter_by(email=email).first()

                        if user is not None and data['success'] is True:
                            user_session_history_login = UserSessionHistoryLogin.query \
                                .join(User.session_history_login) \
                                .filter(User.id == user.id) \
                                .order_by(UserSessionHistoryLogin.updated_at).first()

                            user_session_history_login_count = UserSessionHistoryLogin.query \
                                .join(User.session_history_login) \
                                .filter(User.id == user.id).count()

                            if user_session_history_login_count < 25:
                                session_history_login_payload = UserSessionHistoryLogin(
                                    country_code=data['country_code'],
                                    country_name=data['country_name'],
                                    ip=ip,
                                    browser_name=browser_name,
                                    browser_version=browser_version,
                                    os_name=os_name,
                                    platform_type=platform_type
                                )
                                user.session_history_login.append(session_history_login_payload)
                                session_history_login_payload.db_post()
                            elif user_session_history_login_count >= 25:
                                user_session_history_login.country_code = data['country_code']
                                user_session_history_login.country_name = data['country_name']
                                user_session_history_login.ip = ip
                                user_session_history_login.browser_name = browser_name
                                user_session_history_login.browser_version = browser_version
                                user_session_history_login.os_name = os_name
                                user_session_history_login.platform_type = platform_type
                                user_session_history_login.updated_at = db.func.now()
                                user_session_history_login.db_post()

                    return make_response(jsonify(validation), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(SignIn, '/sign-in')

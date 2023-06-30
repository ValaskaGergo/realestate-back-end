# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from .utilities.validators import Validation
from .utilities.utility import VerificationCode, EncodedJWT, DecodeJWT
from app.models.models import User, UserProfile, UserPermission, UserBillingInformation, UserShippingInformation, \
    UserSecondaryEmail, Online, NotificationSettings, Messages
from pyjsonq import JsonQ

mod = Blueprint('signup_module', __name__)
api = Api(mod)

sign_up = reqparse.RequestParser()
sign_up.add_argument('email', required=True)

sign_up_pin = reqparse.RequestParser()
sign_up_pin.add_argument('code', required=True)
sign_up_pin.add_argument('email', required=True)
sign_up_pin.add_argument('pin', required=True)

sign_up_data = reqparse.RequestParser()
sign_up_data.add_argument('code', required=True)
sign_up_data.add_argument('email', required=True)
sign_up_data.add_argument('username', required=True)
sign_up_data.add_argument('password', required=True)
sign_up_data.add_argument('password_confirm', required=True)
sign_up_data.add_argument('privacy', required=True)


class SignUp(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = sign_up.parse_args()

        email = data['email']
        pin = VerificationCode.generate_pin(6)

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.sign_up(email)
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
        data = sign_up_pin.parse_args()

        code = data['code']
        email = data['email']
        pin = data['pin']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.sign_up_pin(email, pin, code)
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


class SignUpData(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = sign_up_data.parse_args()

        code = data['code']
        email = data['email']
        username = data['username']
        password = data['password']
        password_confirm = data['password_confirm']
        privacy = data['privacy']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.sign_up_data(email, code, username, password, password_confirm, privacy)
                if validation['status'] == "success":

                    user_payload = User(
                        email=email
                    )
                    user_payload.password_hash(password)
                    user_payload.privacy = privacy
                    user_payload.db_post()

                    user_profile_payload = UserProfile(
                        username=username + str(user_payload.id)
                    )
                    user_profile_payload.user_profile_backref.append(user_payload)
                    user_profile_payload.db_post()

                    user_permission_payload = UserPermission()
                    user_permission_payload.user_permission_backref.append(user_payload)
                    user_permission_payload.last_modification_user_id = user_payload.id
                    user_permission_payload.last_modification_user_name = user_profile_payload.username
                    user_permission_payload.db_post()

                    user_billing_information_payload = UserBillingInformation()
                    user_billing_information_payload.user_billing_information_backref.append(user_payload)
                    user_billing_information_payload.db_post()

                    user_shipping_information_payload = UserShippingInformation()
                    user_shipping_information_payload.user_shipping_information_backref.append(user_payload)
                    user_shipping_information_payload.db_post()

                    user_secondary_email_payload = UserSecondaryEmail()
                    user_secondary_email_payload.user_secondary_email_backref.append(user_payload)
                    user_secondary_email_payload.db_post()

                    online_payload = Online()
                    online_payload.online_backref.append(user_payload)
                    online_payload.db_post()

                    is_notification_workers = User.query.join(User.permission).filter(
                        UserPermission.is_notifications == "True").all()

                    worker_list = []

                    if len(is_notification_workers) >= 1:
                        for worker in is_notification_workers:
                            if len(is_notification_workers) == 1 or worker.id != 1:
                                costumer_count = User.query.join(User.notification_settings).filter(
                                    NotificationSettings.assistant == worker.id).count()
                                item = {
                                    "worker_id": worker.id,
                                    "costumer_count": int(costumer_count)
                                }
                                worker_list.append(item)

                        jq = JsonQ(data={"data": worker_list})
                        worker = jq.at('data').sort_by('costumer_count').first()

                        notification_settings_payload = NotificationSettings(
                            assistant=worker['worker_id']
                        )
                        notification_settings_payload.notification_settings_backref.append(user_payload)
                        notification_settings_payload.db_post()

                        # Start Send First Login Messages
                        sender_name = UserBillingInformation \
                            .query.join(User.billing_information) \
                            .filter(User.id == worker['worker_id']).first()

                        sender_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user_payload.id).first()

                        host_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user_payload.id).first()

                        if sender_name.first_name is not None and sender_name.last_name is not None:
                            sender_first_name = sender_name.first_name
                            sender_last_name = sender_name.last_name
                        else:
                            sender_first_name = sender_profile.username
                            sender_last_name = sender_profile.username

                        host_name = UserBillingInformation \
                            .query.join(User.billing_information) \
                            .filter(User.id == user_payload.id).first()

                        if host_name.first_name is not None and host_name.last_name is not None:
                            host_first_name = host_name.first_name
                            host_last_name = host_name.last_name
                        else:
                            host_first_name = host_profile.username
                            host_last_name = host_profile.username

                        room = VerificationCode.generate_pin(24)

                        worker_user = User.query.filter_by(id=worker['worker_id']).first()

                        # Start 1
                        message_payload = Messages(
                            sender_id=worker['worker_id'],
                            sender_first_name=sender_first_name,
                            sender_last_name=sender_last_name,
                            sender_username=sender_profile.username,
                            host_id=user_payload.id,
                            host_first_name=host_first_name,
                            host_last_name=host_last_name,
                            host_username=host_profile.username,
                            message="anlihouse-A236",
                            room=room
                        )
                        message_payload.received = "False"
                        message_payload.sender_assistant = "True"
                        message_payload.messages_backref.append(worker_user)
                        message_payload.db_post()
                        # End 1

                        # Start 2
                        message_payload = Messages(
                            sender_id=worker['worker_id'],
                            sender_first_name=sender_first_name,
                            sender_last_name=sender_last_name,
                            sender_username=sender_profile.username,
                            host_id=user_payload.id,
                            host_first_name=host_first_name,
                            host_last_name=host_last_name,
                            host_username=host_profile.username,
                            message="anlihouse-A237",
                            room=room
                        )
                        message_payload.received = "False"
                        message_payload.sender_assistant = "True"
                        message_payload.messages_backref.append(worker_user)
                        message_payload.db_post()
                        # End 2

                        # Start 3
                        message_payload = Messages(
                            sender_id=worker['worker_id'],
                            sender_first_name=sender_first_name,
                            sender_last_name=sender_last_name,
                            sender_username=sender_profile.username,
                            host_id=user_payload.id,
                            host_first_name=host_first_name,
                            host_last_name=host_last_name,
                            host_username=host_profile.username,
                            message="anlihouse-A238",
                            room=room
                        )
                        message_payload.received = "False"
                        message_payload.sender_assistant = "True"
                        message_payload.messages_backref.append(worker_user)
                        message_payload.db_post()
                        # End 3
                        # End Send First Login Messages

                    else:
                        notification_settings_payload = NotificationSettings(
                            assistant=None
                        )
                        notification_settings_payload.notification_settings_backref.append(user_payload)
                        notification_settings_payload.db_post()

                    data = {"status": 'success', "email": email, "code": code}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(SignUp, '/sign-up')
api.add_resource(SignUpPin, '/sign-up-pin')
api.add_resource(SignUpData, '/sign-up-data')

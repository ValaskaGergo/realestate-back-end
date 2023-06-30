# -*- coding: utf-8 -*-
from app import app, db
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from app.models.models import User, Online, Messages, UserProfile, UserBillingInformation, NotificationSettings, \
    UserPermission
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, desc, asc, func
from dateutil.parser import parse
import itertools
import bleach
from .utilities.utility import BoolStr

mod = Blueprint('notification_module', __name__)
api = Api(mod)

connect_user = reqparse.RequestParser()
connect_user.add_argument('email', required=True)
connect_user.add_argument('sid', required=False)

chat_list = reqparse.RequestParser()
chat_list.add_argument('email', required=True)
chat_list.add_argument('page_number_start', required=True)
chat_list.add_argument('page_number_stop', required=True)
chat_list.add_argument('archived', required=True)

chat_modal = reqparse.RequestParser()
chat_modal.add_argument('email', required=True)
chat_modal.add_argument('message_id', required=True)
chat_modal.add_argument('sender_id', required=True)
chat_modal.add_argument('host_id', required=True)

send_message = reqparse.RequestParser()
send_message.add_argument('room', required=True)
send_message.add_argument('from_username', required=True)
send_message.add_argument('to_username', required=True)
send_message.add_argument('msg', required=True)

received = reqparse.RequestParser()
received.add_argument('message_id', required=True)

rm_message = reqparse.RequestParser()
rm_message.add_argument('message_id', required=True)
rm_message.add_argument('sender_id', required=True)

notifications = reqparse.RequestParser()
notifications.add_argument('notification_type', required=True)
notifications.add_argument('notification_data', required=True)
notifications.add_argument('user_id', required=True)

chat_archive_data = reqparse.RequestParser()
chat_archive_data.add_argument('sender_id', required=True)
chat_archive_data.add_argument('host_id', required=True)
chat_archive_data.add_argument('action_type', required=True)


class PostOnline(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = connect_user.parse_args()

        email = data['email']
        sid = data['sid']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    online_query = Online \
                        .query.join(User.online) \
                        .filter(User.id == user.id).first()

                    online_query.sid = sid
                    online_query.online = "True"
                    online_query.db_post()

                    online_query_all = Online.query.filter_by(online="True").all()
                    datetime_now = datetime.now() - timedelta(minutes=1)

                    for online in online_query_all:
                        if online.updated_at < datetime_now:
                            # online.sid = None
                            online.online = "False"
                            online.db_post()

                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetChatList(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = chat_list.parse_args()

        email = data['email']
        archived = BoolStr.bool(data['archived'])

        page_number_start = int(data['page_number_start'])
        page_number_stop = int(data['page_number_stop'])

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    online_query_all = Online.query.filter_by(online="True").all()
                    datetime_now = datetime.now() - timedelta(minutes=1)

                    for online in online_query_all:
                        if online.updated_at < datetime_now:
                            # online.sid = None
                            online.online = "False"
                            online.db_post()

                    messages_received = Messages.query \
                        .filter(Messages.host_id == user.id) \
                        .filter(Messages.received == "False") \
                        .count()

                    messages_json_list = []

                    if archived:
                        messages_list = Messages.query \
                            .filter(
                            and_(Messages.archive_sender_id == user.id, Messages.two_sided_archiving == False) | and_(
                                Messages.archive_sender_id == user.id, Messages.two_sided_archiving == True) | and_(
                                Messages.archive_host_id == user.id, Messages.two_sided_archiving == True)) \
                            .filter(Messages.message != app.config['USER_TO_USER_FIRST_MESSAGE']) \
                            .order_by(Messages.sender_id, Messages.host_id) \
                            .order_by(Messages.created_at.desc()) \
                            .distinct(Messages.sender_id, Messages.host_id) \
                            .all()
                    else:
                        messages_list = Messages.query \
                            .filter(or_(Messages.sender_id == user.id, Messages.host_id == user.id), and_(
                            or_(Messages.archive_sender_id == None, Messages.archive_sender_id != user.id)),
                                    and_(Messages.two_sided_archiving != True)) \
                            .filter(Messages.message != app.config['USER_TO_USER_FIRST_MESSAGE']) \
                            .order_by(Messages.sender_id, Messages.host_id) \
                            .order_by(Messages.created_at.desc()) \
                            .distinct(Messages.sender_id, Messages.host_id) \
                            .all()

                    for message in messages_list:
                        sender_online = Online \
                            .query.join(User.online) \
                            .filter(User.id == message.sender_id).first()

                        host_online = Online \
                            .query.join(User.online) \
                            .filter(User.id == message.host_id).first()

                        sender_permission = UserPermission \
                            .query.join(User.permission) \
                            .filter(User.id == message.sender_id).first()

                        host_permission = UserPermission \
                            .query.join(User.permission) \
                            .filter(User.id == message.host_id).first()

                        if user.id != message.sender_id:
                            sender_you = "False"
                        else:
                            sender_you = "True"

                        received_count = Messages.query \
                            .filter(and_(Messages.sender_id == message.sender_id, Messages.host_id == user.id)) \
                            .filter(Messages.received == "False") \
                            .count()

                        if message.sender_first_name is not None and message.sender_last_name is not None:
                            sender_first_name = message.sender_first_name
                            sender_last_name = message.sender_last_name
                        else:
                            sender_first_name = message.sender_username
                            sender_last_name = message.sender_username

                        if message.host_first_name is not None and message.host_last_name is not None:
                            host_first_name = message.host_first_name
                            host_last_name = message.host_last_name
                        else:
                            host_first_name = message.host_username
                            host_last_name = message.host_username

                        if user.id == message.sender_id:
                            partner_online = host_online.online
                        else:
                            partner_online = sender_online.online

                        if user.id != message.sender_id:
                            if sender_first_name != sender_last_name:
                                title_name = sender_first_name + " " + sender_last_name
                            else:
                                title_name = sender_last_name
                            from_username = message.host_username
                            to_username = message.sender_username
                        else:
                            if host_first_name != host_last_name:
                                title_name = host_first_name + " " + host_last_name
                            else:
                                title_name = host_last_name
                            from_username = message.sender_username
                            to_username = message.host_username

                        messages_item = {
                            "room": message.room,
                            "partner_online": partner_online,
                            "from_username": from_username,
                            "to_username": to_username,
                            "title_name": title_name,
                            "message_id": message.id,
                            "sender_id": message.sender_id,
                            "sender_first_name": sender_first_name,
                            "sender_last_name": sender_last_name,
                            "sender_online": sender_online.online,
                            "sender_assistant": message.sender_assistant,
                            "host_id": message.host_id,
                            "host_first_name": host_first_name,
                            "host_last_name": host_last_name,
                            "host_online": host_online.online,
                            "message": message.message,
                            "received": message.received,
                            "received_count": received_count,
                            "sender_you": sender_you,
                            "is_sender_worker": sender_permission.is_worker,
                            "is_host_worker": host_permission.is_worker,
                            "created_at": message.created_at,
                            "updated_at": message.updated_at
                        }
                        messages_json_list.append(messages_item)

                    messages_json_list = sorted(messages_json_list, key=lambda x: x['created_at'], reverse=True)
                    messages_json_list = sorted(messages_json_list, key=lambda x: x['room'])

                    messages_json_list = itertools.groupby(messages_json_list, key=lambda x: (x['room']))
                    messages_list_group = []
                    for key, group in messages_json_list:
                        messages_list_group.append(list(group))

                    messages_list = []
                    for k in range(len(messages_list_group)):
                        messages_list.append(messages_list_group[k][0])

                    messages_list = sorted(messages_list, key=lambda x: parse(str(x['created_at'])), reverse=True)

                    # messages_list = list(itertools.islice(itertools.islice(messages_list, page_number, None), 1))
                    # messages_list = list(itertools.islice(messages_list, page_number_start * 3, page_number_stop * 3))

                    payload = {
                        "messages_received": {
                            "received": messages_received
                        },
                        "messages_list": messages_list,
                    }
                    data = {"status": "success", "data": payload}
                    return make_response(jsonify(data), 200)
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetChatModal(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = chat_modal.parse_args()

        email = data['email']
        message_id = int(data['message_id'])
        sender_id = int(data['sender_id'])
        host_id = int(data['host_id'])

        if api_key == app.config['API_KEY']:
            try:
                email = User.query.filter_by(email=email).first()
                message = Messages.query.filter_by(id=message_id).first()
                sender = User.query.filter_by(id=sender_id).first()
                host = User.query.filter_by(id=host_id).first()

                if email is not None and message is not None and sender is not None and host is not None:
                    if email.id == sender.id or email.id == host.id and message.sender_id == sender.id or message.host_id == host.id:
                        # .filter(Messages.message != app.config['USER_TO_USER_FIRST_MESSAGE'])
                        messages_query = Messages.query \
                            .filter(or_(Messages.sender_id == sender.id, Messages.sender_id == host.id)) \
                            .filter(or_(Messages.host_id == host.id, Messages.host_id == sender.id)) \
                            .order_by(asc(Messages.updated_at)) \
                            .all()

                        sender_online = Online \
                            .query.join(User.online) \
                            .filter(User.id == message.sender_id).first()

                        host_online = Online \
                            .query.join(User.online) \
                            .filter(User.id == message.host_id).first()

                        if email.id != message.sender_id:
                            partner_online = sender_online.online
                        else:
                            partner_online = host_online.online

                        messages_list = []
                        for message in messages_query:
                            #  app.logger.info(message.id)
                            #  app.logger.info(message.received)

                            sender_profile = UserProfile \
                                .query.join(User.profile) \
                                .filter(User.id == message.sender_id).first()

                            host_profile = UserProfile \
                                .query.join(User.profile) \
                                .filter(User.id == message.host_id).first()

                            if message.sender_first_name is not None and message.sender_last_name is not None:
                                sender_first_name = message.sender_first_name
                                sender_last_name = message.sender_last_name
                            else:
                                sender_first_name = sender_profile.username
                                sender_last_name = sender_profile.username

                            if message.host_first_name is not None and message.host_last_name is not None:
                                host_first_name = message.host_first_name
                                host_last_name = message.host_last_name
                            else:
                                host_first_name = host_profile.username
                                host_last_name = host_profile.username

                            if email.id != message.sender_id:
                                if sender_first_name != sender_last_name:
                                    title_name = sender_first_name + " " + sender_last_name
                                else:
                                    title_name = sender_last_name
                                from_username = host_profile.username
                                to_username = sender_profile.username
                            else:
                                if host_first_name != host_last_name:
                                    title_name = host_first_name + " " + host_last_name
                                else:
                                    title_name = host_last_name
                                from_username = sender_profile.username
                                to_username = host_profile.username

                            if email.id == message.sender_id:
                                sender_you = "True"
                            else:
                                sender_you = "False"

                            item = {
                                "room": message.room,
                                "partner_online": partner_online,
                                "from_username": from_username,
                                "to_username": to_username,
                                "title_name": title_name,
                                "message_id": message.id,
                                "sender_id": message.sender_id,
                                "sender_first_name": sender_first_name,
                                "sender_last_name": sender_last_name,
                                "sender_online": sender_online.online,
                                "sender_assistant": message.sender_assistant,
                                "host_id": message.host_id,
                                "host_first_name": host_first_name,
                                "host_last_name": host_last_name,
                                "host_online": host_online.online,
                                "message": message.message,
                                "received": message.received,
                                "sender_you": sender_you,
                                "created_at": message.created_at,
                                "updated_at": message.updated_at
                            }
                            messages_list.append(item)

                            received_query = Messages.query \
                                .filter(and_(Messages.host_id == email.id, Messages.sender_id == message.sender_id)) \
                                .filter(Messages.id == message.id) \
                                .filter(Messages.received == "False") \
                                .first()
                            if received_query is not None:
                                received_query.received = "True"
                                received_query.db_post()
                        data = {"data": sorted(messages_list, key=lambda x: parse(str(x['created_at'])), reverse=False)}
                        return make_response(jsonify(data), 200)
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class SendMessage(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = send_message.parse_args()

        room = data['room']
        from_username = data['from_username']
        to_username = data['to_username']
        msg = bleach.clean(data['msg'], attributes={'img': ['src']}, tags=['img'])

        if api_key == app.config['API_KEY']:
            try:
                from_user = User.query \
                    .join(User.profile) \
                    .filter(UserProfile.username == from_username) \
                    .first()

                to_user = User.query \
                    .join(User.profile) \
                    .filter(UserProfile.username == to_username) \
                    .first()

                if from_user is not None and to_user is not None:
                    user_online = Online \
                        .query.join(User.online) \
                        .filter(User.id == from_user.id).first()
                    user_online.online = "True"
                    user_online.db_post()

                    from_name = UserBillingInformation \
                        .query.join(User.billing_information) \
                        .filter(User.id == from_user.id).first()

                    to_name = UserBillingInformation \
                        .query.join(User.billing_information) \
                        .filter(User.id == to_user.id).first()

                    from_username = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == from_user.id).first()

                    to_username = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == to_user.id).first()

                    if from_name.first_name is not None and from_name.last_name is not None:
                        from_first_name = from_name.first_name
                        from_last_name = from_name.last_name
                    else:
                        from_first_name = from_username.username
                        from_last_name = from_username.username

                    if to_name.first_name is not None and to_name.last_name is not None:
                        to_first_name = to_name.first_name
                        to_last_name = to_name.last_name
                    else:
                        to_first_name = to_username.username
                        to_last_name = to_username.username

                    is_messages = Messages.query \
                        .filter(or_(Messages.sender_id == from_user.id, Messages.sender_id == to_user.id)) \
                        .filter(or_(Messages.host_id == to_user.id, Messages.host_id == from_user.id)) \
                        .first()

                    sender_user = User.query.filter_by(id=from_user.id).first()

                    if is_messages is not None:
                        datetime_now = datetime.now()

                        message_payload = Messages(
                            sender_id=from_user.id,
                            sender_first_name=from_first_name,
                            sender_last_name=from_last_name,
                            sender_username=from_username.username,
                            host_id=to_user.id,
                            host_first_name=to_first_name,
                            host_last_name=to_last_name,
                            host_username=to_username.username,
                            message=msg,
                            room=is_messages.room
                        )
                        message_payload.received = "False"
                        message_payload.sender_assistant = "False"

                        is_msg = Messages.query \
                            .filter(or_(Messages.sender_id == from_user.id, Messages.sender_id == to_user.id)) \
                            .filter(or_(Messages.host_id == to_user.id, Messages.host_id == from_user.id)) \
                            .filter(Messages.message != app.config['USER_TO_USER_FIRST_MESSAGE']) \
                            .all()

                        from_user_permission = UserPermission \
                            .query.join(User.permission) \
                            .filter(User.id == from_user.id).first()

                        to_user_permission = UserPermission \
                            .query.join(User.permission) \
                            .filter(User.id == to_user.id).first()

                        from_user_last_msg = Messages.query \
                            .filter(and_(Messages.sender_id == from_user.id, Messages.host_id == to_user.id)) \
                            .filter(Messages.message != app.config['USER_TO_USER_FIRST_MESSAGE']) \
                            .order_by(desc(Messages.created_at)) \
                            .first()

                        to_user_last_msg = Messages.query \
                            .filter(and_(Messages.sender_id == to_user.id, Messages.host_id == from_user.id)) \
                            .filter(Messages.message != app.config['USER_TO_USER_FIRST_MESSAGE']) \
                            .order_by(desc(Messages.created_at)) \
                            .first()

                        is_send_message = "True"

                        if from_user_permission.is_worker == "True":
                            message_payload.messages_backref.append(sender_user)
                            message_payload.db_post()
                        elif to_user_permission.is_worker == "True":
                            message_payload.messages_backref.append(sender_user)
                            message_payload.db_post()
                        elif not is_msg and from_user_permission.subscribed == "True" and from_user_permission.subscribed_chat > 0:
                            from_user_permission.subscribed_chat -= 1
                            message_payload.messages_backref.append(sender_user)
                            message_payload.db_post()
                            from_user_permission.db_post()
                        elif is_msg and from_user_permission.subscribed == "True" and from_user_last_msg is not None and from_user_last_msg.created_at > from_user_permission.subscribed_start:
                            message_payload.messages_backref.append(sender_user)
                            message_payload.db_post()
                            app.logger.info(from_user_last_msg.created_at)
                            app.logger.info(from_user_permission.subscribed_start)
                        elif is_msg and from_user_permission.subscribed == "True" and to_user_last_msg is not None and to_user_last_msg.created_at > from_user_permission.subscribed_start:
                            message_payload.messages_backref.append(sender_user)
                            message_payload.db_post()
                        elif is_msg and from_user_permission.subscribed == "True" and from_user_permission.subscribed_chat > 0 and from_user_last_msg is not None and from_user_last_msg.created_at < from_user_permission.subscribed_start:
                            from_user_permission.subscribed_chat -= 1
                            message_payload.messages_backref.append(sender_user)
                            message_payload.db_post()
                            from_user_permission.db_post()
                        elif is_msg and from_user_permission.subscribed == "True" and from_user_permission.subscribed_chat > 0 and to_user_last_msg is not None and to_user_last_msg.created_at < from_user_permission.subscribed_start:
                            from_user_permission.subscribed_chat -= 1
                            message_payload.messages_backref.append(sender_user)
                            message_payload.db_post()
                            from_user_permission.db_post()
                        else:
                            is_send_message = "False"

                        rm_archived_query = Messages.query \
                            .filter(or_(Messages.sender_id == from_user.id, Messages.sender_id == to_user.id)) \
                            .filter(or_(Messages.host_id == to_user.id, Messages.host_id == from_user.id)) \
                            .all()

                        for archive in rm_archived_query:
                            archive.archive_sender_id = None
                            archive.archive_host_id = None
                            archive.two_sided_archiving = False
                            archive.db_post()

                        data = {"status": "success",
                                "message_id": message_payload.id,
                                "sender_id": message_payload.sender_id,
                                "message": message_payload.message,
                                "room": message_payload.room,
                                "is_send_message": is_send_message
                                }

                        return make_response(jsonify(data), 200)
                    else:
                        pass
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class Received(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = received.parse_args()

        message_id = data['message_id']

        if api_key == app.config['API_KEY']:
            try:
                message = Messages.query.filter_by(id=message_id).first()

                if message is not None:
                    message.received = "True"
                    message.db_post()

                    data = {"status": "success"}
                    return make_response(jsonify(data), 200)
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class RmMessage(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = rm_message.parse_args()

        message_id = data['message_id']
        sender_id = data['sender_id']

        if api_key == app.config['API_KEY']:
            try:
                message = Messages.query.filter_by(id=message_id).first()

                if message is not None:
                    if message.sender_id == int(sender_id):
                        message.message = "anlihouse-A245"
                        message.sender_assistant = "True"
                        message.db_post()

                        data = {"status": "success", "message_id": message.id}
                        return make_response(jsonify(data), 200)
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class Notifications(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = notifications.parse_args()

        notification_type = data['notification_type']
        notification_data = BoolStr.bool(data['notification_data'])
        user_id = int(data['user_id'])

        if api_key == app.config['API_KEY']:
            try:
                notification_settings = NotificationSettings \
                    .query.join(User.notification_settings) \
                    .filter(User.id == user_id).first()

                if notification_settings is not None:
                    if notification_type == "notifications_01":
                        notification_settings.notifications_01 = notification_data
                    elif notification_type == "notifications_02":
                        notification_settings.notifications_02 = notification_data
                    elif notification_type == "notifications_03":
                        notification_settings.notifications_03 = notification_data
                    elif notification_type == "notifications_04":
                        notification_settings.notifications_04 = notification_data
                    elif notification_type == "notifications_05":
                        notification_settings.notifications_05 = notification_data
                    elif notification_type == "notifications_06":
                        notification_settings.notifications_06 = notification_data
                    notification_settings.db_post()

                    data = {"status": "success"}
                    return make_response(jsonify(data), 200)
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class ChatArchive(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = chat_archive_data.parse_args()

        sender_id = int(data['sender_id'])
        host_id = int(data['host_id'])
        action_type = BoolStr.bool(data['action_type'])

        if api_key == app.config['API_KEY']:
            try:
                message_query = Messages.query \
                    .filter(or_(Messages.sender_id == sender_id, Messages.sender_id == host_id)) \
                    .filter(or_(Messages.host_id == host_id, Messages.host_id == sender_id)) \
                    .all()

                if message_query is not None:
                    if action_type:
                        for message in message_query:
                            if message.archive_sender_id is None or message.archive_host_id is None:
                                message.archive_sender_id = sender_id
                                message.archive_host_id = host_id
                                message.db_post()
                            else:
                                message.two_sided_archiving = True
                                message.db_post()
                    else:
                        for message in message_query:
                            if message.two_sided_archiving:
                                message.archive_sender_id = host_id
                                message.archive_host_id = sender_id
                                message.two_sided_archiving = False
                                message.db_post()
                            else:
                                message.archive_sender_id = None
                                message.archive_host_id = None
                                message.two_sided_archiving = False
                                message.db_post()

                    data = {"status": "success"}
                    return make_response(jsonify(data), 200)
                else:
                    data = {"status": "error"}
                    return make_response(jsonify(data), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(PostOnline, '/online')
api.add_resource(GetChatModal, '/chat-modal')
api.add_resource(GetChatList, '/chat-list')
api.add_resource(SendMessage, '/send-message')
api.add_resource(Received, '/received')
api.add_resource(RmMessage, '/rm-message')
api.add_resource(Notifications, '/notifications')
api.add_resource(ChatArchive, '/chat-archive')

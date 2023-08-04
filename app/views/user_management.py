# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, reqparse, Resource
from app.models.models import User, UserPermission, UserProfile, Category, SubCategory, Animal, \
    UserBillingInformation, UserShippingInformation, UserSecondaryEmail, BarionPayment, PayPalPayment, Online, \
    NotificationSettings, Messages
from .utilities.validators import Validation
from .utilities.utility import Pagination, VerificationCode
from dateutil.parser import parse
from sqlalchemy import or_, and_, desc, asc, func
import math
import itertools
from pyjsonq import JsonQ
from slugify import slugify

mod = Blueprint('user_management_module', __name__)
api = Api(mod)

get_user_all = reqparse.RequestParser()
get_user_all.add_argument('page_number', required=True)
get_user_all.add_argument('type', required=True)

delete_user = reqparse.RequestParser()
delete_user.add_argument('email', required=True)

user_management_permission = reqparse.RequestParser()
user_management_permission.add_argument('email', required=True)
user_management_permission.add_argument('data_type', required=True)
user_management_permission.add_argument('data_status', required=True)
user_management_permission.add_argument('data_user_id', required=True)

user_management_list_of_uploaded_animals = reqparse.RequestParser()
user_management_list_of_uploaded_animals.add_argument('email', required=True)

user_management_add_user = reqparse.RequestParser()
user_management_add_user.add_argument('worker_id', required=True)
user_management_add_user.add_argument('worker_username', required=True)
user_management_add_user.add_argument('email', required=True)
user_management_add_user.add_argument('name', required=True)
user_management_add_user.add_argument('password', required=True)
user_management_add_user.add_argument('password_confirm', required=True)

user_management_get_invoices = reqparse.RequestParser()
user_management_get_invoices.add_argument('email', required=True)


class GetUserAll(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_user_all.parse_args()

        if api_key == app.config['API_KEY']:
            try:
                page_number = int(data['page_number'])
                page_type = data['type']
                users_limit = 25
                offset_number = (page_number * users_limit) - users_limit

                # users_query_count = User.query.count()
                users_query_count = 0
                if page_type == "active":
                    users_query_count = UserPermission.query.join(User.permission) \
                        .filter(UserPermission.inactive_account == "False") \
                        .filter(User.deleted == "False") \
                        .count()
                elif page_type == "inactive":
                    users_query_count = UserPermission.query.join(User.permission) \
                        .filter(UserPermission.inactive_account == "True") \
                        .filter(User.deleted == "False") \
                        .count()
                elif page_type == "deleted":
                    users_query_count = UserPermission.query.join(User.permission) \
                        .filter(UserPermission.inactive_account == "True") \
                        .filter(User.deleted == "True") \
                        .count()
                pagination_count = math.ceil(users_query_count / users_limit)
                pagination_first = 1
                pagination_last = pagination_count
                pagination_next = page_number + 1
                pagination_previous = page_number - 1

                users_query = User.query.order_by(desc(User.created_at)).offset(offset_number).limit(users_limit).all()
                users_list = []

                try:
                    pagination_list = Pagination.create(int(pagination_count), int(page_number))
                except:
                    pagination_list = [1]

                pagination = {
                    "page_number": int(page_number),
                    "users_limit": int(users_limit),
                    "users_count": int(users_query_count),
                    "pagination_count": int(pagination_count),
                    "pagination_first": int(pagination_first),
                    "pagination_last": int(pagination_last),
                    "pagination_next": int(pagination_next),
                    "pagination_previous": int(pagination_previous)
                }

                for users_data in users_query:
                    for permission, profile, billing, shipping in itertools.product(users_data.permission,
                                                                                    users_data.profile,
                                                                                    users_data.billing_information,
                                                                                    users_data.shipping_information):
                        item = {
                            "user": {
                                "id": users_data.id,
                                "email": users_data.email,
                                "deleted": users_data.deleted,
                                "created_at": users_data.created_at,
                                "updated_at": users_data.updated_at
                            },
                            "user_profile": {
                                "username": profile.username
                            },
                            "user_permission": {
                                "is_worker": permission.is_worker,
                                "is_admin": permission.is_admin,
                                "subscribed": permission.subscribed,
                                "subscribed_start": permission.subscribed_start,
                                "subscribed_end": permission.subscribed_end,
                                "inactive_account": permission.inactive_account,
                                "last_modification_user_id": permission.last_modification_user_id,
                                "last_modification_user_name": permission.last_modification_user_name,
                                "created_at": permission.created_at,
                                "updated_at": permission.updated_at
                            },
                            "user_billing_information": {
                                "is_company": billing.is_company,
                                "first_name": billing.first_name,
                                "last_name": billing.last_name,
                                "company_name": billing.company_name,
                                "company_tax": billing.company_tax,
                                "phone": billing.phone,
                                "email": billing.email,
                                "country": billing.country,
                                "country_vat": billing.country_vat,
                                "zip_number": billing.zip_number,
                                "place": billing.place,
                                "street": billing.street,
                                "is_shipping_address": billing.is_shipping_address,
                                "completed": billing.completed
                            },
                            "user_shipping_information": {
                                "first_name": shipping.first_name,
                                "last_name": shipping.last_name,
                                "company_name": shipping.company_name,
                                "phone": shipping.phone,
                                "email": shipping.email,
                                "country": shipping.country,
                                "zip_number": shipping.zip_number,
                                "place": shipping.place,
                                "street": shipping.street,
                            }
                        }
                        users_list.append(item)

                data = {"pagination_list": pagination_list, "pagination": pagination, "data": sorted(users_list, key=lambda x: parse(str(x['user']['created_at'])), reverse=True)}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class DeleteUser(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = delete_user.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    user_permission = UserPermission \
                        .query.join(User.permission) \
                        .filter(User.id == user.id).first()

                    if user_permission.inactive_account == "True":
                        user_permission.inactive_account = "False"
                        user_permission.db_post()

                    user.deleted = "True"
                    user.email = user.email[::-1]
                    user.db_post()
                    # user.db_delete()

                    data = {"status": 'success'}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class BackDeleteUser(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = delete_user.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    user.deleted = "False"
                    user.email = user.email[::-1]
                    user.db_post()

                    data = {"status": 'success'}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class ForceDeleteUser(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = delete_user.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    user_permission = UserPermission \
                        .query.join(User.permission) \
                        .filter(User.id == user.id).first()

                    if user_permission.inactive_account == "True":
                        user_permission.inactive_account = "False"
                        user_permission.db_post()

                    user.db_delete()

                    data = {"status": 'success'}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class UserManagementPermission(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = user_management_permission.parse_args()

        email = data['email']
        data_type = data['data_type']
        data_status = data['data_status']
        data_user_id = data['data_user_id']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:

                    #  Admin
                    user_profile = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == user.id).first()

                    #  User
                    user_permission = UserPermission \
                        .query.join(User.permission) \
                        .filter(User.id == data_user_id).first()

                    if data_type == "is_admin_settings_management":
                        if data_status == "True":
                            user_permission.is_admin_settings_management = "False"
                        else:
                            user_permission.is_admin_settings_management = "True"
                    elif data_type == "is_user_management":
                        if data_status == "True":
                            user_permission.is_user_management = "False"
                        else:
                            user_permission.is_user_management = "True"
                    elif data_type == "is_category_management":
                        if data_status == "True":
                            user_permission.is_category_management = "False"
                        else:
                            user_permission.is_category_management = "True"
                    elif data_type == "is_notifications":
                        if data_status == "True":
                            user_permission.is_notifications = "False"
                        else:
                            user_permission.is_notifications = "True"
                    elif data_type == "inactive_account":
                        if data_status == "True":
                            user_permission.inactive_account = "False"
                        else:
                            user_permission.inactive_account = "True"

                    if user_permission.is_admin_settings_management == "True":
                        user_permission.is_worker = "True"
                    elif user_permission.is_user_management == "True":
                        user_permission.is_worker = "True"
                    elif user_permission.is_category_management == "True":
                        user_permission.is_worker = "True"
                    elif user_permission.is_notifications == "True":
                        user_permission.is_worker = "True"
                    else:
                        user_permission.is_worker = "False"

                    if user_permission.is_admin_settings_management == "True" and \
                            user_permission.is_user_management == "True" and \
                            user_permission.is_category_management == "True" and \
                            user_permission.is_notifications == "True":
                        user_permission.is_admin = "True"
                    else:
                        user_permission.is_admin = "False"

                    user_permission.last_modification_user_id = user.id
                    user_permission.last_modification_user_name = user_profile.username

                    user_permission.db_post()

                    data = {"status": 'success', "last_modification_user_id": user.id,
                            "last_modification_user_name": user_profile.username,
                            "updated_at": user_permission.updated_at}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class UserManagementListOfUploadedAnimals(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = user_management_list_of_uploaded_animals.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                category_query = Category.query.all()
                subcategory_query = SubCategory.query.all()

                animals_list = []
                photo_item = {}
                video_item = {}
                pdf_item = {}
                category_item = {}
                subcategory_item = {}
                user_item = {}

                if user is not None:
                    for animal in user.animal.order_by(desc(Animal.created_at)):
                        for photo in animal.photos:
                            photo_item = {
                                "id": photo.id,
                                "img_01": photo.img_01,
                                "img_02": photo.img_02,
                                "img_03": photo.img_03,
                                "img_04": photo.img_04,
                                "img_05": photo.img_05,
                                "img_06": photo.img_06,
                                "img_07": photo.img_07,
                                "img_08": photo.img_08,
                                "img_09": photo.img_09,
                                "img_10": photo.img_10,
                                "created_at": photo.created_at,
                                "updated_at": photo.updated_at
                            }
                        for video in animal.videos:
                            video_item = {
                                "id": video.id,
                                "video_01": video.video_01,
                                "created_at": video.created_at,
                                "updated_at": video.updated_at
                            }
                        for pdf in animal.pdf:
                            pdf_item = {
                                "id": pdf.id,
                                "x_ray": pdf.x_ray,
                                "created_at": pdf.created_at,
                                "updated_at": pdf.updated_at
                            }
                        for category in category_query:
                            if category.id is animal.category_id:
                                category_item = {
                                    "name_hu": category.name_hu,
                                    "name_en": category.name_en,
                                    "name_en_slug": slugify(category.name_en),
                                    "name_de": category.name_de,
                                    "name_fr": category.name_fr,
                                    "name_es": category.name_es,
                                }
                        for subcategory in subcategory_query:
                            if subcategory.id is animal.subcategory_id:
                                subcategory_item = {
                                    "name_hu": subcategory.name_hu,
                                    "name_en": subcategory.name_en,
                                    "name_en_slug": slugify(subcategory.name_en),
                                    "name_de": subcategory.name_de,
                                    "name_fr": subcategory.name_fr,
                                    "name_es": subcategory.name_es,
                                }
                        item = {
                            "animal": {
                                "id": animal.id,
                                "category_id": animal.category_id,
                                "subcategory_id": animal.subcategory_id,
                                "name": animal.name,
                                "country_residence": animal.country_residence,
                                "be_used_for_hu": animal.be_used_for_hu,
                                "be_used_for_en": animal.be_used_for_en,
                                "be_used_for_de": animal.be_used_for_de,
                                "be_used_for_fr": animal.be_used_for_fr,
                                "be_used_for_es": animal.be_used_for_es,
                                "gender_hu": animal.gender_hu,
                                "gender_en": animal.gender_en,
                                "gender_de": animal.gender_de,
                                "gender_fr": animal.gender_fr,
                                "gender_es": animal.gender_es,
                                "color_hu": animal.color_hu,
                                "color_en": animal.color_en,
                                "color_de": animal.color_de,
                                "color_fr": animal.color_fr,
                                "color_es": animal.color_es,
                                "brief_description": animal.brief_description,
                                "brief_description_detect_lang": animal.brief_description_detect_lang,
                                "description": animal.description,
                                "description_detect_lang": animal.description_detect_lang,
                                "page_url": animal.page_url,
                                "url_01": animal.url_01,
                                "url_02": animal.url_02,
                                "price": animal.price,
                                "visibility": animal.visibility,
                                "worker_visibility": animal.worker_visibility,
                                "last_modification_user_name": animal.last_modification_user_name,
                                "last_modification_user_id": animal.last_modification_user_id,
                                "created_at": animal.created_at,
                                "updated_at": animal.updated_at
                            },
                            "photo": photo_item,
                            "video": video_item,
                            "pdf": pdf_item,
                            "category": category_item,
                            "subcategory": subcategory_item,
                            "user": {
                                "user_id": user.id,
                                "user_email": user.email
                            }
                        }
                        animals_list.append(item)
                    data = {
                        "data": sorted(animals_list, key=lambda x: parse(str(x['animal']['updated_at'])), reverse=True)
                    }
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class UserManagementAddUser(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = user_management_add_user.parse_args()

        worker_id = data['worker_id']
        worker_username = data['worker_username']
        email = data['email']
        name = data['name']
        password = data['password']
        password_confirm = data['password_confirm']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.add_user(email, name, password, password_confirm)
                if validation['status'] == "success":

                    user_payload = User(
                        email=email
                    )
                    user_payload.password_hash(password)
                    user_payload.privacy = "True"
                    user_payload.db_post()

                    user_profile_payload = UserProfile(
                        username=name + str(user_payload.id)
                    )
                    user_profile_payload.user_profile_backref.append(user_payload)
                    user_profile_payload.db_post()

                    user_permission_payload = UserPermission()
                    user_permission_payload.user_permission_backref.append(user_payload)
                    user_permission_payload.last_modification_user_id = worker_id
                    user_permission_payload.last_modification_user_name = worker_username
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
                            if worker.id != 1:
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

                    data = {"status": 'success'}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class UserManagementGetInvoices(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = user_management_get_invoices.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                barion_payment_query = BarionPayment \
                    .query.join(User.barion_payment) \
                    .filter(User.id == user.id) \
                    .filter(BarionPayment.status == "Succeeded") \
                    .order_by(desc(BarionPayment.created_at)).all()

                paypal_payment_query = PayPalPayment \
                    .query.join(User.paypal_payment) \
                    .filter(User.id == user.id) \
                    .filter(PayPalPayment.status == "APPROVED") \
                    .filter(User.id == user.id) \
                    .order_by(desc(PayPalPayment.created_at)).all()

                invoices_list = []

                for barion in barion_payment_query:
                    days = int(barion.order_number.split("-")[2].split(".")[0])
                    if days > 200:
                        month = 12
                    elif days > 40:
                        month = 6
                    else:
                        month = 1
                    item = {
                        "payment_type": barion.payment_type,
                        "payment_id": barion.payment_id,
                        "payment_request_id": barion.payment_request_id,
                        "month": month,
                        "funding_source": barion.funding_source,
                        "price": float(barion.price),
                        "vat": float(barion.vat),
                        "total": float(barion.total),
                        "currency": barion.currency,
                        "billing_url": barion.billing_url,
                        "created_at": str(barion.updated_at),
                    }
                    invoices_list.append(item)

                for paypal in paypal_payment_query:
                    days = int(paypal.order_number.split("-")[2].split(".")[0])
                    if days > 200:
                        month = 12
                    elif days > 40:
                        month = 6
                    else:
                        month = 1
                    item = {
                        "payment_type": paypal.payment_type,
                        "payment_id": paypal.payment_id,
                        "payment_request_id": paypal.payment_request_id,
                        "month": month,
                        "funding_source": paypal.funding_source,
                        "price": float(paypal.price),
                        "vat": float(paypal.vat),
                        "total": float(paypal.total),
                        "currency": paypal.currency,
                        "billing_url": paypal.billing_url,
                        "created_at": str(paypal.created_at),
                    }
                    invoices_list.append(item)

                data = {"data": sorted(invoices_list, key=lambda x: parse(str(x['created_at'])), reverse=True)}
                return make_response(jsonify(data), 200)

            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(GetUserAll, '/get-user-all')
api.add_resource(DeleteUser, '/user-management-delete-user')
api.add_resource(BackDeleteUser, '/user-management-back-delete-user')
api.add_resource(ForceDeleteUser, '/user-management-force-delete-user')
api.add_resource(UserManagementPermission, '/user-management-permission')
api.add_resource(UserManagementListOfUploadedAnimals, '/user-management-list-of-uploaded-animals')
api.add_resource(UserManagementAddUser, '/user-management-add-user')
api.add_resource(UserManagementGetInvoices, '/user-management-get-invoices')

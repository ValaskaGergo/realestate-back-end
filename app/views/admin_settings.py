# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, reqparse, Resource
from app.models.models import User, UserProfile, AdminSettings
from .utilities.validators import Validation
from dateutil.parser import parse

mod = Blueprint('admin_settings_module', __name__)
api = Api(mod)

add_settings = reqparse.RequestParser()
add_settings.add_argument('email', required=True)
add_settings.add_argument('settings_name', required=True)
add_settings.add_argument('settings_type', required=True)
add_settings.add_argument('settings_value', required=True)

get_settings = reqparse.RequestParser()
get_settings.add_argument('settings_id', required=True)

edit_settings = reqparse.RequestParser()
edit_settings.add_argument('email', required=True)
edit_settings.add_argument('settings_id', required=True)
edit_settings.add_argument('settings_name', required=True)
edit_settings.add_argument('settings_type', required=True)
edit_settings.add_argument('settings_value', required=True)


class AddSettings(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = add_settings.parse_args()

        email = data['email']
        settings_name = data['settings_name']
        settings_type = data['settings_type']
        settings_value = data['settings_value']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.add_settings(settings_name, settings_type, settings_value)
                if validation['status'] == "success":

                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        user_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user.id).first()

                        admin_settings_payload = AdminSettings(
                            settings_user_id=user.id,
                            settings_user_name=user_profile.username,
                            settings_name=settings_name,
                            settings_type=settings_type,
                            settings_value=settings_value
                        )
                        admin_settings_payload.db_post()
                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetAdminSettingsAll(Resource):
    @staticmethod
    def get():
        api_key = request.headers['X-Api-Key']

        if api_key == app.config['API_KEY']:
            try:
                settings_query = AdminSettings.query.all()
                settings_list = []

                for settings_data in settings_query:
                    item = {
                        "settings_id": settings_data.id,
                        "settings_user_id": settings_data.settings_user_id,
                        "settings_user_name": settings_data.settings_user_name,
                        "settings_name": settings_data.settings_name,
                        "settings_type": settings_data.settings_type,
                        "settings_value": settings_data.settings_value,
                        "created_at": str(settings_data.created_at),
                        "updated_at": str(settings_data.updated_at),
                    }
                    settings_list.append(item)

                data = {"data": sorted(settings_list, key=lambda x: parse(str(x['settings_id'])), reverse=False)}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetAdminSettings(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_settings.parse_args()

        settings_id = int(data['settings_id'])

        if api_key == app.config['API_KEY']:
            try:
                settings_query = AdminSettings.query.filter_by(id=settings_id).first()
                settings_list = []

                if settings_query is not None:
                    item = {
                        "settings_id": settings_query.id,
                        "settings_user_id": settings_query.settings_user_id,
                        "settings_user_name": settings_query.settings_user_name,
                        "settings_name": settings_query.settings_name,
                        "settings_type": settings_query.settings_type,
                        "settings_value": settings_query.settings_value,
                        "created_at": str(settings_query.created_at),
                        "updated_at": str(settings_query.updated_at),
                    }
                    settings_list.append(item)

                    data = {"data": sorted(settings_list, key=lambda x: parse(x['updated_at']), reverse=True)}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class EditSettings(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = edit_settings.parse_args()

        email = data['email']
        settings_id = data['settings_id']
        settings_name = data['settings_name']
        settings_type = data['settings_type']
        settings_value = data['settings_value']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.add_settings(settings_name, settings_type, settings_value)
                if validation['status'] == "success":

                    user = User.query.filter_by(email=email).first()
                    settings_query = AdminSettings.query.filter_by(id=settings_id).first()

                    if user is not None and settings_query is not None:
                        user_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user.id).first()

                        settings_query.settings_user_id = user.id
                        settings_query.settings_user_name = user_profile.username
                        settings_query.settings_name = settings_name
                        settings_query.settings_type = settings_type
                        settings_query.settings_value = settings_value
                        settings_query.db_post()
                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(AddSettings, '/add-settings')
api.add_resource(GetAdminSettingsAll, '/get-admin-settings-all')
api.add_resource(GetAdminSettings, '/get-admin-settings')
api.add_resource(EditSettings, '/edit-settings')

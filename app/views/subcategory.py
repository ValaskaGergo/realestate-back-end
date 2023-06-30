# -*- coding: utf-8 -*-
from app import app, db
from flask import Blueprint, request, make_response, jsonify, json
from flask_restful import Api, Resource, reqparse
from app.models.models import User, UserProfile, Category, SubCategory
from .utilities.validators import Validation
from dateutil.parser import parse

mod = Blueprint('subcategory_module', __name__)
api = Api(mod)

add_subcategory_all = reqparse.RequestParser()
add_subcategory_all.add_argument('email', required=True)
add_subcategory_all.add_argument('category_id_select', required=True)
add_subcategory_all.add_argument('visibility', required=True)
add_subcategory_all.add_argument('name_hu', required=True)
add_subcategory_all.add_argument('name_en', required=True)
add_subcategory_all.add_argument('name_de', required=True)
add_subcategory_all.add_argument('name_fr', required=True)
add_subcategory_all.add_argument('name_es', required=True)
add_subcategory_all.add_argument('description_hu', required=True)
add_subcategory_all.add_argument('description_en', required=True)
add_subcategory_all.add_argument('description_de', required=True)
add_subcategory_all.add_argument('description_fr', required=True)
add_subcategory_all.add_argument('description_es', required=True)
add_subcategory_all.add_argument('img_data', required=False)

get_subcategory = reqparse.RequestParser()
get_subcategory.add_argument('email', required=True)
get_subcategory.add_argument('subcategory_id', required=True)

edit_subcategory = reqparse.RequestParser()
edit_subcategory.add_argument('email', required=True)
edit_subcategory.add_argument('subcategory_id', required=True)
edit_subcategory.add_argument('category_id_select', required=True)
edit_subcategory.add_argument('visibility', required=True)
edit_subcategory.add_argument('name_hu', required=True)
edit_subcategory.add_argument('name_en', required=True)
edit_subcategory.add_argument('name_de', required=True)
edit_subcategory.add_argument('name_fr', required=True)
edit_subcategory.add_argument('name_es', required=True)
edit_subcategory.add_argument('description_hu', required=True)
edit_subcategory.add_argument('description_en', required=True)
edit_subcategory.add_argument('description_de', required=True)
edit_subcategory.add_argument('description_fr', required=True)
edit_subcategory.add_argument('description_es', required=True)
edit_subcategory.add_argument('img_data', required=False)

delete_subcategory = reqparse.RequestParser()
delete_subcategory.add_argument('email', required=True)
delete_subcategory.add_argument('subcategory_id', required=True)


class AddSubCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = add_subcategory_all.parse_args()

        email = data['email']
        category_id_select = data['category_id_select']
        visibility = data['visibility']
        name_hu = data['name_hu']
        name_en = data['name_en']
        name_de = data['name_de']
        name_fr = data['name_fr']
        name_es = data['name_es']
        description_hu = data['description_hu']
        description_en = data['description_en']
        description_de = data['description_de']
        description_fr = data['description_fr']
        description_es = data['description_es']
        img_data = data['img_data']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.add_subcategory(category_id_select, name_hu, name_en, name_de, name_fr, name_es,
                                                        description_hu, description_en, description_de, description_fr,
                                                        description_es)
                if validation['status'] == "success":
                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        category_query = Category.query.filter_by(id=category_id_select).first()

                        user_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user.id).first()

                        if img_data:
                            category_photo_data = json.loads(img_data)
                            category_photo = category_photo_data['folder']
                        else:
                            img_data = None
                            category_photo = None

                        subcategory_payload = SubCategory(
                            category_id=category_id_select,
                            category_user_id=user.id,
                            category_user_name=user_profile.username,
                            name_hu=name_hu,
                            name_en=name_en,
                            name_de=name_de,
                            name_fr=name_fr,
                            name_es=name_es,
                            description_hu=description_hu,
                            description_en=description_en,
                            description_de=description_de,
                            description_fr=description_fr,
                            description_es=description_es,
                            img_data=img_data,
                            img=category_photo,
                            visibility=visibility
                        )

                        subcategory_payload.sub_category_backref.append(category_query)
                        subcategory_payload.db_post()

                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetSubCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_subcategory.parse_args()

        subcategory_id = int(data['subcategory_id'])

        if api_key == app.config['API_KEY']:
            try:
                subcategory_query = SubCategory.query.filter_by(id=subcategory_id).first()
                subcategory_list = []

                if subcategory_query is not None:
                    item = {
                        "subcategory_id": subcategory_query.id,
                        "category_id": subcategory_query.category_id,
                        "category_user_id": subcategory_query.category_user_id,
                        "category_user_name": subcategory_query.category_user_name,
                        "name_hu": subcategory_query.name_hu,
                        "name_en": subcategory_query.name_en,
                        "name_de": subcategory_query.name_de,
                        "name_fr": subcategory_query.name_fr,
                        "name_es": subcategory_query.name_es,
                        "description_hu": subcategory_query.description_hu,
                        "description_en": subcategory_query.description_en,
                        "description_de": subcategory_query.description_de,
                        "description_fr": subcategory_query.description_fr,
                        "description_es": subcategory_query.description_es,
                        "visibility": subcategory_query.visibility,
                        "img_data": subcategory_query.img_data,
                        "img": subcategory_query.img,
                        "created_at": str(subcategory_query.created_at),
                        "updated_at": str(subcategory_query.updated_at),
                    }
                    subcategory_list.append(item)

                    data = {"data": sorted(subcategory_list, key=lambda x: parse(x['updated_at']), reverse=True)}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class EditSubCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = edit_subcategory.parse_args()

        email = data['email']
        subcategory_id = data['subcategory_id']
        category_id_select = data['category_id_select']
        visibility = data['visibility']
        name_hu = data['name_hu']
        name_en = data['name_en']
        name_de = data['name_de']
        name_fr = data['name_fr']
        name_es = data['name_es']
        description_hu = data['description_hu']
        description_en = data['description_en']
        description_de = data['description_de']
        description_fr = data['description_fr']
        description_es = data['description_es']
        img_data = data['img_data']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.add_subcategory(category_id_select, name_hu, name_en, name_de, name_fr, name_es,
                                                        description_hu, description_en,
                                                        description_de, description_fr,
                                                        description_es)
                if validation['status'] == "success":
                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        category_query = Category.query.filter_by(id=category_id_select).first()

                        user_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user.id).first()

                        if img_data:
                            category_photo_data = json.loads(img_data)
                            category_photo = category_photo_data['folder']
                        else:
                            img_data = None
                            category_photo = None

                        subcategory_payload = SubCategory.query.filter_by(id=subcategory_id).first()

                        subcategory_payload.category_id = category_id_select
                        subcategory_payload.category_user_id = user.id
                        subcategory_payload.category_user_name = user_profile.username
                        subcategory_payload.name_hu = name_hu
                        subcategory_payload.name_en = name_en
                        subcategory_payload.name_de = name_de
                        subcategory_payload.name_fr = name_fr
                        subcategory_payload.name_es = name_es
                        subcategory_payload.description_hu = description_hu
                        subcategory_payload.description_en = description_en
                        subcategory_payload.description_de = description_de
                        subcategory_payload.description_fr = description_fr
                        subcategory_payload.description_es = description_es
                        subcategory_payload.img_data = img_data
                        subcategory_payload.img = category_photo
                        subcategory_payload.visibility = visibility
                        subcategory_payload.db_post()

                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class DeleteSubCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = delete_subcategory.parse_args()

        email = data['email']
        subcategory_id = data['subcategory_id']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    subcategory_payload = SubCategory.query.filter_by(id=subcategory_id).first()
                    subcategory_payload.db_delete()

                    data = {"status": 'success'}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(AddSubCategory, '/add-subcategory')
api.add_resource(GetSubCategory, '/get-subcategory')
api.add_resource(EditSubCategory, '/edit-subcategory')
api.add_resource(DeleteSubCategory, '/delete-subcategory')

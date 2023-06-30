# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify, json
from flask_restful import Api, Resource, reqparse
from app.models.models import User, UserProfile, Category, SubCategory
from .utilities.validators import Validation
from dateutil.parser import parse
from .utilities.utility import StringToList

mod = Blueprint('category_module', __name__)
api = Api(mod)

add_category_all = reqparse.RequestParser()
add_category_all.add_argument('email', required=True)
add_category_all.add_argument('visibility', required=True)
add_category_all.add_argument('name_hu', required=True)
add_category_all.add_argument('name_en', required=True)
add_category_all.add_argument('name_de', required=True)
add_category_all.add_argument('name_fr', required=True)
add_category_all.add_argument('name_es', required=True)
add_category_all.add_argument('gender_hu', required=False)
add_category_all.add_argument('gender_en', required=False)
add_category_all.add_argument('gender_de', required=False)
add_category_all.add_argument('gender_fr', required=False)
add_category_all.add_argument('gender_es', required=False)
add_category_all.add_argument('be_used_for_hu', required=False)
add_category_all.add_argument('be_used_for_en', required=False)
add_category_all.add_argument('be_used_for_de', required=False)
add_category_all.add_argument('be_used_for_fr', required=False)
add_category_all.add_argument('be_used_for_es', required=False)
add_category_all.add_argument('color_hu', required=False)
add_category_all.add_argument('color_en', required=False)
add_category_all.add_argument('color_de', required=False)
add_category_all.add_argument('color_fr', required=False)
add_category_all.add_argument('color_es', required=False)
add_category_all.add_argument('img_data', required=False)

get_category = reqparse.RequestParser()
get_category.add_argument('email', required=True)
get_category.add_argument('category_id', required=True)

edit_category = reqparse.RequestParser()
edit_category.add_argument('email', required=True)
edit_category.add_argument('category_id', required=True)
edit_category.add_argument('visibility', required=True)
edit_category.add_argument('name_hu', required=True)
edit_category.add_argument('name_en', required=True)
edit_category.add_argument('name_de', required=True)
edit_category.add_argument('name_fr', required=True)
edit_category.add_argument('name_es', required=True)
edit_category.add_argument('gender_hu', required=False)
edit_category.add_argument('gender_en', required=False)
edit_category.add_argument('gender_de', required=False)
edit_category.add_argument('gender_fr', required=False)
edit_category.add_argument('gender_es', required=False)
edit_category.add_argument('be_used_for_hu', required=False)
edit_category.add_argument('be_used_for_en', required=False)
edit_category.add_argument('be_used_for_de', required=False)
edit_category.add_argument('be_used_for_fr', required=False)
edit_category.add_argument('be_used_for_es', required=False)
edit_category.add_argument('color_hu', required=False)
edit_category.add_argument('color_en', required=False)
edit_category.add_argument('color_de', required=False)
edit_category.add_argument('color_fr', required=False)
edit_category.add_argument('color_es', required=False)
edit_category.add_argument('img_data', required=False)

delete_category = reqparse.RequestParser()
delete_category.add_argument('email', required=True)
delete_category.add_argument('category_id', required=True)

get_category_to_subcategories = reqparse.RequestParser()
get_category_to_subcategories.add_argument('category_id', required=True)


class AddCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = add_category_all.parse_args()

        email = data['email']
        visibility = data['visibility']
        name_hu = data['name_hu']
        name_en = data['name_en']
        name_de = data['name_de']
        name_fr = data['name_fr']
        name_es = data['name_es']
        gender_hu = data['gender_hu']
        gender_en = data['gender_en']
        gender_de = data['gender_de']
        gender_fr = data['gender_fr']
        gender_es = data['gender_es']
        be_used_for_hu = data['be_used_for_hu']
        be_used_for_en = data['be_used_for_en']
        be_used_for_de = data['be_used_for_de']
        be_used_for_fr = data['be_used_for_fr']
        be_used_for_es = data['be_used_for_es']
        color_hu = data['color_hu']
        color_en = data['color_en']
        color_de = data['color_de']
        color_fr = data['color_fr']
        color_es = data['color_es']
        img_data = data['img_data']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.add_category(name_hu, name_en, name_de, name_fr, name_es)
                if validation['status'] == "success":
                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        user_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user.id).first()

                        if img_data:
                            category_photo_data = json.loads(img_data)
                            category_photo = category_photo_data['filename']
                        else:
                            img_data = None
                            category_photo = None

                        category_payload = Category(
                            category_user_id=user.id,
                            category_user_name=user_profile.username,
                            name_hu=name_hu,
                            name_en=name_en,
                            name_de=name_de,
                            name_fr=name_fr,
                            name_es=name_es,
                            gender_hu=StringToList.list(gender_hu),
                            gender_en=StringToList.list(gender_en),
                            gender_de=StringToList.list(gender_de),
                            gender_fr=StringToList.list(gender_fr),
                            gender_es=StringToList.list(gender_es),
                            be_used_for_hu=StringToList.list(be_used_for_hu),
                            be_used_for_en=StringToList.list(be_used_for_en),
                            be_used_for_de=StringToList.list(be_used_for_de),
                            be_used_for_fr=StringToList.list(be_used_for_fr),
                            be_used_for_es=StringToList.list(be_used_for_es),
                            color_hu=StringToList.list(color_hu),
                            color_en=StringToList.list(color_en),
                            color_de=StringToList.list(color_de),
                            color_fr=StringToList.list(color_fr),
                            color_es=StringToList.list(color_es),
                            img_data=img_data,
                            img=category_photo,
                            visibility=visibility
                        )
                        category_payload.db_post()

                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetCategoryAll(Resource):
    @staticmethod
    def get():
        api_key = request.headers['X-Api-Key']

        if api_key == app.config['API_KEY']:
            try:
                category_query = Category.query.all()
                category_list = []

                for category_data in category_query:
                    item = {
                        "category_id": category_data.id,
                        "category_user_id": category_data.category_user_id,
                        "category_user_name": category_data.category_user_name,
                        "name_hu": category_data.name_hu,
                        "name_en": category_data.name_en,
                        "name_de": category_data.name_de,
                        "name_fr": category_data.name_fr,
                        "name_es": category_data.name_es,
                        "gender_hu": category_data.gender_hu,
                        "gender_en": category_data.gender_en,
                        "gender_de": category_data.gender_de,
                        "gender_fr": category_data.gender_fr,
                        "gender_es": category_data.gender_es,
                        "be_used_for_hu": category_data.be_used_for_hu,
                        "be_used_for_en": category_data.be_used_for_en,
                        "be_used_for_de": category_data.be_used_for_de,
                        "be_used_for_fr": category_data.be_used_for_fr,
                        "be_used_for_es": category_data.be_used_for_es,
                        "color_hu": category_data.color_hu,
                        "color_en": category_data.color_en,
                        "color_de": category_data.color_de,
                        "color_fr": category_data.color_fr,
                        "color_es": category_data.color_es,
                        "img": category_data.img,
                        "visibility": category_data.visibility,
                        "subcategory_count": category_data.sub_category.count(),
                        "created_at": str(category_data.created_at),
                        "updated_at": str(category_data.updated_at),
                    }
                    category_list.append(item)

                data = {"data": sorted(category_list, key=lambda x: parse(str(x['updated_at'])), reverse=True)}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_category.parse_args()

        category_id = int(data['category_id'])

        if api_key == app.config['API_KEY']:
            try:
                category_query = Category.query.filter_by(id=category_id).first()
                category_list = []

                if category_query is not None:
                    item = {
                        "category_id": category_query.id,
                        "category_user_id": category_query.category_user_id,
                        "category_user_name": category_query.category_user_name,
                        "name_hu": category_query.name_hu,
                        "name_en": category_query.name_en,
                        "name_de": category_query.name_de,
                        "name_fr": category_query.name_fr,
                        "name_es": category_query.name_es,
                        "gender_hu": StringToList.string(category_query.gender_hu),
                        "gender_en": StringToList.string(category_query.gender_en),
                        "gender_de": StringToList.string(category_query.gender_de),
                        "gender_fr": StringToList.string(category_query.gender_fr),
                        "gender_es": StringToList.string(category_query.gender_es),
                        "be_used_for_hu": StringToList.string(category_query.be_used_for_hu),
                        "be_used_for_en": StringToList.string(category_query.be_used_for_en),
                        "be_used_for_de": StringToList.string(category_query.be_used_for_de),
                        "be_used_for_fr": StringToList.string(category_query.be_used_for_fr),
                        "be_used_for_es": StringToList.string(category_query.be_used_for_es),
                        "color_hu": StringToList.string(category_query.color_hu),
                        "color_en": StringToList.string(category_query.color_en),
                        "color_de": StringToList.string(category_query.color_de),
                        "color_fr": StringToList.string(category_query.color_fr),
                        "color_es": StringToList.string(category_query.color_es),
                        "visibility": category_query.visibility,
                        "img_data": category_query.img_data,
                        "img": category_query.img,
                        "created_at": str(category_query.created_at),
                        "updated_at": str(category_query.updated_at),
                    }
                    category_list.append(item)

                    data = {"data": sorted(category_list, key=lambda x: parse(x['updated_at']), reverse=True)}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class EditCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = edit_category.parse_args()

        email = data['email']
        category_id = data['category_id']
        visibility = data['visibility']
        name_hu = data['name_hu']
        name_en = data['name_en']
        name_de = data['name_de']
        name_fr = data['name_fr']
        name_es = data['name_es']
        gender_hu = data['gender_hu']
        gender_en = data['gender_en']
        gender_de = data['gender_de']
        gender_fr = data['gender_fr']
        gender_es = data['gender_es']
        be_used_for_hu = data['be_used_for_hu']
        be_used_for_en = data['be_used_for_en']
        be_used_for_de = data['be_used_for_de']
        be_used_for_fr = data['be_used_for_fr']
        be_used_for_es = data['be_used_for_es']
        color_hu = data['color_hu']
        color_en = data['color_en']
        color_de = data['color_de']
        color_fr = data['color_fr']
        color_es = data['color_es']
        img_data = data['img_data']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.add_category(name_hu, name_en, name_de, name_fr, name_es)
                if validation['status'] == "success":
                    user = User.query.filter_by(email=email).first()

                    if user is not None:
                        user_profile = UserProfile \
                            .query.join(User.profile) \
                            .filter(User.id == user.id).first()

                        if img_data:
                            category_photo_data = json.loads(img_data)
                            category_photo = category_photo_data['filename']
                        else:
                            img_data = None
                            category_photo = None

                        category_payload = Category.query.filter_by(id=category_id).first()

                        category_payload.category_user_id = user.id
                        category_payload.category_user_name = user_profile.username
                        category_payload.name_hu = name_hu
                        category_payload.name_en = name_en
                        category_payload.name_de = name_de
                        category_payload.name_fr = name_fr
                        category_payload.name_es = name_es
                        category_payload.gender_hu = StringToList.list(gender_hu)
                        category_payload.gender_en = StringToList.list(gender_en)
                        category_payload.gender_de = StringToList.list(gender_de)
                        category_payload.gender_fr = StringToList.list(gender_fr)
                        category_payload.gender_es = StringToList.list(gender_es)
                        category_payload.be_used_for_hu = StringToList.list(be_used_for_hu)
                        category_payload.be_used_for_en = StringToList.list(be_used_for_en)
                        category_payload.be_used_for_de = StringToList.list(be_used_for_de)
                        category_payload.be_used_for_fr = StringToList.list(be_used_for_fr)
                        category_payload.be_used_for_es = StringToList.list(be_used_for_es)
                        category_payload.color_hu = StringToList.list(color_hu)
                        category_payload.color_en = StringToList.list(color_en)
                        category_payload.color_de = StringToList.list(color_de)
                        category_payload.color_fr = StringToList.list(color_fr)
                        category_payload.color_es = StringToList.list(color_es)
                        category_payload.img_data = img_data
                        category_payload.img = category_photo
                        category_payload.visibility = visibility

                        category_payload.db_post()

                        data = {"status": 'success'}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class DeleteCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = delete_category.parse_args()

        email = data['email']
        category_id = data['category_id']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                if user is not None:
                    category_payload = Category.query.filter_by(id=category_id).first()
                    category_payload.db_delete()

                    data = {"status": 'success'}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetCategoryToSubcategories(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_category_to_subcategories.parse_args()

        category_id = int(data['category_id'])

        if api_key == app.config['API_KEY']:
            try:
                category_query = Category.query.filter_by(id=category_id).first()

                subcategory_query = SubCategory \
                    .query.join(Category.sub_category) \
                    .filter(Category.id == category_query.id).all()
                subcategory_list = []

                for subcategory_data in subcategory_query:
                    item = {
                        "subcategory_id": subcategory_data.id,
                        "category_id": subcategory_data.category_id,
                        "category_user_id": subcategory_data.category_user_id,
                        "category_user_name": subcategory_data.category_user_name,
                        "name_hu": subcategory_data.name_hu,
                        "name_en": subcategory_data.name_en,
                        "name_de": subcategory_data.name_de,
                        "name_fr": subcategory_data.name_fr,
                        "name_es": subcategory_data.name_es,
                        "description_hu": subcategory_data.description_hu,
                        "description_en": subcategory_data.description_en,
                        "description_de": subcategory_data.description_de,
                        "description_fr": subcategory_data.description_fr,
                        "description_es": subcategory_data.description_es,
                        "visibility": subcategory_data.visibility,
                        "img_data": subcategory_data.img_data,
                        "img": subcategory_data.img,
                        "created_at": str(subcategory_data.created_at),
                        "updated_at": str(subcategory_data.updated_at),
                    }
                    subcategory_list.append(item)

                data = {"data": sorted(subcategory_list, key=lambda x: parse(x['updated_at']), reverse=True)}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(AddCategory, '/add-category')
api.add_resource(GetCategoryAll, '/get-category-all')
api.add_resource(GetCategory, '/get-category')
api.add_resource(EditCategory, '/edit-category')
api.add_resource(DeleteCategory, '/delete-category')
api.add_resource(GetCategoryToSubcategories, '/get-category-to-subcategories')

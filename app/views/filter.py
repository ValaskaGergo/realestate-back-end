# -*- coding: utf-8 -*-
from app import app
from config import _basedir
from flask import Blueprint, request, make_response, jsonify, json
from flask_restful import Api, Resource, reqparse
from app.models.models import Category, SubCategory, Animal, Rating, User, Wishlist, Questions, Talking, \
    UserBillingInformation
from pyjsonq import JsonQ
from .utilities.utility import StringToList
from dateutil.parser import parse
from sqlalchemy import or_, and_, desc, asc, func, cast, String
from .utilities.utility import EncodedJWT, DecodeJWT
import itertools
from .utilities.utility import Pagination
import math
from slugify import slugify
import io

mod = Blueprint('filter_module', __name__)
api = Api(mod)

get_filter_category_all = reqparse.RequestParser()
get_filter_category_all.add_argument('lang', required=True)

get_category_subcategory_all = reqparse.RequestParser()
get_category_subcategory_all.add_argument('lang', required=True)

get_filter_category = reqparse.RequestParser()
get_filter_category.add_argument('category_id', required=True)
get_filter_category.add_argument('lang', required=True)

get_filter_count = reqparse.RequestParser()
get_filter_count.add_argument('lang')
get_filter_count.add_argument('where_input')
get_filter_count.add_argument('where_all')
get_filter_count.add_argument('where_name')
get_filter_count.add_argument('where_description')
get_filter_count.add_argument('price_min')
get_filter_count.add_argument('price_max')
get_filter_count.add_argument('category_all')
get_filter_count.add_argument('subcategory_all')
get_filter_count.add_argument('gender_all')
get_filter_count.add_argument('color_all')
get_filter_count.add_argument('be_used_for_all')
get_filter_count.add_argument('region_residence')
get_filter_count.add_argument('country_residence')
get_filter_count.add_argument('seller_user_id')
get_filter_count.add_argument('seller_user_name')
get_filter_count.add_argument('wishlist')

get_filter_data = reqparse.RequestParser()
get_filter_data.add_argument('encode')
get_filter_data.add_argument('page_number')
get_filter_data.add_argument('snap')
get_filter_data.add_argument('customer_user_id')


class GetFilterCategoryAll(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_filter_category_all.parse_args()

        lang = data['lang']

        if api_key == app.config['API_KEY']:
            try:
                category_query = Category.query.filter_by(visibility="True").all()
                if category_query is not None:
                    category_list_all = []

                    for category in category_query:
                        item = {
                            "id": category.id,
                            "name_hu": category.name_hu,
                            "name_en": category.name_en,
                            "name_de": category.name_de,
                            "name_fr": category.name_fr,
                            "name_es": category.name_es,
                            "lang": lang
                        }
                        category_list_all.append(item)

                    try:
                        jq = JsonQ(data=category_list_all)
                        if lang == "hu":
                            category_list_all = jq.sort_by("name_hu", "asc").get()
                        if lang == "en":
                            category_list_all = jq.sort_by("name_en", "asc").get()
                        if lang == "de":
                            category_list_all = jq.sort_by("name_de", "asc").get()
                        if lang == "fr":
                            category_list_all = jq.sort_by("name_fr", "asc").get()
                        if lang == "es":
                            category_list_all = jq.sort_by("name_es", "asc").get()
                    except AttributeError:
                        pass

                    data = {"status": "success", "category_list_all": category_list_all}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(), 404)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetCategorySubcategoryAll(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_category_subcategory_all.parse_args()

        lang = data['lang']

        if api_key == app.config['API_KEY']:
            try:
                category_query = Category.query.filter_by(visibility="True").all()
                if category_query is not None:
                    category_list_all = []
                    subcategory_list_all = []

                    for category in category_query:
                        animal_query = Animal.query.filter(Animal.category_id == category.id).first()
                        if animal_query is not None:
                            item = {
                                "id": category.id,
                                "name_hu": category.name_hu,
                                "name_en": category.name_en,
                                "name_en_slug": slugify(category.name_en),
                                "name_de": category.name_de,
                                "name_fr": category.name_fr,
                                "name_es": category.name_es,
                                "lang": lang
                            }
                            category_list_all.append(item)

                        try:
                            jq = JsonQ(data=category_list_all)
                            if lang == "hu":
                                category_list_all = jq.sort_by("name_hu", "asc").get()
                            if lang == "en":
                                category_list_all = jq.sort_by("name_en", "asc").get()
                            if lang == "de":
                                category_list_all = jq.sort_by("name_de", "asc").get()
                            if lang == "fr":
                                category_list_all = jq.sort_by("name_fr", "asc").get()
                            if lang == "es":
                                category_list_all = jq.sort_by("name_es", "asc").get()
                        except AttributeError:
                            pass

                    subcategory_query = SubCategory.query.filter_by(visibility="True").all()
                    if subcategory_query is not None:

                        for subcategory in subcategory_query:
                            item = {
                                "category_id": subcategory.category_id,
                                "id": subcategory.id,
                                "name_hu": subcategory.name_hu,
                                "name_en": subcategory.name_en,
                                "name_en_slug": slugify(subcategory.name_en),
                                "name_de": subcategory.name_de,
                                "name_fr": subcategory.name_fr,
                                "name_es": subcategory.name_es,
                                "lang": lang
                            }
                            subcategory_list_all.append(item)

                        try:
                            jq = JsonQ(data=subcategory_list_all)
                            if lang == "hu":
                                subcategory_list_all = jq.sort_by("name_hu", "asc").get()
                            if lang == "en":
                                subcategory_list_all = jq.sort_by("name_en", "asc").get()
                            if lang == "de":
                                subcategory_list_all = jq.sort_by("name_de", "asc").get()
                            if lang == "fr":
                                subcategory_list_all = jq.sort_by("name_fr", "asc").get()
                            if lang == "es":
                                subcategory_list_all = jq.sort_by("name_es", "asc").get()
                        except AttributeError:
                            pass

                    data = {
                        "status": "success",
                        "category_list_all": category_list_all,
                        "subcategory_list_all": subcategory_list_all
                    }
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(), 404)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetFilterCategory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_filter_category.parse_args()

        category_id = StringToList.string(data['category_id'])
        lang = data['lang']

        if api_key == app.config['API_KEY']:
            try:
                category_query = Category.query.filter_by(visibility="True").filter_by(id=category_id).all()
                subcategory_query = SubCategory.query.filter_by(visibility="True").filter_by(
                    category_id=category_id).all()

                category_name = []
                category_gender = []
                category_be_used_for = []
                category_color = []

                subcategory_list_all = []

                if category_query is not None:

                    for category in category_query:
                        category_name_item = {
                            "id": category.id,
                            "name_hu": category.name_hu,
                            "name_en": category.name_en,
                            "name_de": category.name_de,
                            "name_fr": category.name_fr,
                            "name_es": category.name_es,
                            "lang": lang
                        }
                        category_name.append(category_name_item)

                        category_gender_item = {
                            "id": category.id,
                            "gender_hu": category.gender_hu,
                            "gender_en": category.gender_en,
                            "gender_de": category.gender_de,
                            "gender_fr": category.gender_fr,
                            "gender_es": category.gender_es,
                            "gender_sort": "",
                            "lang": lang
                        }
                        category_gender.append(category_gender_item)

                        category_be_used_for_item = {
                            "id": category.id,
                            "be_used_for_hu": category.be_used_for_hu,
                            "be_used_for_en": category.be_used_for_en,
                            "be_used_for_de": category.be_used_for_de,
                            "be_used_for_fr": category.be_used_for_fr,
                            "be_used_for_es": category.be_used_for_es,
                            "be_used_for_sort": "",
                            "lang": lang
                        }
                        category_be_used_for.append(category_be_used_for_item)

                        category_color_item = {
                            "id": category.id,
                            "color_hu": category.color_hu,
                            "color_en": category.color_en,
                            "color_de": category.color_de,
                            "color_fr": category.color_fr,
                            "color_es": category.color_es,
                            "color_sort": "",
                            "lang": lang
                        }
                        category_color.append(category_color_item)

                    try:
                        category_name_jq = JsonQ(data=category_name)
                        if lang == "hu":
                            # Category Name
                            category_name = category_name_jq.sort_by("name_hu", "asc").get()

                            # Category Gender
                            category_gender_sort = StringToList.string(category_gender[0]['gender_hu']).split(', ')
                            category_gender_sort.sort(reverse=False)
                            category_gender[0]['gender_sort'] = category_gender_sort

                            # Category Be used For
                            category_be_used_for_sort = StringToList.string(
                                category_be_used_for[0]['be_used_for_hu']).split(', ')
                            category_be_used_for_sort.sort(reverse=False)
                            category_be_used_for[0]['be_used_for_sort'] = category_be_used_for_sort

                            # Category Color
                            category_color_sort = StringToList.string(
                                category_color[0]['color_hu']).split(', ')
                            category_color_sort.sort(reverse=False)
                            category_color[0]['color_sort'] = category_color_sort
                        if lang == "en":
                            # Category Name
                            category_name = category_name_jq.sort_by("name_en", "asc").get()

                            # Category Gender
                            category_gender_sort = StringToList.string(category_gender[0]['gender_en']).split(', ')
                            category_gender_sort.sort(reverse=False)
                            category_gender[0]['gender_sort'] = category_gender_sort

                            # Category Be used For
                            category_be_used_for_sort = StringToList.string(
                                category_be_used_for[0]['be_used_for_en']).split(', ')
                            category_be_used_for_sort.sort(reverse=False)
                            category_be_used_for[0]['be_used_for_sort'] = category_be_used_for_sort

                            # Category Color
                            category_color_sort = StringToList.string(
                                category_color[0]['color_en']).split(', ')
                            category_color_sort.sort(reverse=False)
                            category_color[0]['color_sort'] = category_color_sort
                        if lang == "de":
                            # Category Name
                            category_name = category_name_jq.sort_by("name_de", "asc").get()

                            # Category Gender
                            category_gender_sort = StringToList.string(category_gender[0]['gender_de']).split(', ')
                            category_gender_sort.sort(reverse=False)
                            category_gender[0]['gender_sort'] = category_gender_sort

                            # Category Be used For
                            category_be_used_for_sort = StringToList.string(
                                category_be_used_for[0]['be_used_for_de']).split(', ')
                            category_be_used_for_sort.sort(reverse=False)
                            category_be_used_for[0]['be_used_for_sort'] = category_be_used_for_sort

                            # Category Color
                            category_color_sort = StringToList.string(
                                category_color[0]['color_de']).split(', ')
                            category_color_sort.sort(reverse=False)
                            category_color[0]['color_sort'] = category_color_sort
                        if lang == "fr":
                            # Category Name
                            category_name = category_name_jq.sort_by("name_fr", "asc").get()

                            # Category Gender
                            category_gender_sort = StringToList.string(category_gender[0]['gender_fr']).split(', ')
                            category_gender_sort.sort(reverse=False)
                            category_gender[0]['gender_sort'] = category_gender_sort

                            # Category Be used For
                            category_be_used_for_sort = StringToList.string(
                                category_be_used_for[0]['be_used_for_fr']).split(', ')
                            category_be_used_for_sort.sort(reverse=False)
                            category_be_used_for[0]['be_used_for_sort'] = category_be_used_for_sort

                            # Category Color
                            category_color_sort = StringToList.string(
                                category_color[0]['color_fr']).split(', ')
                            category_color_sort.sort(reverse=False)
                            category_color[0]['color_sort'] = category_color_sort
                        if lang == "es":
                            # Category Name
                            category_name = category_name_jq.sort_by("name_es", "asc").get()

                            # Category Gender
                            category_gender_sort = StringToList.string(category_gender[0]['gender_es']).split(', ')
                            category_gender_sort.sort(reverse=False)
                            category_gender[0]['gender_sort'] = category_gender_sort

                            # Category Be used For
                            category_be_used_for_sort = StringToList.string(
                                category_be_used_for[0]['be_used_for_es']).split(', ')
                            category_be_used_for_sort.sort(reverse=False)
                            category_be_used_for[0]['be_used_for_sort'] = category_be_used_for_sort

                            # Category Color
                            category_color_sort = StringToList.string(
                                category_color[0]['color_es']).split(', ')
                            category_color_sort.sort(reverse=False)
                            category_color[0]['color_sort'] = category_color_sort
                    except AttributeError:
                        pass
                else:
                    return make_response(jsonify(), 404)

                if subcategory_query is not None:
                    for subcategory in subcategory_query:
                        item = {
                            "id": subcategory.id,
                            "name_hu": subcategory.name_hu,
                            "name_en": subcategory.name_en,
                            "name_de": subcategory.name_de,
                            "name_fr": subcategory.name_fr,
                            "name_es": subcategory.name_es,
                            "lang": lang
                        }
                        subcategory_list_all.append(item)

                    try:
                        jq = JsonQ(data=subcategory_list_all)
                        if lang == "hu":
                            subcategory_list_all = jq.sort_by("name_hu", "asc").get()
                        if lang == "en":
                            subcategory_list_all = jq.sort_by("name_en", "asc").get()
                        if lang == "de":
                            subcategory_list_all = jq.sort_by("name_de", "asc").get()
                        if lang == "fr":
                            subcategory_list_all = jq.sort_by("name_fr", "asc").get()
                        if lang == "es":
                            subcategory_list_all = jq.sort_by("name_es", "asc").get()
                    except AttributeError:
                        pass
                data = {"status": "success",
                        "category_name": category_name,
                        "category_gender": category_gender,
                        "category_be_used_for": category_be_used_for,
                        "category_color": category_color,
                        "subcategory_list_all": subcategory_list_all}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetFilterCount(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_filter_count.parse_args()

        lang = data['lang']

        where_input = data['where_input'].lstrip()
        where_all = data['where_all']  # active or inactive
        where_name = data['where_name']  # active or inactive
        where_description = data['where_description']  # active or inactive

        price_min = int(data['price_min'])
        price_max = int(data['price_max'])

        category_all = data['category_all']

        subcategory_all = data['subcategory_all']

        gender_all = data['gender_all']

        color_all = data['color_all']

        be_used_for_all = data['be_used_for_all']


        region_residence = data['region_residence']
        country_residence = data['country_residence']


        seller_user_id = data['seller_user_id']
        seller_user_name = data['seller_user_name']

        wishlist = data['wishlist']

        filters_and = []
        filters_or = []

        filters_like_or = []
        filters_like_and = []

        filters_price_or = []
        filters_price_and = []

        filters_category_or = []
        filters_category_and = []

        filters_subcategory_or = []
        filters_subcategory_and = []

        filters_gender_or = []
        filters_gender_and = []

        filters_color_or = []
        filters_color_and = []

        filters_beusedfor_or = []
        filters_beusedfor_and = []

        filters_age_or = []
        filters_age_and = []

        filters_country_or = []
        filters_country_and = []

        if api_key == app.config['API_KEY']:
            try:
                #  Start User List
                if seller_user_id != "None":
                    filters_and.append(Animal.user_id == seller_user_id)
                    try:
                        seller_query = User.query.filter(User.id == seller_user_id).first()
                        for seller in itertools.product(seller_query.billing_information):
                            for seller_user in seller:
                                seller_user_name = seller_user.last_name
                    except AttributeError:
                        pass
                #  End User List

                #  Start Wishlist
                if wishlist != "None":
                    wishlist_animal_list = []
                    wishlist_query = Wishlist.query.filter(Wishlist.user_id == wishlist).all()
                    for wishlist_animal in wishlist_query:
                        wishlist_animal_list.append(wishlist_animal.animal_id)
                    filters_and.append(Animal.id.in_(wishlist_animal_list))
                    is_wishlist = True
                else:
                    is_wishlist = False
                #  End Wishlist

                #  Start Visibility
                filters_and.append(Animal.visibility == "True")
                filters_and.append(Animal.worker_visibility == "True")
                #  End Visibility

                #  Start Not Deleted
                filters_and.append(Animal.deleted != True)
                #  End Not Deleted

                #  Start Search Input
                where_input_result = bool(where_input and where_input.strip())
                if where_input_result and len(where_input) >= 3:
                    if where_all == "active":
                        filters_like_or.append(Animal.name.ilike('%{}%'.format(where_input)))
                        filters_like_or.append(Animal.brief_description.ilike('%{}%'.format(where_input)))
                        filters_like_or.append(Animal.description.ilike('%{}%'.format(where_input)))
                        filters_like_or.append(
                            func.cast(Animal.advertisement_id, String).ilike('%{}%'.format(where_input)))
                    elif where_all == "inactive":
                        if where_name == "active":
                            filters_like_or.append(Animal.name.ilike('%{}%'.format(where_input)))
                        if where_description == "active":
                            filters_like_or.append(Animal.brief_description.ilike('%{}%'.format(where_input)))
                            filters_like_or.append(Animal.description.ilike('%{}%'.format(where_input)))

                #  End Search Input

                #  Start Price
                filters_price_and.append(Animal.price >= price_min)
                filters_price_and.append(Animal.price <= price_max)
                #  End Price

                #  Start Category
                category_all = json.loads(category_all)
                if len(category_all) > 1 and category_all.__contains__(0) is not True:
                    for category_id in category_all:
                        filters_category_or.append(Animal.category_id == category_id)
                elif len(category_all) == 1 and category_all.__contains__(0) is not True:
                    filters_category_or.append(Animal.category_id == category_all[0])

                    #  Start Subcategory
                    subcategory_all = json.loads(subcategory_all)
                    if len(subcategory_all) > 1 and subcategory_all.__contains__(0) is not True:
                        for subcategory_id in subcategory_all:
                            filters_subcategory_or.append(Animal.subcategory_id == subcategory_id)
                    elif len(subcategory_all) == 1 and subcategory_all.__contains__(0) is not True:
                        filters_subcategory_or.append(Animal.subcategory_id == subcategory_all[0])
                    #  End Subcategory

                    #  Start Gender
                    gender_all = json.loads(gender_all)
                    if len(gender_all) > 1 and gender_all.__contains__(0) is not True:
                        if lang == "hu":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_hu == gender)
                        if lang == "en":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_en == gender)
                        if lang == "de":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_de == gender)
                        if lang == "fr":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_fr == gender)
                        if lang == "es":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_es == gender)
                    elif len(gender_all) == 1 and gender_all.__contains__(0) is not True:
                        if lang == "hu":
                            filters_gender_or.append(Animal.gender_hu == gender_all[0])
                        if lang == "en":
                            filters_gender_or.append(Animal.gender_en == gender_all[0])
                        if lang == "de":
                            filters_gender_or.append(Animal.gender_de == gender_all[0])
                        if lang == "fr":
                            filters_gender_or.append(Animal.gender_fr == gender_all[0])
                        if lang == "es":
                            filters_gender_or.append(Animal.gender_es == gender_all[0])
                    #  End Gender

                    #  Start Color
                    color_all = json.loads(color_all)
                    if len(color_all) > 1 and color_all.__contains__(0) is not True:
                        if lang == "hu":
                            for color in color_all:
                                filters_color_or.append(Animal.color_hu == color)
                        if lang == "en":
                            for color in color_all:
                                filters_color_or.append(Animal.color_en == color)
                        if lang == "de":
                            for color in color_all:
                                filters_color_or.append(Animal.color_de == color)
                        if lang == "fr":
                            for color in color_all:
                                filters_color_or.append(Animal.color_fr == color)
                        if lang == "es":
                            for color in color_all:
                                filters_color_or.append(Animal.color_es == color)
                    elif len(color_all) == 1 and color_all.__contains__(0) is not True:
                        if lang == "hu":
                            filters_color_or.append(Animal.color_hu == color_all[0])
                        if lang == "en":
                            filters_color_or.append(Animal.color_en == color_all[0])
                        if lang == "de":
                            filters_color_or.append(Animal.color_de == color_all[0])
                        if lang == "fr":
                            filters_color_or.append(Animal.color_fr == color_all[0])
                        if lang == "es":
                            filters_color_or.append(Animal.color_es == color_all[0])
                    #  End Color

                    #  Start Be Used For
                    be_used_for_all = json.loads(be_used_for_all)
                    if len(be_used_for_all) > 1 and be_used_for_all.__contains__(0) is not True:
                        if lang == "hu":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_hu.ilike('%{}%'.format(beusedfor)))
                        if lang == "en":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_en.ilike('%{}%'.format(beusedfor)))
                        if lang == "de":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_de.ilike('%{}%'.format(beusedfor)))
                        if lang == "fr":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_fr.ilike('%{}%'.format(beusedfor)))
                        if lang == "es":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_es.ilike('%{}%'.format(beusedfor)))
                    elif len(be_used_for_all) == 1 and be_used_for_all.__contains__(0) is not True:
                        if lang == "hu":
                            filters_beusedfor_or.append(Animal.be_used_for_hu.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "en":
                            filters_beusedfor_or.append(Animal.be_used_for_en.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "de":
                            filters_beusedfor_or.append(Animal.be_used_for_de.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "fr":
                            filters_beusedfor_or.append(Animal.be_used_for_fr.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "es":
                            filters_beusedfor_or.append(Animal.be_used_for_es.ilike('%{}%'.format(be_used_for_all[0])))
                    #  End Be used For

                    #  Start Age
                    filters_age_and.append(Animal.years >= age_min)
                    filters_age_and.append(Animal.years <= age_max)
                    #  End Age

                #  End Category

                #  Start Country Residence
                if region_residence != "ALL":
                    filters_country_and.append(Animal.region_residence == region_residence)
                    if country_residence != "ALL":
                        filters_country_and.append(Animal.country_residence == country_residence)
                #  End Country Residence


                animal_query_count = Animal.query \
                    .filter(or_(*filters_like_or)) \
                    .filter(and_(*filters_price_and)) \
                    .filter(or_(*filters_category_or)) \
                    .filter(or_(*filters_subcategory_or)) \
                    .filter(or_(*filters_gender_or)) \
                    .filter(or_(*filters_color_or)) \
                    .filter(or_(*filters_beusedfor_or)) \
                    .filter(and_(*filters_and)) \
                    .filter(or_(*filters_or)) \
                    .count()

                if animal_query_count is not None:
                    data = {"status": "success", "count": animal_query_count}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(), 404)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetFilterData(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_filter_data.parse_args()

        encode = data['encode']
        decode = DecodeJWT.decode(encode)

        try:
            snap = data['snap']
        except KeyError:
            snap = decode['snap']
        except:
            snap = "None"

        page_number = int(data['page_number'])

        animals_limit = 26
        if snap == "None" or snap is None:
            animals_limit = 5
        elif snap == "True":
            if page_number == 1:
                animals_limit = 5
            else:
                animals_limit = 5
        else:
            pass
        offset_number = (page_number * animals_limit) - animals_limit

        lang = decode['lang']

        where_input = decode['where_input'].lstrip()
        where_all = decode['where_all']  # active or inactive
        where_name = decode['where_name']  # active or inactive
        where_description = decode['where_description']  # active or inactive

        price_min = int(decode['price_min'])
        price_max = int(decode['price_max'])

        category_all = decode['category_all']

        subcategory_all = decode['subcategory_all']

        gender_all = decode['gender_all']

        color_all = decode['color_all']

        be_used_for_all = decode['be_used_for_all']



        region_residence = decode['region_residence']
        country_residence = decode['country_residence']


        order_by_price = decode['order_by_price']

        order_by_rating = decode['order_by_rating']

        only_one_category_id = decode['only_one_category_id']
        only_one_category_name = None
        only_one_category_name_slug = None
        only_one_subcategory_id = decode['only_one_subcategory_id']
        only_one_subcategory_name = None

        seller_user_id = decode['seller_user_id']
        seller_user_name = decode['seller_user_name']
        seller_user_name_slug = None

        wishlist = decode['wishlist']

        customer_user_id = data['customer_user_id']

        filters_and = []
        filters_or = []

        filters_like_or = []
        filters_like_and = []

        filters_price_or = []
        filters_price_and = []

        filters_category_or = []
        filters_category_and = []

        filters_subcategory_or = []
        filters_subcategory_and = []

        filters_gender_or = []
        filters_gender_and = []

        filters_color_or = []
        filters_color_and = []

        filters_beusedfor_or = []
        filters_beusedfor_and = []

        filters_age_or = []
        filters_age_and = []

        filters_country_or = []
        filters_country_and = []

        filters_order_by = []

        if api_key == app.config['API_KEY']:
            try:
                #  Start User List
                if seller_user_id != "None":
                    filters_and.append(Animal.user_id == seller_user_id)
                    try:
                        seller_query = User.query.filter(User.id == seller_user_id).first()
                        for seller in itertools.product(seller_query.billing_information):
                            for seller_user in seller:
                                seller_user_name = seller_user.last_name
                                seller_user_name_slug = slugify(seller_user.last_name)
                    except AttributeError:
                        pass
                #  End User List

                #  Start Wishlist
                if wishlist != "None":
                    wishlist_animal_list = []
                    wishlist_query = Wishlist.query.filter(Wishlist.user_id == wishlist).all()
                    for wishlist_animal in wishlist_query:
                        wishlist_animal_list.append(wishlist_animal.animal_id)
                    filters_and.append(Animal.id.in_(wishlist_animal_list))
                    is_wishlist = True
                else:
                    is_wishlist = False
                #  End Wishlist

                #  Start Visibility
                filters_and.append(Animal.visibility == "True")
                filters_and.append(Animal.worker_visibility == "True")
                #  End Visibility

                #  Start Deleted
                filters_and.append(Animal.deleted != True)
                #  End Deleted

                #  Start Search Input
                where_input_result = bool(where_input and where_input.strip())
                if where_input_result and len(where_input) >= 3:
                    if where_all == "active":
                        filters_like_or.append(Animal.name.ilike('%{}%'.format(where_input)))
                        filters_like_or.append(Animal.brief_description.ilike('%{}%'.format(where_input)))
                        filters_like_or.append(Animal.description.ilike('%{}%'.format(where_input)))
                        filters_like_or.append(
                            func.cast(Animal.advertisement_id, String).ilike('%{}%'.format(where_input)))
                    elif where_all == "inactive":
                        if where_name == "active":
                            filters_like_or.append(Animal.name.ilike('%{}%'.format(where_input)))
                        if where_description == "active":
                            filters_like_or.append(Animal.brief_description.ilike('%{}%'.format(where_input)))
                            filters_like_or.append(Animal.description.ilike('%{}%'.format(where_input)))

                #  End Search Input

                #  Start Price
                filters_price_and.append(Animal.price >= price_min)
                filters_price_and.append(Animal.price <= price_max)
                #  End Price

                #  Start Category
                category_all = json.loads(category_all)
                if len(category_all) > 1 and category_all.__contains__(0) is not True:
                    for category_id in category_all:
                        filters_category_or.append(Animal.category_id == category_id)
                elif len(category_all) == 1 and category_all.__contains__(0) is not True:
                    filters_category_or.append(Animal.category_id == category_all[0])

                    #  Start Subcategory
                    subcategory_all = json.loads(subcategory_all)
                    if len(subcategory_all) > 1 and subcategory_all.__contains__(0) is not True:
                        for subcategory_id in subcategory_all:
                            filters_subcategory_or.append(Animal.subcategory_id == subcategory_id)
                    elif len(subcategory_all) == 1 and subcategory_all.__contains__(0) is not True:
                        filters_subcategory_or.append(Animal.subcategory_id == subcategory_all[0])
                    #  End Subcategory

                    #  Start Gender
                    gender_all = json.loads(gender_all)
                    if len(gender_all) > 1 and gender_all.__contains__(0) is not True:
                        if lang == "hu":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_hu == gender)
                        if lang == "en":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_en == gender)
                        if lang == "de":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_de == gender)
                        if lang == "fr":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_fr == gender)
                        if lang == "es":
                            for gender in gender_all:
                                filters_gender_or.append(Animal.gender_es == gender)
                    elif len(gender_all) == 1 and gender_all.__contains__(0) is not True:
                        if lang == "hu":
                            filters_gender_or.append(Animal.gender_hu == gender_all[0])
                        if lang == "en":
                            filters_gender_or.append(Animal.gender_en == gender_all[0])
                        if lang == "de":
                            filters_gender_or.append(Animal.gender_de == gender_all[0])
                        if lang == "fr":
                            filters_gender_or.append(Animal.gender_fr == gender_all[0])
                        if lang == "es":
                            filters_gender_or.append(Animal.gender_es == gender_all[0])
                    #  End Gender

                    #  Start Color
                    color_all = json.loads(color_all)
                    if len(color_all) > 1 and color_all.__contains__(0) is not True:
                        if lang == "hu":
                            for color in color_all:
                                filters_color_or.append(Animal.color_hu == color)
                        if lang == "en":
                            for color in color_all:
                                filters_color_or.append(Animal.color_en == color)
                        if lang == "de":
                            for color in color_all:
                                filters_color_or.append(Animal.color_de == color)
                        if lang == "fr":
                            for color in color_all:
                                filters_color_or.append(Animal.color_fr == color)
                        if lang == "es":
                            for color in color_all:
                                filters_color_or.append(Animal.color_es == color)
                    elif len(color_all) == 1 and color_all.__contains__(0) is not True:
                        if lang == "hu":
                            filters_color_or.append(Animal.color_hu == color_all[0])
                        if lang == "en":
                            filters_color_or.append(Animal.color_en == color_all[0])
                        if lang == "de":
                            filters_color_or.append(Animal.color_de == color_all[0])
                        if lang == "fr":
                            filters_color_or.append(Animal.color_fr == color_all[0])
                        if lang == "es":
                            filters_color_or.append(Animal.color_es == color_all[0])
                    #  End Color

                    #  Start Be Used For
                    be_used_for_all = json.loads(be_used_for_all)
                    if len(be_used_for_all) > 1 and be_used_for_all.__contains__(0) is not True:
                        if lang == "hu":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_hu.ilike('%{}%'.format(beusedfor)))
                        if lang == "en":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_en.ilike('%{}%'.format(beusedfor)))
                        if lang == "de":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_de.ilike('%{}%'.format(beusedfor)))
                        if lang == "fr":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_fr.ilike('%{}%'.format(beusedfor)))
                        if lang == "es":
                            for beusedfor in be_used_for_all:
                                filters_beusedfor_or.append(Animal.be_used_for_es.ilike('%{}%'.format(beusedfor)))
                    elif len(be_used_for_all) == 1 and be_used_for_all.__contains__(0) is not True:
                        if lang == "hu":
                            filters_beusedfor_or.append(Animal.be_used_for_hu.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "en":
                            filters_beusedfor_or.append(Animal.be_used_for_en.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "de":
                            filters_beusedfor_or.append(Animal.be_used_for_de.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "fr":
                            filters_beusedfor_or.append(Animal.be_used_for_fr.ilike('%{}%'.format(be_used_for_all[0])))
                        if lang == "es":
                            filters_beusedfor_or.append(Animal.be_used_for_es.ilike('%{}%'.format(be_used_for_all[0])))
                    #  End Be used For

                    #  Start Age
                    filters_age_and.append(Animal.years >= age_min)
                    filters_age_and.append(Animal.years <= age_max)
                    #  End Age

                #  End Category

                #  Start Country Residence
                if region_residence != "ALL":
                    filters_country_and.append(Animal.region_residence == region_residence)
                    if country_residence != "ALL":
                        filters_country_and.append(Animal.country_residence == country_residence)
                #  End Country Residence


                #  Start Order By
                if order_by_price != "None":
                    if order_by_price == "asc":
                        filters_order_by.append(asc(Animal.price))
                        filters_order_by.append(desc(Animal.created_at))
                    elif order_by_price == "desc":
                        filters_order_by.append(desc(Animal.price))
                        filters_order_by.append(desc(Animal.created_at))

                elif order_by_rating != "None":
                    if order_by_rating == "asc":
                        filters_order_by.append(asc(Animal.rating))
                        filters_order_by.append(desc(Animal.created_at))
                    elif order_by_rating == "desc":
                        filters_order_by.append(desc(Animal.rating))
                        filters_order_by.append(desc(Animal.created_at))

                #  End Order By

                animal_query = Animal.query \
                    .filter(or_(*filters_like_or)) \
                    .filter(and_(*filters_price_and)) \
                    .filter(or_(*filters_category_or)) \
                    .filter(or_(*filters_subcategory_or)) \
                    .filter(or_(*filters_gender_or)) \
                    .filter(or_(*filters_color_or)) \
                    .filter(or_(*filters_beusedfor_or)) \
                    .filter(and_(*filters_and)) \
                    .filter(or_(*filters_or)) \
                    .order_by(*filters_order_by) \
                    .offset(offset_number) \
                    .limit(animals_limit) \
                    .all()

                if animal_query is not None:
                    animals_list = []

                    for animal in animal_query:
                        category_query = Category.query.filter(Category.id == animal.category_id).first()
                        subcategory_query = SubCategory.query.filter(SubCategory.id == animal.subcategory_id).first()
                        for photos, videos, pdf in itertools.product(animal.photos, animal.videos, animal.pdf):

                            #  Start Rating
                            rating_query = Rating.query.filter_by(animal_id=animal.id).all()

                            if len(rating_query):
                                rating_count_all = Rating.query.filter(Rating.animal_id == animal.id).count()
                                rating_count_one = Rating.query \
                                    .filter(Rating.animal_id == animal.id) \
                                    .filter(Rating.rating == 1).count()
                                rating_count_two = Rating.query \
                                    .filter(Rating.animal_id == animal.id) \
                                    .filter(Rating.rating == 2).count()
                                rating_count_three = Rating.query \
                                    .filter(Rating.animal_id == animal.id) \
                                    .filter(Rating.rating == 3).count()
                                rating_count_four = Rating.query \
                                    .filter(Rating.animal_id == animal.id) \
                                    .filter(Rating.rating == 4).count()
                                rating_count_five = Rating.query \
                                    .filter(Rating.animal_id == animal.id) \
                                    .filter(Rating.rating == 5).count()
                                for r in rating_query:
                                    pass
                            else:
                                rating_count_all = 0
                                rating_count_one = 0
                                rating_count_two = 0
                                rating_count_three = 0
                                rating_count_four = 0
                                rating_count_five = 0

                            try:
                                rating = (1 * rating_count_one +
                                          2 * rating_count_two +
                                          3 * rating_count_three +
                                          4 * rating_count_four +
                                          5 * rating_count_five) / (
                                                 rating_count_one + rating_count_two + rating_count_three +
                                                 rating_count_four + rating_count_five)
                            except ZeroDivisionError:
                                rating = 0
                            #  End Rating

                            # Start Snap Seller
                            snap_seller_id = animal.user_id
                            snap_seller_query = User.query.filter(User.id == snap_seller_id).first()

                            snap_seller_last_name = None
                            snap_seller_last_name_slug = None
                            for snap_billings in itertools.product(snap_seller_query.billing_information):
                                for snap_billing in snap_billings:
                                    snap_seller_last_name = snap_billing.last_name
                                    snap_seller_last_name_slug = slugify(snap_billing.last_name)
                            # End Snap Seller

                            # Start Questions Count
                            questions_count = Questions.query.filter(Questions.animal_id == animal.id).count()
                            # End Questions Count

                            # Start Talking Count
                            talking_count = Talking.query.filter(Talking.subcategory_id == subcategory_query.id).count()
                            # End Talking Count

                            # Start Price
                            if customer_user_id is not None:
                                exchange_json = io.open(_basedir + "/app/json/exchange.json", 'r')
                                exchange_json_read = json.loads(exchange_json.read())

                                customer_user_query = User.query.filter(User.id == customer_user_id).first()
                                price_exchange_currency = None
                                price_exchange = None
                                for customer_billing in itertools.product(customer_user_query.billing_information):
                                    for customer_billing_currency in customer_billing:
                                        if customer_billing_currency.currency is not None:
                                            customer_currency = customer_billing_currency.currency
                                            customer_currency = float(exchange_json_read['rates'][customer_currency])
                                            price_exchange_currency = customer_billing_currency.currency
                                            price_exchange = animal.price * customer_currency
                                            price_exchange = round(price_exchange)
                                        else:
                                            price_exchange_currency = None
                                            price_exchange = None
                            else:
                                price_exchange_currency = None
                                price_exchange = None
                            # End Price

                            item = {
                                "animal": {
                                    "id": animal.id,
                                    "category_id": animal.category_id,
                                    "subcategory_id": animal.subcategory_id,
                                    "name": animal.name,
                                    "region_residence": animal.region_residence,
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
                                    "price_exchange_currency": price_exchange_currency,
                                    "price_exchange": price_exchange,
                                    "visibility": animal.visibility,
                                    "worker_visibility": animal.worker_visibility,
                                    "created_at": animal.created_at,
                                    "updated_at": animal.updated_at
                                },
                                "photo": {
                                    "id": photos.id,
                                    "img_01": photos.img_01,
                                    "img_02": photos.img_02,
                                    "img_03": photos.img_03,
                                    "img_04": photos.img_04,
                                    "img_05": photos.img_05,
                                    "img_06": photos.img_06,
                                    "img_07": photos.img_07,
                                    "img_08": photos.img_08,
                                    "img_09": photos.img_09,
                                    "img_10": photos.img_10,
                                    "created_at": photos.created_at,
                                    "updated_at": photos.updated_at
                                },
                                "video": {
                                    "id": videos.id,
                                    "video_01": videos.video_01,
                                    "video_01_folder": videos.video_01.replace(".mp4", ""),
                                    "created_at": videos.created_at,
                                    "updated_at": videos.updated_at
                                },
                                "category": {
                                    "name_hu": category_query.name_hu,
                                    "name_en": category_query.name_en,
                                    "name_en_slug": slugify(category_query.name_en),
                                    "name_de": category_query.name_de,
                                    "name_fr": category_query.name_fr,
                                    "name_es": category_query.name_es,
                                },
                                "subcategory": {
                                    "name_hu": subcategory_query.name_hu,
                                    "name_en": subcategory_query.name_en,
                                    "name_en_slug": slugify(subcategory_query.name_en),
                                    "name_de": subcategory_query.name_de,
                                    "name_fr": subcategory_query.name_fr,
                                    "name_es": subcategory_query.name_es,
                                },
                                "pdf": {
                                    "id": pdf.id,
                                    "x_ray": pdf.x_ray
                                },
                                "rating": {
                                    "rating_count_all": rating_count_all,
                                    "rating_count_one": rating_count_one,
                                    "rating_count_two": rating_count_two,
                                    "rating_count_three": rating_count_three,
                                    "rating_count_four": rating_count_four,
                                    "rating_count_five": rating_count_five,
                                    "rating": round(rating, 1)
                                },
                                "seller": {
                                    "seller_user_id": seller_user_id,
                                    "seller_user_name": seller_user_name,
                                    "seller_user_name_slug": seller_user_name_slug
                                },
                                "wishlist": {
                                    "is_wishlist": is_wishlist
                                },
                                "snap": {
                                    "snap_seller_id": snap_seller_id,
                                    "snap_seller_last_name": snap_seller_last_name,
                                    "snap_seller_last_name_slug": snap_seller_last_name_slug
                                },
                                "questions": {
                                    "questions_count": questions_count
                                },
                                "talking": {
                                    "talking_count": talking_count
                                }
                            }
                            animals_list.append(item)

                    if only_one_category_id != None:
                        only_one_category_id_list = only_one_category_id.strip('][')
                    else:
                        only_one_category_id_list = []
                    if only_one_subcategory_id != None:
                        only_one_subcategory_id_list = only_one_subcategory_id.strip('][')
                    else:
                        only_one_subcategory_id_list = []

                    try:
                        if len(only_one_category_id_list) == 1 and only_one_category_id_list[0] != "0" and \
                                only_one_category_id_list[
                                    0] != "None":
                            cat = Category.query.filter(Category.id == only_one_category_id_list[0]).first()
                            if lang == "hu":
                                only_one_category_name = cat.name_hu
                            elif lang == "en":
                                only_one_category_name = cat.name_en
                            elif lang == "de":
                                only_one_category_name = cat.name_de
                            elif lang == "fr":
                                only_one_category_name = cat.name_fr
                            elif lang == "es":
                                only_one_category_name = cat.name_es
                            only_one_category_name_slug = slugify(cat.name_en)
                    except TypeError:
                        pass

                    try:
                        if len(only_one_subcategory_id_list) == 1 and only_one_subcategory_id_list[0] != "0" and \
                                only_one_subcategory_id_list[0] != "None":
                            subcat = SubCategory.query.filter(SubCategory.id == only_one_subcategory_id_list[0]).first()
                            if lang == "hu":
                                only_one_subcategory_name = subcat.name_hu
                            elif lang == "en":
                                only_one_subcategory_name = subcat.name_en
                            elif lang == "de":
                                only_one_subcategory_name = subcat.name_de
                            elif lang == "fr":
                                only_one_subcategory_name = subcat.name_fr
                            elif lang == "es":
                                only_one_subcategory_name = subcat.name_es
                    except TypeError:
                        pass

                    #  Start Pagination
                    animals_query_count = Animal.query \
                        .filter(or_(*filters_like_or)) \
                        .filter(and_(*filters_price_and)) \
                        .filter(or_(*filters_category_or)) \
                        .filter(or_(*filters_subcategory_or)) \
                        .filter(or_(*filters_gender_or)) \
                        .filter(or_(*filters_color_or)) \
                        .filter(or_(*filters_beusedfor_or)) \
                        .filter(and_(*filters_age_and)) \
                        .filter(and_(*filters_country_and)) \
                        .filter(and_(*filters_and)) \
                        .filter(or_(*filters_or)) \
                        .count()

                    pagination_count = math.ceil(animals_query_count / animals_limit)
                    pagination_first = 1
                    pagination_last = pagination_count
                    pagination_next = page_number + 1
                    pagination_previous = page_number - 1

                    try:
                        pagination_list = Pagination.create(int(pagination_count), int(page_number))
                    except:
                        pagination_list = [1]

                    pagination = {
                        "page_number": int(page_number),
                        "animals_limit": int(animals_limit),
                        "animals_count": int(animals_query_count),
                        "pagination_count": int(pagination_count),
                        "pagination_first": int(pagination_first),
                        "pagination_last": int(pagination_last),
                        "pagination_next": int(pagination_next),
                        "pagination_previous": int(pagination_previous)
                    }
                    #  End pagination

                    data = {"status": "success", "pagination_list": pagination_list, "pagination": pagination,
                            "animals_list": animals_list, "lang": lang, "only_one_category_id": only_one_category_id,
                            "only_one_category_name": only_one_category_name,
                            "only_one_subcategory_id": only_one_subcategory_id,
                            "only_one_subcategory_name": only_one_subcategory_name,
                            "only_one_category_name_slug": only_one_category_name_slug,
                            "wishlist": wishlist}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(), 404)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(GetFilterCategoryAll, '/get-filter-category-all')
api.add_resource(GetCategorySubcategoryAll, '/get-category-subcategory-all')
api.add_resource(GetFilterCategory, '/get-filter-category')
api.add_resource(GetFilterCount, '/get-filter-count')
api.add_resource(GetFilterData, '/get-filter-data')

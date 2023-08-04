# -*- coding: utf-8 -*-
from app import app
from config import _basedir
from flask import Blueprint, request, make_response, jsonify, json
from flask_restful import Api, Resource, reqparse
from app.models.models import Animal, Category, SubCategory, Rating, Questions, Answers, User, UserBillingInformation, \
    QuestionsHistory, Talking, Wishlist, Messages, UserProfile
import itertools
from slugify import slugify
from sqlalchemy import or_, and_, desc, asc, func
from .utilities.utility import CountryCodeToLangCode
import io
from .utilities.utility import VerificationCode

mod = Blueprint('full_page_module', __name__)
api = Api(mod)

full_page = reqparse.RequestParser()
full_page.add_argument('page_id', required=True)
full_page.add_argument('user_id')
full_page.add_argument('lang')

full_data_info_box = reqparse.RequestParser()
full_data_info_box.add_argument('animal_id', required=True)

wishlist_data = reqparse.RequestParser()
wishlist_data.add_argument('animal_id', required=True)
wishlist_data.add_argument('user_id', required=True)
wishlist_data.add_argument('wishlist_status', required=True)

alike_data = reqparse.RequestParser()
alike_data.add_argument('subcategory_id', required=True)
alike_data.add_argument('animal_id', required=True)
alike_data.add_argument('price_show')
alike_data.add_argument('customer_user_id')
alike_data.add_argument('lang')

user_to_user_message_data = reqparse.RequestParser()
user_to_user_message_data.add_argument('sender_id', required=True)
user_to_user_message_data.add_argument('host_id', required=True)


class FullPage(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = full_page.parse_args()

        page_id = data['page_id']
        user_id = data['user_id']
        lang = data['lang']
        payload = None

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter(User.id == user_id).first()

                user_country = None
                user_lang = None

                if user is not None:
                    for billing in itertools.product(user.billing_information):
                        for country in billing:
                            try:
                                user_country = country.country.lower()
                            except AttributeError:
                                user_country = "en"
                            user_lang = lang

                animal_query = Animal.query.filter(Animal.id == page_id).filter(Animal.visibility != "False").first()
                if animal_query is not None:

                    category_query = Category.query.filter(Category.id == animal_query.category_id).first()
                    subcategory_query = SubCategory.query.filter(SubCategory.id == animal_query.subcategory_id).first()

                    #  Start Rating
                    rating_query = Rating.query.filter_by(animal_id=animal_query.id).all()

                    if len(rating_query):
                        rating_count_all = Rating.query.filter(Rating.animal_id == animal_query.id).count()
                        rating_count_one = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 1).count()
                        rating_count_two = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 2).count()
                        rating_count_three = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 3).count()
                        rating_count_four = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 4).count()
                        rating_count_five = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
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

                    try:
                        rating_count_one_percent = (rating_count_one / rating_count_all) * 100
                        rating_count_two_percent = (rating_count_two / rating_count_all) * 100
                        rating_count_three_percent = (rating_count_three / rating_count_all) * 100
                        rating_count_four_percent = (rating_count_four / rating_count_all) * 100
                        rating_count_five_percent = (rating_count_five / rating_count_all) * 100
                    except ZeroDivisionError:
                        rating_count_one_percent = 0
                        rating_count_two_percent = 0
                        rating_count_three_percent = 0
                        rating_count_four_percent = 0
                        rating_count_five_percent = 0

                    is_user_animal_rating = Rating.query \
                        .filter(and_(Rating.user_id == user_id, Rating.animal_id == animal_query.id)) \
                        .first()
                    if is_user_animal_rating is not None:
                        is_user_animal_rating = is_user_animal_rating.rating
                    else:
                        is_user_animal_rating = None
                    #  End Rating

                    #  Start Questions
                    questions_query = Questions.query \
                        .filter(Questions.animal_id == animal_query.id) \
                        .filter(Questions.visibility) \
                        .filter(Questions.deleted == False) \
                        .order_by(desc(Questions.created_at)) \
                        .all()
                    #  End Questions

                    #  Start Question & Answer
                    questions_list = []
                    if questions_query is not None:
                        for question in questions_query:
                            answer_list = []
                            for answers in itertools.product(question.answers):

                                for answer in answers:
                                    if question.id == answer.question_id and answer.visibility and answer.deleted != True:

                                        answer_sender_user = User.query.filter(User.id == answer.user_id).first()
                                        answer_sender_last_name = None
                                        answer_sender_user_id = None
                                        if answer_sender_user is not None:
                                            answer_sender_user_id = answer_sender_user.id
                                            for billing_information in itertools.product(
                                                    answer_sender_user.billing_information):
                                                for sender in billing_information:
                                                    answer_sender_last_name = sender.last_name

                                        answer_history_list = []
                                        for answer_history in itertools.product(answer.answers_history):
                                            for answer_history_ in answer_history:
                                                answer_history_item = {
                                                    "id": answer_history_.id,
                                                    "answer_id": answer_history_.answer_id,
                                                    "answer": answer_history_.answer,
                                                    "answer_detect_lang": answer_history_.answer_detect_lang,
                                                    "deleted": str(answer_history_.deleted),
                                                    "visibility": str(answer_history_.visibility),
                                                    "created_at": answer_history_.created_at,
                                                    "updated_at": answer_history_.updated_at
                                                }
                                                answer_history_list.append(answer_history_item)
                                        answer_item = {
                                            "id": answer.id,
                                            "question_id": answer.question_id,
                                            "answer": answer.answer.replace('\n', '<br>'),
                                            "answer_detect_lang": answer.answer_detect_lang,
                                            "sender_last_name": answer_sender_last_name,
                                            "sender_id": answer_sender_user_id,
                                            "created_at": answer.created_at,
                                            "updated_at": answer.updated_at,
                                            "is_editing": answer.editing,
                                            "answer_history": answer_history_list
                                        }
                                        answer_list.append(answer_item)

                                        #  Start Answer Sorted
                                        answer_list = sorted(answer_list, key=lambda x: (
                                            x['answer_detect_lang'], x['created_at']),
                                                             reverse=True)

                                        answer_list_user_country = sorted(
                                            [x for x in answer_list if
                                             x['answer_detect_lang'] == CountryCodeToLangCode.c_to_l(user_country)],
                                            key=lambda k: k['answer_detect_lang'])

                                        answer_list_user_lang = sorted(
                                            [x for x in answer_list if x['answer_detect_lang'] == user_lang],
                                            key=lambda k: k['answer_detect_lang'])

                                        answer_list_other = sorted(
                                            [x for x in answer_list if
                                             x['answer_detect_lang'] != CountryCodeToLangCode.c_to_l(user_country) and
                                             x[
                                                 'answer_detect_lang'] != user_lang],
                                            key=lambda k: k['answer_detect_lang'])

                                        if user_country != user_lang:
                                            answer_list = answer_list_user_country + answer_list_user_lang + answer_list_other
                                        else:
                                            answer_list = answer_list_user_country + answer_list_other
                                        #  End Answer Sorted

                            # Start Question History
                            question_history_list = []
                            for question_history in itertools.product(question.questions_history):
                                for history in question_history:
                                    if history.deleted is not True and history.visibility:
                                        question_history_item = {
                                            "question_id": history.question_id,
                                            "question": history.question,
                                            "question_detect_lang": history.question_detect_lang,
                                            "deleted": str(history.deleted),
                                            "visibility": str(history.visibility),
                                            "created_at": history.created_at,
                                            "updated_at": history.updated_at
                                        }
                                        question_history_list.append(question_history_item)
                            # End Question History

                            question_sender_user = User.query.filter(User.id == question.user_id).first()
                            question_sender_last_name = None
                            question_sender_user_id = None
                            if question_sender_user is not None:
                                question_sender_user_id = question_sender_user.id
                                for billing_information in itertools.product(question_sender_user.billing_information):
                                    for sender in billing_information:
                                        question_sender_last_name = sender.last_name
                            item = {
                                "id": question.id,
                                "animal_id": question.animal_id,
                                "question": question.question,
                                "question_detect_lang": question.question_detect_lang,
                                "sender_last_name": question_sender_last_name,
                                "sender_id": question_sender_user_id,
                                "created_at": question.created_at,
                                "updated_at": question.updated_at,
                                "answer": answer_list,
                                "is_editing": question.editing,
                                "question_history": question_history_list
                            }
                            questions_list.append(item)
                    #  End Question & Answer

                    #  Start Question Sorted
                    questions_list = sorted(questions_list, key=lambda x: (x['question_detect_lang'], x['created_at']),
                                            reverse=True)

                    questions_list_user_country = sorted(
                        [x for x in questions_list if
                         x['question_detect_lang'] == CountryCodeToLangCode.c_to_l(user_country)],
                        key=lambda k: k['question_detect_lang'])

                    questions_list_user_lang = sorted(
                        [x for x in questions_list if x['question_detect_lang'] == user_lang],
                        key=lambda k: k['question_detect_lang'])

                    questions_list_other = sorted(
                        [x for x in questions_list if
                         x['question_detect_lang'] != CountryCodeToLangCode.c_to_l(user_country) and x[
                             'question_detect_lang'] != user_lang],
                        key=lambda k: k['question_detect_lang'])

                    if user_country != user_lang:
                        questions_list = questions_list_user_country + questions_list_user_lang + questions_list_other
                    else:
                        questions_list = questions_list_user_country + questions_list_other
                    #  End Question Sorted

                    #  Start Seller Data
                    seller_id = None
                    seller_last_name = None
                    seller_last_name_slug = None
                    seller_country = None
                    seller_place = None
                    animal_count = None
                    try:
                        seller_query = User.query.filter(User.id == animal_query.user_id).first()
                        for seller in itertools.product(seller_query.billing_information):
                            for seller_user in seller:
                                seller_id = seller_query.id
                                seller_last_name = seller_user.last_name
                                seller_last_name_slug = slugify(seller_user.last_name)
                                seller_country = seller_user.country
                                seller_place = seller_user.place
                        animal_count = Animal.query.filter(Animal.user_id == seller_query.id).count()
                    except AttributeError:
                        pass
                    #  End Seller Data

                    #  Start Customer Data
                    customer_id = None
                    customer_last_name = None
                    wishlist_status = None
                    try:
                        customer_query = user
                        for customer in itertools.product(customer_query.billing_information):
                            for customer_user in customer:
                                customer_id = customer_query.id
                                customer_last_name = customer_user.last_name
                    except AttributeError:
                        pass

                    wishlist_query = Wishlist.query.filter(
                        and_(Wishlist.user_id == customer_id, Wishlist.animal_id == animal_query.id)
                    ).first()
                    if wishlist_query is not None:
                        wishlist_status = "active"
                    else:
                        wishlist_status = "inactive"
                    #  End Customer data

                    for photos, videos, pdf in itertools.product(animal_query.photos, animal_query.videos,
                                                                 animal_query.pdf):
                        payload = {
                            "animal": {
                                "id": animal_query.id,
                                "advertisement_id": animal_query.advertisement_id,
                                "name": animal_query.name,
                                "name_slug": slugify(animal_query.name),
                                "price": animal_query.price,
                                "brief_description": animal_query.brief_description,
                                "brief_description_detect_lang": animal_query.brief_description_detect_lang,
                                "description": animal_query.description.replace('\n', '<br>'),
                                "description_detect_lang": animal_query.description_detect_lang,
                                "gender_hu": animal_query.gender_hu,
                                "gender_en": animal_query.gender_en,
                                "gender_de": animal_query.gender_de,
                                "gender_fr": animal_query.gender_fr,
                                "gender_es": animal_query.gender_es,
                                "color_hu": animal_query.color_hu,
                                "color_en": animal_query.color_en,
                                "color_de": animal_query.color_de,
                                "color_fr": animal_query.color_fr,
                                "color_es": animal_query.color_es,
                                "be_used_for_hu": animal_query.be_used_for_hu,
                                "be_used_for_en": animal_query.be_used_for_en,
                                "be_used_for_de": animal_query.be_used_for_de,
                                "be_used_for_fr": animal_query.be_used_for_fr,
                                "be_used_for_es": animal_query.be_used_for_es,
                                "region_residence": animal_query.region_residence,
                                "country_residence": animal_query.country_residence,
                                "url_01": animal_query.url_01,
                                "url_02": animal_query.url_02,
                                "visibility": animal_query.visibility,
                                "deleted": animal_query.deleted,
                                "created_at": animal_query.created_at,
                                "updated_at": animal_query.updated_at,
                            },
                            "video": {
                                "video_01": videos.video_01
                            },
                            "photo": {
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
                            },
                            "pdf": {

                                "x_ray": pdf.x_ray,
                                "x_ray_data": pdf.x_ray_data
                            },
                            "category": {
                                "id": category_query.id,
                                "name_hu": category_query.name_hu,
                                "name_en": category_query.name_en,
                                "name_en_slug": slugify(category_query.name_en),
                                "name_de": category_query.name_de,
                                "name_fr": category_query.name_fr,
                                "name_es": category_query.name_es,
                            },
                            "subcategory": {
                                "id": subcategory_query.id,
                                "name_hu": subcategory_query.name_hu,
                                "name_en": subcategory_query.name_en,
                                "name_en_slug": slugify(subcategory_query.name_en),
                                "name_de": subcategory_query.name_de,
                                "name_fr": subcategory_query.name_fr,
                                "name_es": subcategory_query.name_es,
                            },
                            "rating": {
                                "rating_count_all": rating_count_all,
                                "rating_count_one": rating_count_one,
                                "rating_count_one_percent": rating_count_one_percent,
                                "rating_count_two": rating_count_two,
                                "rating_count_two_percent": rating_count_two_percent,
                                "rating_count_three": rating_count_three,
                                "rating_count_three_percent": rating_count_three_percent,
                                "rating_count_four": rating_count_four,
                                "rating_count_four_percent": rating_count_four_percent,
                                "rating_count_five": rating_count_five,
                                "rating_count_five_percent": rating_count_five_percent,
                                "rating": round(rating, 1),
                                "is_user_animal_rating": is_user_animal_rating
                            },
                            "questions": questions_list,
                            "seller": {
                                "seller_id": seller_id,
                                "seller_last_name": seller_last_name,
                                "seller_last_name_slug": seller_last_name_slug,
                                "seller_country": seller_country,
                                "seller_place": seller_place,
                                "animal_count": animal_count
                            },
                            "customer": {
                                "customer_id": customer_id,
                                "customer_last_name": customer_last_name,
                                "wishlist_status": wishlist_status
                            }
                        }
                    data = {"status": "success", "animal": payload}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class FullDataInfoPage(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = full_data_info_box.parse_args()

        animal_id = int(data['animal_id'])

        if api_key == app.config['API_KEY']:
            try:
                animal_query = Animal.query.filter(Animal.id == animal_id).first()

                if animal_query is not None:

                    #  Start Rating
                    rating_query = Rating.query.filter_by(animal_id=animal_query.id).all()

                    if len(rating_query):
                        rating_count_all = Rating.query.filter(Rating.animal_id == animal_query.id).count()
                        rating_count_one = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 1).count()
                        rating_count_two = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 2).count()
                        rating_count_three = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 3).count()
                        rating_count_four = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
                            .filter(Rating.rating == 4).count()
                        rating_count_five = Rating.query \
                            .filter(Rating.animal_id == animal_query.id) \
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

                    #  Start Questions Count
                    questions_count = Questions.query \
                        .filter(Questions.animal_id == animal_query.id) \
                        .filter(Questions.visibility) \
                        .filter(Questions.deleted == False) \
                        .count()
                    #  End Questions Count

                    #  Start Talking Count
                    talking_count = Talking.query \
                        .filter(Talking.subcategory_id == animal_query.subcategory_id) \
                        .filter(Talking.visibility) \
                        .filter(Talking.deleted == False) \
                        .count()
                    #  End Talking Count

                    data = {"status": 'success', "rating": round(rating, 1), "questions_count": questions_count,
                            "talking_count": talking_count}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class WishlistPost(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = wishlist_data.parse_args()

        animal_id = int(data['animal_id'])
        user_id = int(data['user_id'])
        wishlist_status = data['wishlist_status']

        if api_key == app.config['API_KEY']:
            try:
                animal_query = Animal.query.filter(Animal.id == animal_id).first()
                user_query = User.query.filter(User.id == user_id).first()
                if animal_query is not None and user_query is not None:
                    wishlist_query = Wishlist.query.filter(
                        and_(Wishlist.animal_id == animal_id, Wishlist.user_id == user_id)).first()
                    if wishlist_status == "active":
                        if wishlist_query is not None:
                            wishlist_query.db_delete()
                            wishlist_status = "inactive"
                    elif wishlist_status == "inactive":
                        if wishlist_query is None:
                            wishlist_payload = Wishlist(user_id=user_id, animal_id=animal_id)
                            wishlist_payload.wishlist_backref.append(user_query)
                            wishlist_payload.db_post()
                            wishlist_status = "active"
                    else:
                        pass
                    data = {"status": 'success', "wishlist_status": wishlist_status}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify({"status": "error"}), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class AlikeGet(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = alike_data.parse_args()

        subcategory_id = int(data['subcategory_id'])
        animal_id = int(data['animal_id'])
        price_show = data['price_show']
        customer_user_id = data['customer_user_id']
        lang = data['lang']

        if api_key == app.config['API_KEY']:
            try:
                # animal_query = Animal.query.filter(and_(Animal.subcategory_id == subcategory_id, Animal.id != animal_id)).order_by(desc(Animal.rating)).limit(6)
                animal_query = Animal.query.filter(
                    and_(Animal.subcategory_id == subcategory_id, Animal.id != animal_id)).order_by(
                    func.random()).limit(3)

                if animal_query is not None:
                    animals_list = []
                    for animal in animal_query:
                        category_query = Category.query.filter(Category.id == animal.category_id).first()
                        subcategory_query = SubCategory.query.filter(SubCategory.id == animal.subcategory_id).first()
                        for photos, videos, pdf in itertools.product(animal.photos, animal.videos, animal.pdf):
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
                                            price_show = True
                                        else:
                                            price_exchange_currency = None
                                            price_exchange = None
                                            price_show = False
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
                                    "rating": animal.rating,
                                    "page_url": animal.page_url,
                                    "price": animal.price,
                                    "price_exchange_currency": price_exchange_currency,
                                    "price_exchange": price_exchange,
                                    "price_show": price_show
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
                                    "img_10": photos.img_10
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
                                "lang": {
                                    "lang": lang
                                }
                            }
                            animals_list.append(item)
                    data = {"animal": animals_list}
                    return make_response(jsonify(data), 200)
                else:
                    pass
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class UserToUserMessage(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = user_to_user_message_data.parse_args()

        sender_id = int(data['sender_id'])
        host_id = int(data['host_id'])

        if api_key == app.config['API_KEY']:
            try:
                sender_query = User.query.filter(User.id == sender_id).first()
                host_query = User.query.filter(User.id == host_id).first()

                if sender_query is not None and host_query is not None:
                    sender_user_profile = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == sender_query.id).first()

                    sender_user_billing = UserBillingInformation \
                        .query.join(User.billing_information) \
                        .filter(User.id == sender_query.id).first()

                    host_user_profile = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == host_query.id).first()

                    host_user_billing = UserBillingInformation \
                        .query.join(User.billing_information) \
                        .filter(User.id == host_query.id).first()

                    room = VerificationCode.generate_pin(24)

                    message_payload = Messages(
                        sender_id=sender_query.id,
                        sender_first_name=sender_user_billing.first_name,
                        sender_last_name=sender_user_billing.last_name,
                        sender_username=sender_user_profile.username,
                        host_id=host_query.id,
                        host_first_name=host_user_billing.first_name,
                        host_last_name=host_user_billing.last_name,
                        host_username=host_user_profile.username,
                        message=app.config['USER_TO_USER_FIRST_MESSAGE'],
                        room=room
                    )
                    message_payload.received = "True"
                    message_payload.sender_assistant = "False"
                    message_payload.db_post()

                    data = {"status": 'success', "sender_id": sender_query.id, "host_id": host_query.id,
                            "message_id": message_payload.id, "message": app.config['USER_TO_USER_FIRST_MESSAGE']}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify({"status": "error"}), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(FullPage, '/full-page')
api.add_resource(FullDataInfoPage, '/full-data-info-box')
api.add_resource(WishlistPost, '/wishlist')
api.add_resource(AlikeGet, '/alike')
api.add_resource(UserToUserMessage, '/user-to-user-message')

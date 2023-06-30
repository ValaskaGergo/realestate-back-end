# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from app.models.models import User, Talking, TalkingHistory, TalkingAnswer, TalkingAnswerHistory, TalkingVote
from .utilities.validators import Validation
import detectlanguage
import itertools
from sqlalchemy import or_, and_, desc, asc, func
from .utilities.utility import CountryCodeToLangCode

mod = Blueprint('talking_module', __name__)
api = Api(mod)

detectlanguage.configuration.api_key = app.config['DETECT_LANGUAGE_KEY']
detectlanguage.configuration.secure = True

post_talking_data = reqparse.RequestParser()
post_talking_data.add_argument('category_id', required=True)
post_talking_data.add_argument('subcategory_id', required=True)
post_talking_data.add_argument('user_id', required=True)
post_talking_data.add_argument('experience', required=True)

get_talking_data = reqparse.RequestParser()
get_talking_data.add_argument('subcategory_id', required=True)
get_talking_data.add_argument('user_id', required=True)
get_talking_data.add_argument('lang')

delete_talking_data = reqparse.RequestParser()
delete_talking_data.add_argument('user_id', required=True)
delete_talking_data.add_argument('talking_id', required=True)
delete_talking_data.add_argument('experience', required=True)

edit_talking_data = reqparse.RequestParser()
edit_talking_data.add_argument('user_id', required=True)
edit_talking_data.add_argument('talking_id', required=True)
edit_talking_data.add_argument('experience', required=True)

get_talking_history_data = reqparse.RequestParser()
get_talking_history_data.add_argument('user_id', required=True)
get_talking_history_data.add_argument('talking_id', required=True)

post_talking_answer_data = reqparse.RequestParser()
post_talking_answer_data.add_argument('talking_id', required=True)
post_talking_answer_data.add_argument('talking_answer_id')
post_talking_answer_data.add_argument('answer', required=True)
post_talking_answer_data.add_argument('answer_type', required=True)
post_talking_answer_data.add_argument('user_id', required=True)

delete_talking_answer_data = reqparse.RequestParser()
delete_talking_answer_data.add_argument('user_id', required=True)
delete_talking_answer_data.add_argument('talking_answer_id', required=True)
delete_talking_answer_data.add_argument('answer', required=True)

edit_talking_answer_data = reqparse.RequestParser()
edit_talking_answer_data.add_argument('user_id', required=True)
edit_talking_answer_data.add_argument('talking_answer_id', required=True)
edit_talking_answer_data.add_argument('answer', required=True)

get_talking_answer_history_data = reqparse.RequestParser()
get_talking_answer_history_data.add_argument('user_id', required=True)
get_talking_answer_history_data.add_argument('talking_answer_id', required=True)

post_talk_vote_data = reqparse.RequestParser()
post_talk_vote_data.add_argument('user_id', required=True)
post_talk_vote_data.add_argument('talking_id', required=True)
post_talk_vote_data.add_argument('vote', required=True)


class PostTalking(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = post_talking_data.parse_args()

        category_id = int(data['category_id'])
        subcategory_id = int(data['subcategory_id'])
        user_id = int(data['user_id'])
        experience = data['experience']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking(experience)

                if validation['status'] == "success":

                    detectlanguage_status = detectlanguage.user_status()
                    if detectlanguage_status['status'] == "ACTIVE":
                        lang = detectlanguage.detect(experience)

                        if lang[0]['language']:
                            experience_detect_lang = lang[0]['language']
                        else:
                            experience_detect_lang = None
                    else:
                        experience_detect_lang = None

                    talking_payload = Talking(
                        category_id=category_id,
                        subcategory_id=subcategory_id,
                        user_id=user_id,
                        experience=experience,
                        experience_detect_lang=experience_detect_lang)

                    talking_payload.db_post()

                    talking_sender_user = User.query.filter(User.id == user_id).first()
                    sender_last_name = None
                    talking_sender_user_id = None
                    if talking_sender_user is not None:
                        talking_sender_user_id = talking_sender_user.id
                        for billing_information in itertools.product(talking_sender_user.billing_information):
                            for sender in billing_information:
                                sender_last_name = sender.last_name

                    #  Start Talking Count
                    talking_count = Talking.query \
                        .filter(Talking.subcategory_id == subcategory_id) \
                        .filter(Talking.visibility) \
                        .filter(Talking.deleted == False) \
                        .count()
                    #  End Talking Count

                    talking_data = {
                        "id": talking_payload.id,
                        "category_id": talking_payload.category_id,
                        "subcategory_id": talking_payload.subcategory_id,
                        "user_id": talking_payload.user_id,
                        "experience": talking_payload.experience,
                        "experience_detect_lang": talking_payload.experience_detect_lang,
                        "sender_last_name": sender_last_name,
                        "sender_id": talking_sender_user_id,
                        "created_at": talking_payload.created_at,
                        "updated_at": talking_payload.updated_at,
                        "is_editing": str(talking_payload.editing),
                        "talking_count": talking_count
                    }

                    data = {"status": 'success', "talking_data": talking_data}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetTalking(Resource):
    @staticmethod
    def get():
        api_key = request.headers['X-Api-Key']
        data = get_talking_data.parse_args()

        subcategory_id = int(data['subcategory_id'])
        user_id = int(data['user_id'])
        lang = data['lang']

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

                talking_query = Talking.query \
                    .filter(Talking.subcategory_id == subcategory_id) \
                    .filter(Talking.visibility) \
                    .filter(Talking.deleted == False) \
                    .order_by(desc(Talking.created_at)) \
                    .all()

                talking_list = []
                if talking_query is not None:
                    talking_user_vote = None
                    for talking in talking_query:

                        talking_user = User.query.filter(User.id == talking.user_id).first()
                        talking_user_last_name = None
                        if talking_user is not None:
                            for billing_information in itertools.product(talking_user.billing_information):
                                for sender in billing_information:
                                    talking_user_last_name = sender.last_name

                        talking_history_list = []
                        for history_data in itertools.product(talking.talking_history):
                            for history in history_data:
                                talking_history_item = {
                                    "talking_id": history.talking_id,
                                    "experience": history.experience,
                                    "experience_detect_lang": history.experience_detect_lang,
                                    "deleted": history.deleted,
                                    "visibility": history.visibility,
                                    "created_at": history.created_at,
                                    "updated_at": history.updated_at,
                                }
                                talking_history_list.append(talking_history_item)

                        talking_answer_list = []
                        talking_answer_id_query = None
                        for talking_answer in itertools.product(talking.talking_answer):
                            for answer in talking_answer:
                                if talking.id == answer.talking_id and answer.visibility and answer.deleted != True:
                                    sender_user = User.query.filter(User.id == answer.user_id).first()
                                    sender_user_id = sender_user.id
                                    sender_user_last_name = None
                                    if sender_user is not None:
                                        for billing_information in itertools.product(
                                                sender_user.billing_information):
                                            for sender in billing_information:
                                                sender_user_last_name = sender.last_name

                                    if answer.answer_type == "talking":
                                        host_user_id = talking.user_id
                                        host_user_last_name = talking_user_last_name
                                    else:
                                        try:
                                            talking_answer_id_query = TalkingAnswer.query.filter(
                                                TalkingAnswer.id == answer.talking_answer_id).first()
                                            host_user = User.query.filter(
                                                User.id == talking_answer_id_query.user_id).first()
                                            talking_answer_id_query = talking_answer_id_query.id
                                        except AttributeError:
                                            host_user = User.query.filter(User.id == answer.user_id).first()
                                        host_user_id = answer.id
                                        host_user_last_name = None
                                        if host_user is not None:
                                            for billing_information in itertools.product(
                                                    host_user.billing_information):
                                                for host in billing_information:
                                                    host_user_last_name = host.last_name

                                    talking_answer_item = {
                                        "id": answer.id,
                                        "talking_id": answer.talking_id,
                                        "talking_answer_id": talking_answer_id_query,
                                        "user_id": user.id,
                                        "talking_user_id": talking.user_id,
                                        "talking_user_last_name": talking_user_last_name,
                                        "host_user_id": host_user_id,
                                        "host_user_last_name": host_user_last_name,
                                        "sender_user_id": sender_user_id,
                                        "sender_user_last_name": sender_user_last_name,
                                        "answer": answer.answer,
                                        "answer_detect_lang": answer.answer_detect_lang,
                                        "answer_type": answer.answer_type,
                                        "editing": answer.editing,
                                        "deleted": answer.deleted,
                                        "visibility": str(answer.visibility),
                                        "created_at": answer.created_at,
                                        "updated_at": answer.updated_at,
                                    }
                                    talking_answer_list.append(talking_answer_item)

                                    talking_answer_list = sorted(talking_answer_list, key=lambda x: (x['created_at']),
                                                                 reverse=False)

                        talking_vote_query = TalkingVote.query \
                            .filter(TalkingVote.talking_id == talking.id) \
                            .filter(TalkingVote.user_id == user_id) \
                            .first()
                        if talking_vote_query is not None:
                            if talking_vote_query.vote == "up":
                                talking_user_vote = "up"
                            elif talking_vote_query.vote == "down":
                                talking_user_vote = "down"
                            else:
                                talking_user_vote = None

                        talking_item = {
                            "id": talking.id,
                            "category_id": talking.category_id,
                            "subcategory_id": talking.subcategory_id,
                            "sender_user_id": talking.user_id,
                            "sender_user_last_name": talking_user_last_name,
                            "experience": talking.experience.replace('\n', '<br>'),
                            "experience_detect_lang": talking.experience_detect_lang,
                            "editing": talking.editing,
                            "deleted": talking.deleted,
                            "visibility": talking.visibility,
                            "created_at": talking.created_at,
                            "updated_at": talking.updated_at,
                            "user_id": user_id,
                            "talking_history": talking_history_list,
                            "talking_answer": talking_answer_list,
                            "vote": talking.vote,
                            "talking_user_vote": talking_user_vote,
                            "browser_lang": lang
                        }
                        talking_list.append(talking_item)

                        #  Start Talking Sorted
                        talking_list = sorted(talking_list,
                                              key=lambda x: (x['experience_detect_lang'], x['created_at']),
                                              reverse=True)

                        talking_list_user_country = sorted(
                            [x for x in talking_list if
                             x['experience_detect_lang'] == CountryCodeToLangCode.c_to_l(user_country)],
                            key=lambda k: (k['experience_detect_lang'], k['vote']), reverse=True)

                        talking_list_user_lang = sorted(
                            [x for x in talking_list if x['experience_detect_lang'] == user_lang],
                            key=lambda k: (k['experience_detect_lang'], k['vote']), reverse=True)

                        talking_list_other = sorted(
                            [x for x in talking_list if
                             x['experience_detect_lang'] != CountryCodeToLangCode.c_to_l(user_country) and x[
                                 'experience_detect_lang'] != user_lang],
                            key=lambda k: (k['experience_detect_lang'], k['vote']), reverse=True)

                        if user_country != user_lang:
                            talking_list = talking_list_user_country + talking_list_user_lang + talking_list_other
                        else:
                            talking_list = talking_list_user_country + talking_list_other
                        #  End Talking Sorted

                    data = {"status": "success", "talking_list": talking_list}
                    return make_response(jsonify(data), 200)
                else:
                    data = {"status": "success", "talking_list": talking_list}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class TalkingDelete(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = delete_talking_data.parse_args()

        user_id = int(data['user_id'])
        talking_id = int(data['talking_id'])
        experience = data['experience']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking_deleted(experience)

                if validation['status'] == "success":
                    talking_query = Talking.query.filter(Talking.id == talking_id).first()
                    if talking_query is not None and talking_query.user_id == user_id:
                        talking_query.deleted = True
                        talking_query.db_post()

                        #  Start Talking Count
                        talking_count = Talking.query \
                            .filter(Talking.subcategory_id == talking_query.subcategory_id) \
                            .filter(Talking.visibility) \
                            .filter(Talking.deleted == False) \
                            .count()
                        #  End Talking Count

                        data = {"status": 'success', "talking_id": talking_query.id, "talking_count": talking_count}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class TalkingEdit(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = edit_talking_data.parse_args()

        user_id = int(data['user_id'])
        talking_id = int(data['talking_id'])
        experience = data['experience']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking_edit(experience)

                if validation['status'] == "success":
                    talking_query = Talking.query.filter(Talking.id == talking_id).first()
                    if talking_query is not None and talking_query.user_id == user_id:
                        if talking_query.experience != experience:
                            detectlanguage_status = detectlanguage.user_status()
                            if detectlanguage_status['status'] == "ACTIVE":
                                lang = detectlanguage.detect(experience)

                                if lang[0]['language']:
                                    experience_detect_lang = lang[0]['language']
                                else:
                                    experience_detect_lang = None
                            else:
                                experience_detect_lang = None

                            # Start History
                            history_payload = TalkingHistory(
                                talking_id=talking_query.id,
                                experience=talking_query.experience,
                                experience_detect_lang=talking_query.experience_detect_lang
                            )
                            history_payload.talking_history_backref.append(talking_query)
                            history_payload.db_post()

                            # End History

                            talking_query.experience = experience
                            talking_query.experience_detect_lang = experience_detect_lang
                            talking_query.editing = True
                            talking_query.db_post()

                            data = {"status": 'success', "talking_id": talking_query.id,
                                    "experience": talking_query.experience,
                                    "experience_detect_lang": talking_query.experience_detect_lang}
                            return make_response(jsonify(data), 200)
                        else:
                            data = {"status": 'success', "talking_id": talking_query.id,
                                    "experience": talking_query.experience,
                                    "experience_detect_lang": talking_query.experience_detect_lang}
                            return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetTalkingHistory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_talking_history_data.parse_args()

        user_id = int(data['user_id'])
        talking_id = int(data['talking_id'])
        talking_history_list = []

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking_history(talking_id)

                if validation['status'] == "success":
                    talking_query = Talking.query.filter(Talking.id == talking_id).first()
                    if talking_query is not None:
                        for talking_history in itertools.product(talking_query.talking_history):
                            for history in talking_history:
                                if history.deleted != True and history.visibility != False:
                                    item = {
                                        "id": history.id,
                                        "talking_id": talking_query.id,
                                        "experience": history.experience,
                                        "experience_detect_lang": history.experience_detect_lang,
                                        "deleted": str(history.deleted),
                                        "visibility": str(history.visibility),
                                        "created_at": history.created_at,
                                        "updated_at": history.updated_at,
                                    }
                                    talking_history_list.append(item)
                        data = {"status": 'success', "talking_history": talking_history_list}
                        return make_response(jsonify(data), 200)
                    else:
                        data = {"status": 'success', "talking_history": []}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class PostTalkingAnswer(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = post_talking_answer_data.parse_args()

        talking_id = int(data['talking_id'])
        talking_answer_id = data['talking_answer_id']
        answer = data['answer']
        answer_type = data['answer_type']
        user_id = int(data['user_id'])

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking_answer(answer)

                if validation['status'] == "success":

                    detectlanguage_status = detectlanguage.user_status()
                    if detectlanguage_status['status'] == "ACTIVE":
                        lang = detectlanguage.detect(answer)

                        if lang[0]['language']:
                            answer_detect_lang = lang[0]['language']
                        else:
                            answer_detect_lang = None
                    else:
                        answer_detect_lang = None

                    talking_answer_payload = TalkingAnswer(
                        talking_id=talking_id,
                        user_id=user_id,
                        answer=answer,
                        answer_detect_lang=answer_detect_lang,
                        answer_type=answer_type
                    )

                    if talking_answer_id is not None:
                        talking_answer_payload.talking_answer_id = talking_answer_id

                    talking_query = Talking.query.filter(Talking.id == talking_id).first()
                    talking_answer_payload.talking_answer_backref.append(talking_query)
                    talking_answer_payload.db_post()

                    sender_user = User.query.filter(User.id == user_id).first()
                    sender_last_name = None
                    sender_user_id = None
                    if sender_user is not None:
                        sender_user_id = sender_user.id
                        for billing_information in itertools.product(sender_user.billing_information):
                            for sender in billing_information:
                                sender_last_name = sender.last_name

                    talking_sender_user = User.query.filter(User.id == talking_query.user_id).first()
                    talking_sender_last_name = None
                    talking_sender_user_id = None
                    if talking_sender_user is not None:
                        talking_sender_user_id = talking_sender_user.id
                        for billing_information in itertools.product(talking_sender_user.billing_information):
                            for talking_sender in billing_information:
                                talking_sender_last_name = talking_sender.last_name

                    talking_answer_data = {
                        "id": talking_answer_payload.id,
                        "talking_id": talking_query.id,
                        "answer": talking_answer_payload.answer,
                        "answer_detect_lang": talking_answer_payload.answer_detect_lang,
                        "answer_type": answer_type,
                        "sender_last_name": sender_last_name,
                        "sender_id": sender_user_id,
                        "talking_sender_last_name": talking_sender_last_name,
                        "talking_sender_user_id": talking_sender_user_id,
                        "created_at": talking_answer_payload.created_at,
                        "updated_at": talking_answer_payload.updated_at,
                        "is_editing": str(talking_answer_payload.editing)
                    }

                    data = {"status": 'success', "talking_answer_data": talking_answer_data}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class TalkingAnswerDelete(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = delete_talking_answer_data.parse_args()

        app.logger.info(data)

        user_id = int(data['user_id'])
        talking_answer_id = int(data['talking_answer_id'])
        answer = data['answer']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking_answer_deleted(answer)

                if validation['status'] == "success":
                    talking_answer_query = TalkingAnswer.query.filter(TalkingAnswer.id == talking_answer_id).first()
                    if talking_answer_query is not None and talking_answer_query.user_id == user_id:
                        talking_answer_query.deleted = True
                        talking_answer_query.db_post()

                        data = {"status": 'success', "talking_answer_id": talking_answer_query.id}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class TalkingAnswerEdit(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = edit_talking_answer_data.parse_args()

        user_id = int(data['user_id'])
        talking_answer_id = int(data['talking_answer_id'])
        answer = data['answer']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking_answer_edit(answer)

                if validation['status'] == "success":
                    talking_answer_query = TalkingAnswer.query.filter(TalkingAnswer.id == talking_answer_id).first()
                    if talking_answer_query is not None and talking_answer_query.user_id == user_id:
                        if talking_answer_query.answer != answer:
                            detectlanguage_status = detectlanguage.user_status()
                            if detectlanguage_status['status'] == "ACTIVE":
                                lang = detectlanguage.detect(answer)

                                if lang[0]['language']:
                                    answer_detect_lang = lang[0]['language']
                                else:
                                    answer_detect_lang = None
                            else:
                                answer_detect_lang = None

                            # Start History
                            history_payload = TalkingAnswerHistory(
                                talking_id=talking_answer_query.id,
                                answer=talking_answer_query.answer,
                                answer_detect_lang=talking_answer_query.answer_detect_lang,
                                answer_type=talking_answer_query.answer_type
                            )
                            history_payload.talking_answer_history_backref.append(talking_answer_query)
                            history_payload.db_post()

                            # End History

                            talking_answer_query.answer = answer
                            talking_answer_query.answer_detect_lang = answer_detect_lang
                            talking_answer_query.editing = True
                            talking_answer_query.db_post()

                            data = {"status": 'success', "talking_answer_id": talking_answer_query.id,
                                    "answer": talking_answer_query.answer,
                                    "answer_detect_lang": talking_answer_query.answer_detect_lang}
                            return make_response(jsonify(data), 200)
                        else:
                            data = {"status": 'success', "talking_answer_id": talking_answer_query.id,
                                    "answer": talking_answer_query.answer,
                                    "answer_detect_lang": talking_answer_query.experience_detect_lang}
                            return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetTalkingAnswerHistory(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_talking_answer_history_data.parse_args()

        app.logger.info(data)

        user_id = int(data['user_id'])
        talking_answer_id = int(data['talking_answer_id'])
        talking_answer_history_list = []

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.talking_answer_history(talking_answer_id)

                if validation['status'] == "success":
                    talking_answer_query = TalkingAnswer.query.filter(TalkingAnswer.id == talking_answer_id).first()
                    if talking_answer_query is not None:
                        for talking_answer_history in itertools.product(talking_answer_query.talking_answer_history):
                            for history in talking_answer_history:
                                if history.deleted != True and history.visibility != False:
                                    item = {
                                        "id": history.id,
                                        "talking_answer_id": talking_answer_query.id,
                                        "answer": history.answer,
                                        "answer_detect_lang": history.answer_detect_lang,
                                        "deleted": str(history.deleted),
                                        "visibility": str(history.visibility),
                                        "created_at": history.created_at,
                                        "updated_at": history.updated_at,
                                    }
                                    talking_answer_history_list.append(item)
                        data = {"status": 'success', "talking_answer_history": talking_answer_history_list}
                        return make_response(jsonify(data), 200)
                    else:
                        data = {"status": 'success', "talking_history": []}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class PostTalkVote(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = post_talk_vote_data.parse_args()

        user_id = int(data['user_id'])
        talking_id = int(data['talking_id'])
        vote = data['vote']

        if api_key == app.config['API_KEY']:
            try:
                talking_query = Talking.query.filter(Talking.id == talking_id).first()

                talking_vote_query = TalkingVote.query \
                    .filter(TalkingVote.talking_id == talking_query.id) \
                    .filter(TalkingVote.user_id == user_id) \
                    .first()

                user_vote = vote
                user_vote_action = None

                if talking_vote_query is not None:
                    if vote == "up":
                        if talking_vote_query.vote == "up":
                            user_vote_action = "rm"
                            talking_vote_query.db_delete()
                        elif talking_vote_query.vote == "down":
                            user_vote_action = "added"
                            talking_vote_query.vote = "up"
                            talking_vote_query.db_post()
                        else:
                            pass
                    elif vote == "down":
                        if talking_vote_query.vote == "down":
                            user_vote_action = "rm"
                            talking_vote_query.db_delete()
                        elif talking_vote_query.vote == "up":
                            user_vote_action = "added"
                            talking_vote_query.vote = "down"
                            talking_vote_query.db_post()
                        else:
                            pass
                    else:
                        pass
                elif talking_vote_query is None:
                    talking_vote_payload = TalkingVote(
                        talking_id=talking_id,
                        user_id=user_id,
                        vote=vote,
                    )
                    talking_vote_payload.talking_vote_backref.append(talking_query)
                    talking_vote_payload.db_post()
                    user_vote_action = "added"
                else:
                    return make_response(jsonify(), 400)

                talking_vote_up_count = TalkingVote.query \
                    .filter(TalkingVote.talking_id == talking_id) \
                    .filter(TalkingVote.vote == "up") \
                    .count()
                talking_vote_down_count = TalkingVote.query \
                    .filter(TalkingVote.talking_id == talking_id) \
                    .filter(TalkingVote.vote == "down") \
                    .count()

                talking_vote_count = talking_vote_up_count - talking_vote_down_count
                talking_query.vote = talking_vote_count
                talking_query.db_post()

                data = {"status": 'success',
                        "talking_vote_count": talking_vote_count,
                        "user_vote": user_vote,
                        "user_vote_action": user_vote_action
                        }
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(PostTalking, '/post-talking')
api.add_resource(GetTalking, '/get-talking')
api.add_resource(TalkingDelete, '/talking-delete')
api.add_resource(TalkingEdit, '/talking-edit')
api.add_resource(GetTalkingHistory, '/get-talking-history')
api.add_resource(PostTalkingAnswer, '/post-talking-answer')
api.add_resource(TalkingAnswerDelete, '/talking-answer-delete')
api.add_resource(TalkingAnswerEdit, '/talking-answer-edit')
api.add_resource(GetTalkingAnswerHistory, '/get-talking-answer-history')
api.add_resource(PostTalkVote, '/post-talk-vote')

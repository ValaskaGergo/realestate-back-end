# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from app.models.models import User, Animal, Questions, QuestionsHistory, Answers, AnswersHistory
from .utilities.validators import Validation
import detectlanguage
import itertools

mod = Blueprint('questions_and_answers_module', __name__)
api = Api(mod)

detectlanguage.configuration.api_key = app.config['DETECT_LANGUAGE_KEY']
detectlanguage.configuration.secure = True

post_question_data = reqparse.RequestParser()
post_question_data.add_argument('animal_id', required=True)
post_question_data.add_argument('user_id', required=True)
post_question_data.add_argument('question', required=True)

post_answer_data = reqparse.RequestParser()
post_answer_data.add_argument('question_id', required=True)
post_answer_data.add_argument('user_id', required=True)
post_answer_data.add_argument('answer', required=True)

question_delete = reqparse.RequestParser()
question_delete.add_argument('user_id', required=True)
question_delete.add_argument('question_id', required=True)
question_delete.add_argument('question', required=True)

question_edit = reqparse.RequestParser()
question_edit.add_argument('user_id', required=True)
question_edit.add_argument('question_id', required=True)
question_edit.add_argument('question', required=True)

answer_delete = reqparse.RequestParser()
answer_delete.add_argument('user_id', required=True)
answer_delete.add_argument('answer_id', required=True)
answer_delete.add_argument('answer', required=True)

answer_edit = reqparse.RequestParser()
answer_edit.add_argument('user_id', required=True)
answer_edit.add_argument('answer_id', required=True)
answer_edit.add_argument('answer', required=True)


class PostQuestion(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = post_question_data.parse_args()

        user_id = int(data['user_id'])
        animal_id = int(data['animal_id'])
        question = data['question']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.question(question)

                if validation['status'] == "success":
                    user = User.query.filter_by(id=user_id).first()
                    animal = Animal.query.filter_by(id=animal_id).first()

                    detectlanguage_status = detectlanguage.user_status()
                    if detectlanguage_status['status'] == "ACTIVE":
                        lang = detectlanguage.detect(question)

                        if lang[0]['language']:
                            question_detect_lang = lang[0]['language']
                        else:
                            question_detect_lang = None
                    else:
                        question_detect_lang = None

                    question_payload = Questions(
                        animal_id=animal.id,
                        user_id=user.id,
                        question=question,
                        question_detect_lang=question_detect_lang)

                    question_payload.db_post()

                    question_sender_user = User.query.filter(User.id == user.id).first()
                    sender_last_name = None
                    question_sender_user_id = None
                    if question_sender_user is not None:
                        question_sender_user_id = question_sender_user.id
                        for billing_information in itertools.product(question_sender_user.billing_information):
                            for sender in billing_information:
                                sender_last_name = sender.last_name

                    #  Start Questions Count
                    questions_count = Questions.query \
                        .filter(Questions.animal_id == animal_id) \
                        .filter(Questions.visibility) \
                        .filter(Questions.deleted == False) \
                        .count()
                    #  End Questions Count

                    question_data = {
                        "id": question_payload.id,
                        "animal_id": question_payload.animal_id,
                        "question": question_payload.question,
                        "question_detect_lang": question_payload.question_detect_lang,
                        "sender_last_name": sender_last_name,
                        "sender_id": question_sender_user_id,
                        "created_at": question_payload.created_at,
                        "updated_at": question_payload.updated_at,
                        "is_editing": question_payload.editing,
                        "questions_count": questions_count
                    }

                    data = {"status": 'success', "question_data": question_data}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class PostAnswer(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = post_answer_data.parse_args()

        user_id = int(data['user_id'])
        question_id = int(data['question_id'])
        answer = data['answer']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.answer(answer)

                if validation['status'] == "success":
                    user = User.query.filter_by(id=user_id).first()
                    question = Questions.query.filter_by(id=question_id).first()

                    detectlanguage_status = detectlanguage.user_status()
                    if detectlanguage_status['status'] == "ACTIVE":
                        lang = detectlanguage.detect(answer)

                        if lang[0]['language']:
                            answer_detect_lang = lang[0]['language']
                        else:
                            answer_detect_lang = None
                    else:
                        answer_detect_lang = None

                    answer_payload = Answers(
                        question_id=question.id,
                        user_id=user.id,
                        answer=answer,
                        answer_detect_lang=answer_detect_lang
                    )
                    if question.deleted != True or question.visibility != False:
                        answer_payload.answers_backref.append(question)
                        answer_payload.db_post()

                    answer_sender_user = User.query.filter(User.id == user.id).first()
                    sender_last_name = None
                    answer_sender_user_id = None
                    if answer_sender_user is not None:
                        answer_sender_user_id = answer_sender_user.id
                        for billing_information in itertools.product(answer_sender_user.billing_information):
                            for sender in billing_information:
                                sender_last_name = sender.last_name

                    answer_data = {
                        "question_id": question_id,
                        "id": answer_payload.id,
                        "animal_id": question.animal_id,
                        "answer": answer_payload.answer,
                        "question_detect_lang": answer_payload.answer_detect_lang,
                        "sender_last_name": sender_last_name,
                        "sender_id": answer_sender_user_id,
                        "created_at": answer_payload.created_at,
                        "updated_at": answer_payload.updated_at,
                        "is_editing": answer_payload.editing
                    }

                    data = {"status": 'success', "answer_data": answer_data}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                app.logger.info(data)
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class QuestionDelete(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = question_delete.parse_args()

        user_id = int(data['user_id'])
        question_id = int(data['question_id'])
        question = data['question']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.question_deleted(question)

                if validation['status'] == "success":
                    question_query = Questions.query.filter(Questions.id == question_id).first()
                    if question_query is not None and question_query.user_id == user_id:
                        question_query.deleted = True
                        question_query.db_post()

                    #  Start Questions Count
                    questions_count = Questions.query \
                        .filter(Questions.animal_id == question_query.animal_id) \
                        .filter(Questions.visibility) \
                        .filter(Questions.deleted == False) \
                        .count()
                    #  End Questions Count

                    data = {"status": 'success', "question_id": question_id, "questions_count": questions_count}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class QuestionEdit(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = question_edit.parse_args()

        user_id = data['user_id']
        question_id = data['question_id']
        question = data['question']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.question_edit(question)

                if validation['status'] == "success":
                    question_query = Questions.query.filter(Questions.id == question_id).first()

                    if question != question_query.question:

                        detectlanguage_status = detectlanguage.user_status()
                        if detectlanguage_status['status'] == "ACTIVE":
                            lang = detectlanguage.detect(question)

                            if lang[0]['language']:
                                question_detect_lang = lang[0]['language']
                            else:
                                question_detect_lang = None
                        else:
                            question_detect_lang = None

                        # Start History
                        history_payload = QuestionsHistory(
                            question_id=question_query.id,
                            question=question_query.question,
                            question_detect_lang=question_query.question_detect_lang
                        )
                        history_payload.questions_history_backref.append(question_query)
                        history_payload.db_post()

                        # End History

                        question_query.question = question
                        question_query.question_detect_lang = question_detect_lang
                        question_query.editing = True
                        question_query.db_post()

                        user = User.query.filter_by(id=user_id).first()

                        question_sender_user = User.query.filter(User.id == user.id).first()
                        sender_last_name = None
                        question_sender_user_id = None
                        if question_sender_user is not None:
                            question_sender_user_id = question_sender_user.id
                            for billing_information in itertools.product(question_sender_user.billing_information):
                                for sender in billing_information:
                                    sender_last_name = sender.last_name

                        question_data = {
                            "id": question_query.id,
                            "animal_id": question_query.animal_id,
                            "question": question_query.question,
                            "question_detect_lang": question_query.question_detect_lang,
                            "sender_last_name": sender_last_name,
                            "sender_id": question_sender_user_id,
                            "created_at": question_query.created_at,
                            "updated_at": question_query.updated_at,
                            "is_editing": question_query.editing
                        }

                        data = {"status": 'success', "question_data": question_data}
                        return make_response(jsonify(data), 200)
                    else:
                        data = {"status": 'success'}
                        return make_response(jsonify(data), 201)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class AnswerDelete(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = answer_delete.parse_args()

        user_id = int(data['user_id'])
        answer_id = int(data['answer_id'])
        answer = data['answer']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.question_deleted(answer)

                if validation['status'] == "success":
                    answer_query = Answers.query.filter(Answers.id == answer_id).first()
                    if answer_query is not None and answer_query.user_id == user_id:
                        answer_query.deleted = True
                        answer_query.db_post()

                    data = {"status": 'success', "answer_id": answer_id, "question_id": answer_query.question_id}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class AnswerEdit(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = answer_edit.parse_args()

        app.logger.info(data)

        user_id = data['user_id']
        answer_id = data['answer_id']
        answer = data['answer']

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.answer_edit(answer)

                if validation['status'] == "success":
                    answer_query = Answers.query.filter(Answers.id == answer_id).first()

                    if answer != answer_query.answer:

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
                        history_payload = AnswersHistory(
                            answer_id=answer_query.id,
                            answer=answer_query.answer,
                            answer_detect_lang=answer_query.answer_detect_lang
                        )
                        history_payload.answers_history_backref.append(answer_query)
                        history_payload.db_post()

                        # End History

                        answer_query.answer = answer
                        answer_query.question_detect_lang = answer_detect_lang
                        answer_query.editing = True
                        answer_query.db_post()

                        user = User.query.filter_by(id=user_id).first()

                        answer_sender_user = User.query.filter(User.id == user.id).first()
                        sender_last_name = None
                        answer_sender_user_id = None
                        if answer_sender_user is not None:
                            answer_sender_user_id = answer_sender_user.id
                            for billing_information in itertools.product(answer_sender_user.billing_information):
                                for sender in billing_information:
                                    sender_last_name = sender.last_name

                        answer_data = {
                            "question_id": answer_query.question_id,
                            "id": answer_query.id,
                            "answer": answer_query.answer,
                            "answer_detect_lang": answer_query.answer_detect_lang,
                            "sender_last_name": sender_last_name,
                            "sender_id": answer_sender_user_id,
                            "created_at": answer_query.created_at,
                            "updated_at": answer_query.updated_at,
                            "is_editing": answer_query.editing
                        }

                        data = {"status": 'success', "answer_data": answer_data}
                        return make_response(jsonify(data), 200)
                    else:
                        data = {"status": 'success'}
                        return make_response(jsonify(data), 201)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(PostQuestion, '/post-question')
api.add_resource(PostAnswer, '/post-answer')
api.add_resource(QuestionDelete, '/question-delete')
api.add_resource(QuestionEdit, '/question-edit')
api.add_resource(AnswerDelete, '/answer-delete')
api.add_resource(AnswerEdit, '/answer-edit')

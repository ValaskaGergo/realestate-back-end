# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from app.models.models import Translate, Animal, TranslateTalking, SubCategory
from sqlalchemy import or_, and_, desc, asc, func
import deepl

mod = Blueprint('translate_module', __name__)
api = Api(mod)

translate_data = reqparse.RequestParser()
translate_data.add_argument('source', required=True)
translate_data.add_argument('target', required=True)
translate_data.add_argument('source_data', required=True)
translate_data.add_argument('translate_type')
translate_data.add_argument('translate_type_id')
translate_data.add_argument('translate_type_data')


class GetTranslate(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = translate_data.parse_args()

        source = data['source'].upper()  # EN
        target = data['target'].upper()  # HU
        source_data = data['source_data']  # Lorem ipsum dolor...
        translate_type = data['translate_type']  # full
        translate_type_id = int(data['translate_type_id'])  # 1
        translate_type_data = data['translate_type_data']  # briefDescription

        if api_key == app.config['API_KEY']:
            try:
                if translate_type == "full":
                    translate_query = Translate.query \
                        .filter(and_
                                (Translate.translate_type == "full", Translate.translate_type_id == translate_type_id,
                                 Translate.translate_type_data == translate_type_data, Translate.source == source,
                                 Translate.target == target, Translate.source_data == source_data)) \
                        .first()

                    if translate_query is not None:
                        result = translate_query.target_data
                    else:
                        auth_key = app.config['DEEPL_API_KEY']
                        translator = deepl.Translator(auth_key)

                        if source == "EN":
                            source_code = "EN-GB"
                        elif source == "PT":
                            source_code = "PT-PT"
                        else:
                            source_code = source

                        result = translator.translate_text(source_data, target_lang=source_code)
                        result = result.text

                        translate_payload = Translate(source=source, target=target, source_data=source_data,
                                                      target_data=result)
                        animal_query = Animal.query.filter(Animal.id == translate_type_id).first()
                        translate_payload.translate_backref.append(animal_query)
                        translate_payload.db_post()

                        translate_payload.translate_type = translate_type
                        translate_payload.translate_type_id = translate_type_id
                        translate_payload.translate_type_data = translate_type_data
                        translate_payload.db_post()

                    data = {"status": 'success', "source_data": source_data, "target_data": result}
                    return make_response(jsonify(data), 200)

                if translate_type == "talking":
                    translate_query = TranslateTalking.query \
                        .filter(and_
                                (TranslateTalking.translate_type == "talking",
                                 TranslateTalking.translate_type_id == translate_type_id,
                                 TranslateTalking.translate_type_data == translate_type_data,
                                 TranslateTalking.source == source,
                                 TranslateTalking.target == target, TranslateTalking.source_data == source_data)) \
                        .first()

                    if translate_query is not None:
                        app.logger.info("db")
                        result = translate_query.target_data
                    else:
                        app.logger.info("deepl")
                        auth_key = app.config['DEEPL_API_KEY']
                        translator = deepl.Translator(auth_key)

                        if source == "EN":
                            source_code = "EN-GB"
                        elif source == "PT":
                            source_code = "PT-PT"
                        else:
                            source_code = source

                        result = translator.translate_text(source_data, target_lang=source_code)
                        result = result.text

                        translate_payload = TranslateTalking(source=source, target=target, source_data=source_data,
                                                             target_data=result)
                        subcategory_query = SubCategory.query.filter(SubCategory.id == translate_type_id).first()
                        translate_payload.translate_talking_backref.append(subcategory_query)
                        translate_payload.db_post()

                        translate_payload.translate_type = translate_type
                        translate_payload.translate_type_id = translate_type_id
                        translate_payload.translate_type_data = translate_type_data
                        translate_payload.db_post()

                    data = {"status": 'success', "source_data": source_data, "target_data": result}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(GetTranslate, '/translate')

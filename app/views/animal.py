# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify, json
from flask_restful import Api, reqparse, Resource
from app.models.models import User, Animal, AnimalPhotos, AnimalVideos, Category, SubCategory, AnimalPDF, \
    UserPermission, UserProfile
from .utilities.validators import Validation
from datetime import datetime
from dateutil import relativedelta
import detectlanguage
from dateutil.parser import parse
import math
from sqlalchemy import desc
from .utilities.utility import Pagination, StringToList, VerificationCode
from slugify import slugify
import itertools

mod = Blueprint('animal_module', __name__)
api = Api(mod)

detectlanguage.configuration.api_key = app.config['DETECT_LANGUAGE_KEY']
detectlanguage.configuration.secure = True

uploading_animal = reqparse.RequestParser()
uploading_animal.add_argument('last_modification_user_email', required=True)
uploading_animal.add_argument('email', required=True)
uploading_animal.add_argument('animal_id', required=False)
uploading_animal.add_argument('category_id', required=False)
uploading_animal.add_argument('subcategory_id', required=False)
uploading_animal.add_argument('name', required=False)
uploading_animal.add_argument('age_year', required=False)
uploading_animal.add_argument('age_month', required=False)
uploading_animal.add_argument('age_day', required=False)
uploading_animal.add_argument('region_origin', required=False)
uploading_animal.add_argument('country_origin', required=False)
uploading_animal.add_argument('region_residence', required=False)
uploading_animal.add_argument('country_residence', required=False)
uploading_animal.add_argument('is_be_used_for', required=False)
uploading_animal.add_argument('be_used_for_hu', required=False)
uploading_animal.add_argument('be_used_for_en', required=False)
uploading_animal.add_argument('be_used_for_de', required=False)
uploading_animal.add_argument('be_used_for_fr', required=False)
uploading_animal.add_argument('be_used_for_es', required=False)
uploading_animal.add_argument('is_gender', required=False)
uploading_animal.add_argument('gender_hu', required=False)
uploading_animal.add_argument('gender_en', required=False)
uploading_animal.add_argument('gender_de', required=False)
uploading_animal.add_argument('gender_fr', required=False)
uploading_animal.add_argument('gender_es', required=False)
uploading_animal.add_argument('is_color', required=False)
uploading_animal.add_argument('color_hu', required=False)
uploading_animal.add_argument('color_en', required=False)
uploading_animal.add_argument('color_de', required=False)
uploading_animal.add_argument('color_fr', required=False)
uploading_animal.add_argument('color_es', required=False)
uploading_animal.add_argument('brief_description', required=False)
uploading_animal.add_argument('description', required=False)
uploading_animal.add_argument('mother', required=False)
uploading_animal.add_argument('mother_mother', required=False)
uploading_animal.add_argument('mother_mother_mother', required=False)
uploading_animal.add_argument('mother_mother_father', required=False)
uploading_animal.add_argument('mother_father', required=False)
uploading_animal.add_argument('mother_father_mother', required=False)
uploading_animal.add_argument('mother_father_father', required=False)
uploading_animal.add_argument('father', required=False)
uploading_animal.add_argument('father_mother', required=False)
uploading_animal.add_argument('father_mother_mother', required=False)
uploading_animal.add_argument('father_mother_father', required=False)
uploading_animal.add_argument('father_father', required=False)
uploading_animal.add_argument('father_father_mother', required=False)
uploading_animal.add_argument('father_father_father', required=False)
uploading_animal.add_argument('img_01_data', required=False)
uploading_animal.add_argument('img_02_data', required=False)
uploading_animal.add_argument('img_03_data', required=False)
uploading_animal.add_argument('img_04_data', required=False)
uploading_animal.add_argument('img_05_data', required=False)
uploading_animal.add_argument('img_06_data', required=False)
uploading_animal.add_argument('img_07_data', required=False)
uploading_animal.add_argument('img_08_data', required=False)
uploading_animal.add_argument('img_09_data', required=False)
uploading_animal.add_argument('img_10_data', required=False)
uploading_animal.add_argument('img_01_data_old', required=False)
uploading_animal.add_argument('img_02_data_old', required=False)
uploading_animal.add_argument('img_03_data_old', required=False)
uploading_animal.add_argument('img_04_data_old', required=False)
uploading_animal.add_argument('img_05_data_old', required=False)
uploading_animal.add_argument('img_06_data_old', required=False)
uploading_animal.add_argument('img_07_data_old', required=False)
uploading_animal.add_argument('img_08_data_old', required=False)
uploading_animal.add_argument('img_09_data_old', required=False)
uploading_animal.add_argument('img_10_data_old', required=False)
uploading_animal.add_argument('img_01_status', required=False)
uploading_animal.add_argument('img_02_status', required=False)
uploading_animal.add_argument('img_03_status', required=False)
uploading_animal.add_argument('img_04_status', required=False)
uploading_animal.add_argument('img_05_status', required=False)
uploading_animal.add_argument('img_06_status', required=False)
uploading_animal.add_argument('img_07_status', required=False)
uploading_animal.add_argument('img_08_status', required=False)
uploading_animal.add_argument('img_09_status', required=False)
uploading_animal.add_argument('img_10_status', required=False)

uploading_animal.add_argument('video_01_data', required=False)
uploading_animal.add_argument('url_01', required=False)
uploading_animal.add_argument('url_02', required=False)
uploading_animal.add_argument('medical_paper_data', required=False)
uploading_animal.add_argument('medical_paper_data_old', required=False)
uploading_animal.add_argument('medical_paper_status', required=False)
uploading_animal.add_argument('breed_registry_data', required=False)
uploading_animal.add_argument('breed_registry_data_old', required=False)
uploading_animal.add_argument('breed_registry_status', required=False)
uploading_animal.add_argument('x_ray_data', required=False)
uploading_animal.add_argument('x_ray_data_old', required=False)
uploading_animal.add_argument('x_ray_status', required=False)
uploading_animal.add_argument('price', required=False)

list_of_uploaded_animals = reqparse.RequestParser()
list_of_uploaded_animals.add_argument('email', required=True)
list_of_uploaded_animals.add_argument('page_number', required=True)

edit_of_uploaded_animal = reqparse.RequestParser()
edit_of_uploaded_animal.add_argument('email', required=True)
edit_of_uploaded_animal.add_argument('animal_id', required=True)

uploading_animal_only_images_video = reqparse.RequestParser()
uploading_animal_only_images_video.add_argument('video_id', required=True)
uploading_animal_only_images_video.add_argument('video_folder', required=True)

del_of_uploaded_animal = reqparse.RequestParser()
del_of_uploaded_animal.add_argument('worker_email', required=True)
del_of_uploaded_animal.add_argument('user_email', required=True)
del_of_uploaded_animal.add_argument('animal_id', required=True)

visibility_of_uploaded_animal = reqparse.RequestParser()
visibility_of_uploaded_animal.add_argument('worker_email', required=True)
visibility_of_uploaded_animal.add_argument('user_email', required=True)
visibility_of_uploaded_animal.add_argument('animal_id', required=True)
visibility_of_uploaded_animal.add_argument('btn', required=True)

youtube_upload_data = reqparse.RequestParser()
youtube_upload_data.add_argument('animal_id')

youtube_id_data = reqparse.RequestParser()
youtube_id_data.add_argument('animal_id')
youtube_id_data.add_argument('youtube_video_id')


class UploadingAnimal(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = uploading_animal.parse_args()
        app.logger.info(data)

        last_modification_user_email = data['last_modification_user_email']
        email = data['email']
        animal_id = data['animal_id']
        category_id = data['category_id']
        subcategory_id = data['subcategory_id']
        name = data['name']
        age_year = data['age_year']
        age_month = data['age_month']
        age_day = data['age_day']
        region_origin = data['region_origin']
        country_origin = data['country_origin']
        region_residence = data['region_residence']
        country_residence = data['country_residence']
        is_be_used_for = data['is_be_used_for']
        be_used_for_hu = data['be_used_for_hu']
        be_used_for_en = data['be_used_for_en']
        be_used_for_de = data['be_used_for_de']
        be_used_for_fr = data['be_used_for_fr']
        be_used_for_es = data['be_used_for_es']
        is_gender = data['is_gender']
        gender_hu = data['gender_hu']
        gender_en = data['gender_en']
        gender_de = data['gender_de']
        gender_fr = data['gender_fr']
        gender_es = data['gender_es']
        is_color = data['is_color']
        color_hu = data['color_hu']
        color_en = data['color_en']
        color_de = data['color_de']
        color_fr = data['color_fr']
        color_es = data['color_es']
        brief_description = data['brief_description']
        description = data['description']
        mother = data['mother']
        mother_mother = data['mother_mother']
        mother_mother_mother = data['mother_mother_mother']
        mother_mother_father = data['mother_mother_father']
        mother_father = data['mother_father']
        mother_father_mother = data['mother_father_mother']
        mother_father_father = data['mother_father_father']
        father = data['father']
        father_mother = data['father_mother']
        father_mother_mother = data['father_mother_mother']
        father_mother_father = data['father_mother_father']
        father_father = data['father_father']
        father_father_mother = data['father_father_mother']
        father_father_father = data['father_father_father']
        img_01_data = data['img_01_data']
        img_02_data = data['img_02_data']
        img_03_data = data['img_03_data']
        img_04_data = data['img_04_data']
        img_05_data = data['img_05_data']
        img_06_data = data['img_06_data']
        img_07_data = data['img_07_data']
        img_08_data = data['img_08_data']
        img_09_data = data['img_09_data']
        img_10_data = data['img_10_data']
        img_01_data_old = data['img_01_data_old']
        img_02_data_old = data['img_02_data_old']
        img_03_data_old = data['img_03_data_old']
        img_04_data_old = data['img_04_data_old']
        img_05_data_old = data['img_05_data_old']
        img_06_data_old = data['img_06_data_old']
        img_07_data_old = data['img_07_data_old']
        img_08_data_old = data['img_08_data_old']
        img_09_data_old = data['img_09_data_old']
        img_10_data_old = data['img_10_data_old']
        img_01_status = data['img_01_status']
        img_02_status = data['img_02_status']
        img_03_status = data['img_03_status']
        img_04_status = data['img_04_status']
        img_05_status = data['img_05_status']
        img_06_status = data['img_06_status']
        img_07_status = data['img_07_status']
        img_08_status = data['img_08_status']
        img_09_status = data['img_09_status']
        img_10_status = data['img_10_status']
        video_01_data = data['video_01_data']
        url_01 = data['url_01']
        url_02 = data['url_02']
        medical_paper_data = data['medical_paper_data']
        medical_paper_data_old = data['medical_paper_data_old']
        medical_paper_status = data['medical_paper_status']
        breed_registry_data = data['breed_registry_data']
        breed_registry_data_old = data['breed_registry_data_old']
        breed_registry_status = data['breed_registry_status']
        x_ray_data = data['x_ray_data']
        x_ray_data_old = data['x_ray_data_old']
        x_ray_status = data['x_ray_status']
        price = data['price'].replace(" ", "")

        if api_key == app.config['API_KEY']:
            try:
                validation = Validation.uploading_animal(category_id, subcategory_id, name, age_year,
                                                         age_month, age_day, country_origin, country_residence,
                                                         is_be_used_for,
                                                         be_used_for_hu, be_used_for_en, be_used_for_de, be_used_for_fr,
                                                         be_used_for_es, is_gender, gender_hu,
                                                         gender_en, gender_de, gender_fr, gender_es, is_color, color_hu,
                                                         color_en, color_de, color_fr, color_es, brief_description,
                                                         description, mother,
                                                         mother_mother, mother_mother_mother, mother_mother_father,
                                                         mother_father, mother_father_mother, mother_father_father,
                                                         father, father_mother, father_mother_mother,
                                                         father_mother_father, father_father, father_father_mother,
                                                         father_father_father, img_01_data, img_02_data, img_03_data,
                                                         img_04_data, video_01_data, url_01, url_02, medical_paper_data,
                                                         breed_registry_data, x_ray_data, price)
                if validation['status'] == "success":

                    is_editing = None

                    user = User.query.filter_by(email=email).first()
                    user_permission = UserPermission.query.join(User.permission).filter(User.id == user.id).first()
                    last_modification_user = User.query.filter_by(email=last_modification_user_email).first()

                    last_modification_user_profile = UserProfile \
                        .query.join(User.profile) \
                        .filter(User.id == last_modification_user.id).first()

                    try:
                        today = datetime.now()
                        date1 = datetime(int(age_year), int(age_month), int(age_day))
                        date2 = today
                        diff = relativedelta.relativedelta(date2, date1)
                        years = diff.years
                        months = diff.months
                        days = diff.days
                    except:
                        years = 0
                        months = 0
                        days = 0

                    if bool(description and description.strip()):
                        detectlanguage_status = detectlanguage.user_status()

                        if detectlanguage_status['status'] == "ACTIVE":
                            lang = detectlanguage.detect(description)

                            if lang[0]['language']:
                                description_detect_lang = lang[0]['language']
                            else:
                                description_detect_lang = None
                        else:
                            description_detect_lang = None
                    else:
                        description_detect_lang = None

                    if bool(brief_description and brief_description.strip()):
                        detectlanguage_status = detectlanguage.user_status()

                        if detectlanguage_status['status'] == "ACTIVE":
                            lang = detectlanguage.detect(brief_description)

                            if lang[0]['language']:
                                brief_description_detect_lang = lang[0]['language']
                            else:
                                brief_description_detect_lang = None
                        else:
                            brief_description_detect_lang = None
                    else:
                        brief_description_detect_lang = None

                    if img_01_status == "rm":
                        img_01_data = None
                        img_01 = None
                    elif img_01_status == "editing":
                        img_01_data_json = json.loads(img_01_data)
                        img_01 = img_01_data_json['filename']
                    elif img_01_status is None or img_01_status == "" or img_01_status == "new" or img_01_status == "unchanged":
                        if img_01_data:
                            img_01_data_json = json.loads(img_01_data)
                            img_01 = img_01_data_json['filename']
                        else:
                            img_01_data = None
                            img_01 = None
                    else:
                        img_01_data = None
                        img_01 = None

                    if img_02_status == "rm":
                        img_02_data = None
                        img_02 = None
                    elif img_02_status == "editing":
                        img_02_data_json = json.loads(img_02_data)
                        img_02 = img_02_data_json['filename']
                    elif img_02_status is None or img_02_status == "" or img_02_status == "new" or img_02_status == "unchanged":
                        if img_02_data:
                            img_02_data_json = json.loads(img_02_data)
                            img_02 = img_02_data_json['filename']
                        else:
                            img_02_data = None
                            img_02 = None
                    else:
                        img_02_data = None
                        img_02 = None

                    if img_03_status == "rm":
                        img_03_data = None
                        img_03 = None
                    elif img_03_status == "editing":
                        img_03_data_json = json.loads(img_03_data)
                        img_03 = img_03_data_json['filename']
                    elif img_03_status is None or img_03_status == "" or img_03_status == "new" or img_03_status == "unchanged":
                        if img_03_data:
                            img_03_data_json = json.loads(img_03_data)
                            img_03 = img_03_data_json['filename']
                        else:
                            img_03_data = None
                            img_03 = None
                    else:
                        img_03_data = None
                        img_03 = None

                    if img_04_status == "rm":
                        img_04_data = None
                        img_04 = None
                    elif img_04_status == "editing":
                        img_04_data_json = json.loads(img_04_data)
                        img_04 = img_04_data_json['filename']
                    elif img_04_status is None or img_04_status == "" or img_04_status == "new" or img_04_status == "unchanged":
                        if img_04_data:
                            img_04_data_json = json.loads(img_04_data)
                            img_04 = img_04_data_json['filename']
                        else:
                            img_04_data = None
                            img_04 = None
                    else:
                        img_04_data = None
                        img_04 = None

                    if img_05_status == "rm":
                        img_05_data = None
                        img_05 = None
                    elif img_05_status == "editing":
                        img_05_data_json = json.loads(img_05_data)
                        img_05 = img_05_data_json['filename']
                    elif img_05_status is None or img_05_status == "" or img_05_status == "new" or img_05_status == "unchanged":
                        if img_05_data:
                            img_05_data_json = json.loads(img_05_data)
                            img_05 = img_05_data_json['filename']
                        else:
                            img_05_data = None
                            img_05 = None
                    else:
                        img_05_data = None
                        img_05 = None

                    if img_06_status == "rm":
                        img_06_data = None
                        img_06 = None
                    elif img_06_status == "editing":
                        img_06_data_json = json.loads(img_06_data)
                        img_06 = img_06_data_json['filename']
                    elif img_06_status is None or img_06_status == "" or img_06_status == "new" or img_06_status == "unchanged":
                        if img_06_data:
                            img_06_data_json = json.loads(img_06_data)
                            img_06 = img_06_data_json['filename']
                        else:
                            img_06_data = None
                            img_06 = None
                    else:
                        img_06_data = None
                        img_06 = None

                    if img_07_status == "rm":
                        img_07_data = None
                        img_07 = None
                    elif img_07_status == "editing":
                        img_07_data_json = json.loads(img_07_data)
                        img_07 = img_07_data_json['filename']
                    elif img_07_status is None or img_07_status == "" or img_07_status == "new" or img_07_status == "unchanged":
                        if img_07_data:
                            img_07_data_json = json.loads(img_07_data)
                            img_07 = img_07_data_json['filename']
                        else:
                            img_07_data = None
                            img_07 = None
                    else:
                        img_07_data = None
                        img_07 = None

                    if img_08_status == "rm":
                        img_08_data = None
                        img_08 = None
                    elif img_08_status == "editing":
                        img_08_data_json = json.loads(img_08_data)
                        img_08 = img_08_data_json['filename']
                    elif img_08_status is None or img_08_status == "" or img_08_status == "new" or img_08_status == "unchanged":
                        if img_08_data:
                            img_08_data_json = json.loads(img_08_data)
                            img_08 = img_08_data_json['filename']
                        else:
                            img_08_data = None
                            img_08 = None
                    else:
                        img_08_data = None
                        img_08 = None

                    if img_09_status == "rm":
                        img_09_data = None
                        img_09 = None
                    elif img_09_status == "editing":
                        img_09_data_json = json.loads(img_09_data)
                        img_09 = img_09_data_json['filename']
                    elif img_09_status is None or img_09_status == "" or img_09_status == "new" or img_09_status == "unchanged":
                        if img_09_data:
                            img_09_data_json = json.loads(img_09_data)
                            img_09 = img_09_data_json['filename']
                        else:
                            img_09_data = None
                            img_09 = None
                    else:
                        img_09_data = None
                        img_09 = None

                    if img_10_status == "rm":
                        img_10_data = None
                        img_10 = None
                    elif img_10_status == "editing":
                        img_10_data_json = json.loads(img_10_data)
                        img_10 = img_10_data_json['filename']
                    elif img_10_status is None or img_10_status == "" or img_10_status == "new" or img_10_status == "unchanged":
                        if img_10_data:
                            img_10_data_json = json.loads(img_10_data)
                            img_10 = img_10_data_json['filename']
                        else:
                            img_10_data = None
                            img_10 = None
                    else:
                        img_10_data = None
                        img_10 = None

                    if video_01_data:
                        video_01_data_json = json.loads(video_01_data)
                        video_01 = video_01_data_json['filename']
                    else:
                        video_01_data = None
                        video_01 = None

                    if medical_paper_status == "rm":
                        medical_paper_data = None
                        medical_paper = None
                    elif medical_paper_status is None or medical_paper_status == "" or medical_paper_status == "new" or medical_paper_status == "unchanged":
                        if medical_paper_data:
                            medical_paper_data_json = json.loads(medical_paper_data)
                            medical_paper = medical_paper_data_json['filename']
                        else:
                            medical_paper_data = None
                            medical_paper = None
                    else:
                        medical_paper_data = None
                        medical_paper = None

                    if breed_registry_status == "rm":
                        breed_registry_data = None
                        breed_registry = None
                    elif breed_registry_status is None or breed_registry_status == "" or breed_registry_status == "new" or breed_registry_status == "unchanged":
                        if breed_registry_data:
                            breed_registry_data_json = json.loads(breed_registry_data)
                            breed_registry = breed_registry_data_json['filename']
                        else:
                            breed_registry_data = None
                            breed_registry = None
                    else:
                        breed_registry_data = None
                        breed_registry = None

                    if x_ray_status == "rm":
                        x_ray_data = None
                        x_ray = None
                    elif x_ray_status is None or x_ray_status == "" or x_ray_status == "new" or x_ray_status == "unchanged":
                        if x_ray_data:
                            x_ray_data_json = json.loads(x_ray_data)
                            x_ray = x_ray_data_json['filename']
                        else:
                            x_ray_data = None
                            x_ray = None
                    else:
                        x_ray_data = None
                        x_ray = None

                    if user is not None:

                        if animal_id is None or animal_id == "":
                            is_editing = "False"
                            aid = str(VerificationCode.generate_timestamp_pin()) + str(VerificationCode.generate_pin(2))
                            animal_payload = Animal(
                                user_id=user.id,
                                advertisement_id=int(aid),
                                category_id=category_id,
                                subcategory_id=subcategory_id,
                                name=name,
                                age_year=age_year,
                                age_month=age_month,
                                age_day=age_day,
                                years=years,
                                months=months,
                                days=days,
                                region_origin=region_origin,
                                country_origin=country_origin,
                                region_residence=region_residence,
                                country_residence=country_residence,
                                be_used_for_hu=be_used_for_hu,
                                be_used_for_en=be_used_for_en,
                                be_used_for_de=be_used_for_de,
                                be_used_for_fr=be_used_for_fr,
                                be_used_for_es=be_used_for_es,
                                gender_hu=gender_hu,
                                gender_en=gender_en,
                                gender_de=gender_de,
                                gender_fr=gender_fr,
                                gender_es=gender_es,
                                color_hu=color_hu,
                                color_en=color_en,
                                color_de=color_de,
                                color_fr=color_fr,
                                color_es=color_es,
                                brief_description=brief_description,
                                brief_description_detect_lang=brief_description_detect_lang,
                                description=description,
                                description_detect_lang=description_detect_lang,
                                mother=mother,
                                mother_mother=mother_mother,
                                mother_mother_mother=mother_mother_mother,
                                mother_mother_father=mother_mother_father,
                                mother_father=mother_father,
                                mother_father_mother=mother_father_mother,
                                mother_father_father=mother_father_father,
                                father=father,
                                father_mother=father_mother,
                                father_mother_mother=father_mother_mother,
                                father_mother_father=father_mother_father,
                                father_father=father_father,
                                father_father_mother=father_father_mother,
                                father_father_father=father_father_father,
                                page_url=None,
                                url_01=url_01,
                                url_02=url_02,
                                price=price,

                                last_modification_user_id=last_modification_user.id,
                                last_modification_user_name=last_modification_user_profile.username
                            )
                            animal_payload.animal_backref.append(user)
                            animal_payload.db_post()
                            animal_id = animal_payload.id

                            animal_photo_payload = AnimalPhotos(
                                user_id=user.id,
                                animal_id=animal_payload.id,
                                img_01=img_01,
                                img_01_data=img_01_data,
                                img_02=img_02,
                                img_02_data=img_02_data,
                                img_03=img_03,
                                img_03_data=img_03_data,
                                img_04=img_04,
                                img_04_data=img_04_data,
                                img_05=img_05,
                                img_05_data=img_05_data,
                                img_06=img_06,
                                img_06_data=img_06_data,
                                img_07=img_07,
                                img_07_data=img_07_data,
                                img_08=img_08,
                                img_08_data=img_08_data,
                                img_09=img_09,
                                img_09_data=img_09_data,
                                img_10=img_10,
                                img_10_data=img_10_data,
                            )
                            animal_photo_payload.animal_photos_backref.append(animal_payload)
                            animal_photo_payload.db_post()

                            animal_video_payload = AnimalVideos(
                                user_id=user.id,
                                animal_id=animal_payload.id,
                                video_01=video_01,
                                video_01_data=video_01_data
                            )
                            animal_video_payload.animal_videos_backref.append(animal_payload)
                            animal_video_payload.db_post()

                            animal_pdf_payload = AnimalPDF(
                                user_id=user.id,
                                animal_id=animal_payload.id,
                                medical_paper=medical_paper,
                                medical_paper_data=medical_paper_data,
                                breed_registry=breed_registry,
                                breed_registry_data=breed_registry_data,
                                x_ray=x_ray,
                                x_ray_data=x_ray_data
                            )
                            animal_pdf_payload.animal_pdf_backref.append(animal_payload)
                            animal_pdf_payload.db_post()

                            animal_payload.page_url = slugify(name)
                            animal_payload.db_post()

                            user_permission.subscribed_ads -= 1
                            user_permission.db_post()
                        else:
                            is_editing = "True"
                            animal_query = Animal.query.filter_by(id=animal_id).first()

                            animal_query.category_id = category_id
                            animal_query.subcategory_id = subcategory_id
                            animal_query.name = name
                            animal_query.age_year = age_year
                            animal_query.age_month = age_month
                            animal_query.age_day = age_day
                            animal_query.years = years
                            animal_query.months = months
                            animal_query.days = days
                            animal_query.region_origin = region_origin
                            animal_query.country_origin = country_origin
                            animal_query.region_residence = region_residence
                            animal_query.country_residence = country_residence
                            animal_query.be_used_for_hu = be_used_for_hu
                            animal_query.be_used_for_en = be_used_for_en
                            animal_query.be_used_for_de = be_used_for_de
                            animal_query.be_used_for_fr = be_used_for_fr
                            animal_query.be_used_for_es = be_used_for_es
                            animal_query.gender_hu = gender_hu
                            animal_query.gender_en = gender_en
                            animal_query.gender_de = gender_de
                            animal_query.gender_fr = gender_fr
                            animal_query.gender_es = gender_es
                            animal_query.color_hu = color_hu
                            animal_query.color_en = color_en
                            animal_query.color_de = color_de
                            animal_query.color_fr = color_fr
                            animal_query.color_es = color_es
                            animal_query.brief_description = brief_description
                            animal_query.brief_description_detect_lang = brief_description_detect_lang
                            animal_query.description = description
                            animal_query.description_detect_lang = description_detect_lang
                            animal_query.mother = mother
                            animal_query.mother_mother = mother_mother
                            animal_query.mother_mother_mother = mother_mother_mother
                            animal_query.mother_mother_father = mother_mother_father
                            animal_query.mother_father = mother_father
                            animal_query.mother_father_mother = mother_father_mother
                            animal_query.mother_father_father = mother_father_father
                            animal_query.father = father
                            animal_query.father_mother = father_mother
                            animal_query.father_mother_mother = father_mother_mother
                            animal_query.father_mother_father = father_mother_father
                            animal_query.father_father = father_father
                            animal_query.father_father_mother = father_father_mother
                            animal_query.father_father_father = father_father_father
                            animal_query.page_url = slugify(name)
                            animal_query.url_01 = url_01
                            animal_query.url_02 = url_02
                            animal_query.price = price
                            animal_query.last_modification_user_id = last_modification_user.id,
                            animal_query.last_modification_user_name = last_modification_user_profile.username
                            animal_query.db_post()
                            animal_id = animal_query.id

                            animal_photo_query = AnimalPhotos \
                                .query.join(Animal.photos) \
                                .filter(Animal.id == animal_query.id).first()

                            animal_photo_query.img_01 = img_01
                            animal_photo_query.img_01_data = img_01_data
                            animal_photo_query.img_02 = img_02
                            animal_photo_query.img_02_data = img_02_data
                            animal_photo_query.img_03 = img_03
                            animal_photo_query.img_03_data = img_03_data
                            animal_photo_query.img_04 = img_04
                            animal_photo_query.img_04_data = img_04_data
                            animal_photo_query.img_05 = img_05
                            animal_photo_query.img_05_data = img_05_data
                            animal_photo_query.img_06 = img_06
                            animal_photo_query.img_06_data = img_06_data
                            animal_photo_query.img_07 = img_07
                            animal_photo_query.img_07_data = img_07_data
                            animal_photo_query.img_08 = img_08
                            animal_photo_query.img_08_data = img_08_data
                            animal_photo_query.img_09 = img_09
                            animal_photo_query.img_09_data = img_09_data
                            animal_photo_query.img_10 = img_10
                            animal_photo_query.img_10_data = img_10_data
                            animal_photo_query.db_post()

                            animal_video_payload = AnimalVideos \
                                .query.join(Animal.videos) \
                                .filter(Animal.id == animal_query.id).first()

                            animal_video_payload.video_01 = video_01
                            animal_video_payload.video_01_data = video_01_data
                            animal_video_payload.db_post()

                            animal_pdf_payload = AnimalPDF \
                                .query.join(Animal.pdf) \
                                .filter(Animal.id == animal_query.id).first()

                            animal_pdf_payload.medical_paper = medical_paper,
                            animal_pdf_payload.medical_paper_data = medical_paper_data,
                            animal_pdf_payload.breed_registry = breed_registry,
                            animal_pdf_payload.breed_registry_data = breed_registry_data,
                            animal_pdf_payload.x_ray = x_ray,
                            animal_pdf_payload.x_ray_data = x_ray_data
                            animal_pdf_payload.db_post()

                        data = {"status": 'success', 'animal_video_id': animal_video_payload.id,
                                'video_01_data': video_01_data, "medical_paper_data": medical_paper_data,
                                "breed_registry_data": breed_registry_data, "x_ray_data": x_ray_data,
                                "is_editing": is_editing, "animal_id": animal_id}
                        return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(validation), 400)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class ListOfUploadedAnimals(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = list_of_uploaded_animals.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                page_number = int(data['page_number'])
                animals_limit = 10
                offset_number = (page_number * animals_limit) - animals_limit

                animal_query_count = Animal.query.filter_by(user_id=user.id).count()
                pagination_count = math.ceil(animal_query_count / animals_limit)
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
                    "animals_count": int(animal_query_count),
                    "pagination_count": int(pagination_count),
                    "pagination_first": int(pagination_first),
                    "pagination_last": int(pagination_last),
                    "pagination_next": int(pagination_next),
                    "pagination_previous": int(pagination_previous)
                }

                category_query = Category.query.all()
                subcategory_query = SubCategory.query.all()

                animals_list = []
                photo_item = {}
                video_item = {}
                pdf_item = {}
                category_item = {}
                subcategory_item = {}

                if user is not None:
                    for animal in user.animal.order_by(desc(Animal.created_at)).offset(offset_number).limit(
                            animals_limit):
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
                                "medical_paper": pdf.medical_paper,
                                "breed_registry": pdf.breed_registry,
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
                                "height": animal.height,
                                "age_year": animal.age_year,
                                "age_month": animal.age_month,
                                "age_day": animal.age_day,
                                "years": animal.years,
                                "months": animal.months,
                                "days": animal.days,
                                "region_origin": animal.region_origin,
                                "country_origin": animal.country_origin,
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
                                "mother": animal.mother,
                                "mother_mother": animal.mother_mother,
                                "mother_mother_mother": animal.mother_mother_mother,
                                "mother_mother_father": animal.mother_mother_father,
                                "mother_father": animal.mother_father,
                                "mother_father_mother": animal.mother_father_mother,
                                "mother_father_father": animal.mother_father_father,
                                "father": animal.father,
                                "father_mother": animal.father_mother,
                                "father_mother_mother": animal.father_mother_mother,
                                "father_mother_father": animal.father_mother_father,
                                "father_father": animal.father_father,
                                "father_father_mother": animal.father_father_mother,
                                "father_father_father": animal.father_father_father,
                                "page_url": animal.page_url,
                                "url_01": animal.url_01,
                                "url_02": animal.url_02,
                                "price": animal.price,
                                "visibility": animal.visibility,
                                "worker_visibility": animal.worker_visibility,
                                "created_at": animal.created_at,
                                "updated_at": animal.updated_at
                            },
                            "photo": photo_item,
                            "video": video_item,
                            "pdf": pdf_item,
                            "category": category_item,
                            "subcategory": subcategory_item
                        }
                        animals_list.append(item)

                    data = {"pagination_list": pagination_list, "pagination": pagination,
                            "data": sorted(animals_list, key=lambda x: parse(str(x['animal']['updated_at'])),
                                           reverse=True)}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class EditOfUploadedAnimal(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = edit_of_uploaded_animal.parse_args()

        email = data['email']
        animal_id = data['animal_id']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                user_permission = UserPermission \
                    .query.join(User.permission) \
                    .filter(User.id == user.id).first()

                animal = Animal.query.filter_by(id=animal_id).first()

                original_user = User.query.filter_by(id=animal.user_id).first()

                if original_user is not None and \
                        original_user.id is animal.user_id or \
                        user_permission.is_user_management == "True":
                    category = Category.query.filter_by(id=animal.category_id).first()
                    subcategory = SubCategory.query.filter_by(id=animal.subcategory_id).first()

                    animals_list = []
                    photo_item = {}
                    video_item = {}
                    pdf_item = {}

                    for photo in animal.photos:
                        photo_item = {
                            "id": photo.id,
                            "img_01": photo.img_01,
                            "img_01_data": photo.img_01_data,
                            "img_02": photo.img_02,
                            "img_02_data": photo.img_02_data,
                            "img_03": photo.img_03,
                            "img_03_data": photo.img_03_data,
                            "img_04": photo.img_04,
                            "img_04_data": photo.img_04_data,
                            "img_05": photo.img_05,
                            "img_05_data": photo.img_05_data,
                            "img_06": photo.img_06,
                            "img_06_data": photo.img_06_data,
                            "img_07": photo.img_07,
                            "img_07_data": photo.img_07_data,
                            "img_08": photo.img_08,
                            "img_08_data": photo.img_08_data,
                            "img_09": photo.img_09,
                            "img_09_data": photo.img_09_data,
                            "img_10": photo.img_10,
                            "img_10_data": photo.img_10_data,
                            "created_at": photo.created_at,
                            "updated_at": photo.updated_at
                        }
                    for video in animal.videos:
                        video_item = {
                            "id": video.id,
                            "video_01": video.video_01,
                            "video_01_data": video.video_01_data,
                            "created_at": video.created_at,
                            "updated_at": video.updated_at
                        }
                    for pdf in animal.pdf:
                        pdf_item = {
                            "id": pdf.id,
                            "medical_paper": pdf.medical_paper,
                            "medical_paper_data": pdf.medical_paper_data,
                            "breed_registry": pdf.breed_registry,
                            "breed_registry_data": pdf.breed_registry_data,
                            "x_ray": pdf.x_ray,
                            "x_ray_data": pdf.x_ray_data,
                            "created_at": pdf.created_at,
                            "updated_at": pdf.updated_at
                        }
                    item = {
                        "animal": {
                            "id": animal.id,
                            "category_id": animal.category_id,
                            "subcategory_id": animal.subcategory_id,
                            "name": animal.name,
                            "height": animal.height,
                            "age_year": animal.age_year,
                            "age_month": animal.age_month,
                            "age_day": animal.age_day,
                            "years": animal.years,
                            "months": animal.months,
                            "days": animal.days,
                            "region_origin": animal.region_origin,
                            "country_origin": animal.country_origin,
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
                            "mother": animal.mother,
                            "mother_mother": animal.mother_mother,
                            "mother_mother_mother": animal.mother_mother_mother,
                            "mother_mother_father": animal.mother_mother_father,
                            "mother_father": animal.mother_father,
                            "mother_father_mother": animal.mother_father_mother,
                            "mother_father_father": animal.mother_father_father,
                            "father": animal.father,
                            "father_mother": animal.father_mother,
                            "father_mother_mother": animal.father_mother_mother,
                            "father_mother_father": animal.father_mother_father,
                            "father_father": animal.father_father,
                            "father_father_mother": animal.father_father_mother,
                            "father_father_father": animal.father_father_father,
                            "page_url": animal.page_url,
                            "url_01": animal.url_01,
                            "url_02": animal.url_02,
                            "price": animal.price,
                            "visibility": animal.visibility,
                            "worker_visibility": animal.worker_visibility,
                            "created_at": animal.created_at,
                            "updated_at": animal.updated_at
                        },
                        "photo": photo_item,
                        "video": video_item,
                        "pdf": pdf_item,
                        "category": {
                            "name_hu": category.name_hu,
                            "name_en": category.name_en,
                            "name_de": category.name_de,
                            "name_fr": category.name_fr,
                            "name_es": category.name_es,
                        },
                        "subcategory": {
                            "name_hu": subcategory.name_hu,
                            "name_en": subcategory.name_en,
                            "name_de": subcategory.name_de,
                            "name_fr": subcategory.name_fr,
                            "name_es": subcategory.name_es,
                        },
                        "user": {
                            "user_id": original_user.id,
                            "user_email": original_user.email
                        }
                    }
                    animals_list.append(item)

                    data = {
                        "data": sorted(animals_list, key=lambda x: parse(str(x['animal']['created_at'])), reverse=True)}
                    return make_response(jsonify(data), 200)
                else:
                    return make_response(jsonify(), 404)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class UploadingAnimalOnlyImagesVideo(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = uploading_animal_only_images_video.parse_args()

        video_id = int(data['video_id'])
        video_folder = str(data['video_folder'])

        if api_key == app.config['API_KEY']:
            try:
                video_payload = AnimalVideos.query.filter_by(id=video_id).first()

                vd = {
                    "data": "/static/videos/tmp/animal/" + video_folder + "/cropped/" + video_folder + ".mp4",
                    "folder": video_folder,
                    "filename": video_folder + ".mp4"
                }

                video_payload.video_01 = video_folder + ".mp4"
                video_payload.video_01_data = json.dumps(vd)

                video_payload.db_post()
                data = {"status": 'success'}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class DelOfUploadedAnimal(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = del_of_uploaded_animal.parse_args()

        worker_email = data['worker_email']
        user_email = data['user_email']
        animal_id = data['animal_id']

        if api_key == app.config['API_KEY']:
            try:
                worker_email_query = User.query.filter_by(email=worker_email).first()
                user_email_query = User.query.filter_by(email=user_email).first()
                user_permission = UserPermission.query.join(User.permission).filter(
                    User.id == user_email_query.id).first()

                worker_email_user_permission_query = UserPermission \
                    .query.join(User.permission) \
                    .filter(User.id == worker_email_query.id).first()

                if worker_email_query is not None and worker_email == user_email or \
                        worker_email_user_permission_query.is_user_management == "True":
                    animal_query = Animal.query.filter_by(id=animal_id).first()
                    if animal_query is not None:
                        is_worker = worker_email_user_permission_query.is_user_management

                        youtube_video_id = None
                        for video_query in itertools.product(animal_query.videos):
                            for video in video_query:
                                youtube_video_id = video.youtube_id

                        animal_query.deleted = True
                        animal_query.db_post()
                        user_permission.subscribed_ads += 1
                        user_permission.db_post()

                        data = {"status": 'success', "is_worker": is_worker, "user_id": user_email_query.id,
                                "youtube_video_id": youtube_video_id}
                        return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class InactivateOfUploadedAnimal(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = visibility_of_uploaded_animal.parse_args()

        worker_email = data['worker_email']
        user_email = data['user_email']
        animal_id = data['animal_id']
        btn = data['btn']

        if api_key == app.config['API_KEY']:
            try:
                worker_email_query = User.query.filter_by(email=worker_email).first()
                user_email_query = User.query.filter_by(email=user_email).first()

                worker_email_user_permission_query = UserPermission \
                    .query.join(User.permission) \
                    .filter(User.id == worker_email_query.id).first()

                if worker_email is not None:
                    animal_query = Animal.query.filter_by(id=animal_id).first()
                    is_worker = worker_email_user_permission_query.is_user_management
                    if animal_query is not None:
                        if worker_email == user_email:
                            animal_query.visibility = "False"
                        if worker_email != user_email:
                            if is_worker == "True":
                                if btn == "btn02_01":
                                    animal_query.visibility = "False"
                                if btn == "btn02_02":
                                    animal_query.visibility = "False"
                                    animal_query.worker_visibility = "False"
                        animal_query.db_post()

                        youtube_video_id = None
                        for video_query in itertools.product(animal_query.videos):
                            for video in video_query:
                                youtube_video_id = video.youtube_id

                        category_query = Category.query.filter(Category.id == animal_query.category_id).first()
                        subcategory_query = SubCategory.query.filter(
                            SubCategory.id == animal_query.subcategory_id).first()

                        data = {
                            "status": 'success',
                            "is_worker": is_worker,
                            "user_id": user_email_query.id,
                            "youtube_video_id": youtube_video_id,
                            "title": animal_query.name,
                            "mother": animal_query.mother,
                            "father": animal_query.father,
                            "animal_id": animal_id,
                            "category_name": category_query.name_en,
                            "subcategory_name": subcategory_query.name_en,
                            "youtube_video_status": "private"
                        }
                        return make_response(jsonify(data), 200)

            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class ActivateOfUploadedAnimal(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = visibility_of_uploaded_animal.parse_args()

        worker_email = data['worker_email']
        user_email = data['user_email']
        animal_id = data['animal_id']
        btn = data['btn']

        if api_key == app.config['API_KEY']:
            try:
                worker_email_query = User.query.filter_by(email=worker_email).first()
                user_email_query = User.query.filter_by(email=user_email).first()

                worker_email_user_permission_query = UserPermission \
                    .query.join(User.permission) \
                    .filter(User.id == worker_email_query.id).first()

                if worker_email is not None:
                    animal_query = Animal.query.filter_by(id=animal_id).first()
                    is_worker = worker_email_user_permission_query.is_user_management
                    if animal_query is not None:
                        if worker_email == user_email:
                            animal_query.visibility = "True"
                        if worker_email != user_email:
                            if is_worker == "True":
                                if btn == "btn03_01":
                                    animal_query.visibility = "True"
                                if btn == "btn03_02":
                                    animal_query.visibility = "True"
                                    animal_query.worker_visibility = "True"
                        animal_query.db_post()

                        youtube_video_id = None
                        for video_query in itertools.product(animal_query.videos):
                            for video in video_query:
                                youtube_video_id = video.youtube_id

                        category_query = Category.query.filter(Category.id == animal_query.category_id).first()
                        subcategory_query = SubCategory.query.filter(
                            SubCategory.id == animal_query.subcategory_id).first()

                        data = {
                            "status": 'success',
                            "is_worker": is_worker,
                            "user_id": user_email_query.id,
                            "youtube_video_id": youtube_video_id,
                            "title": animal_query.name,
                            "mother": animal_query.mother,
                            "father": animal_query.father,
                            "animal_id": animal_id,
                            "category_name": category_query.name_en,
                            "subcategory_name": subcategory_query.name_en,
                            "youtube_video_status": "public"
                        }
                        return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


#  Crone
class AnimalAgeUpdate(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']

        if api_key == app.config['API_KEY']:
            try:
                animal_query = Animal.query.all()

                if animal_query is not None:
                    today = datetime.now()
                    for animal in animal_query:
                        date1 = datetime(int(animal.age_year), int(animal.age_month), int(animal.age_day))
                        date2 = today
                        diff = relativedelta.relativedelta(date2, date1)
                        animal.years = diff.years
                        animal.months = diff.months
                        animal.days = diff.days
                        animal.db_post()

                    data = {"status": 'success'}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class YouTubeUpload(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = youtube_upload_data.parse_args()

        animal_id = data['animal_id']

        if api_key == app.config['API_KEY']:
            try:
                animal_query = Animal.query.filter(Animal.id == animal_id).first()

                if animal_query is not None:
                    for video_query in itertools.product(animal_query.videos):
                        for video in video_query:
                            data = {
                                "status": 'success',
                                "youtube_video_id": video.youtube_id,
                                "title": animal_query.name,
                                "mother": animal_query.mother,
                                "father": animal_query.father,
                                "animal_id": animal_id
                            }
                            return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class YouTubeId(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = youtube_id_data.parse_args()

        animal_id = data['animal_id']
        youtube_video_id = data['youtube_video_id']

        if api_key == app.config['API_KEY']:
            try:
                animal_query = Animal.query.filter(Animal.id == animal_id).first()

                if animal_query is not None:
                    for video_query in itertools.product(animal_query.videos):
                        for video in video_query:
                            video.youtube_id = youtube_video_id
                            video.db_post()
                            data = {"status": 'success'}
                            return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(UploadingAnimal, '/uploading-animal')
api.add_resource(ListOfUploadedAnimals, '/list-of-uploaded-animals')
api.add_resource(EditOfUploadedAnimal, '/edit-of-uploaded-animal')
api.add_resource(UploadingAnimalOnlyImagesVideo, '/uploading-animal-only-images-video')
api.add_resource(DelOfUploadedAnimal, '/del-of-uploaded-animal')
api.add_resource(InactivateOfUploadedAnimal, '/inactivate-of-uploaded-animal')
api.add_resource(ActivateOfUploadedAnimal, '/activate-of-uploaded-animal')
api.add_resource(AnimalAgeUpdate, '/animal-age-update')
api.add_resource(YouTubeUpload, '/youtube-upload')
api.add_resource(YouTubeId, '/youtube-id')

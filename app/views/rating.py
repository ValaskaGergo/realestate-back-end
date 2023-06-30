# -*- coding: utf-8 -*-
from app import app
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from app.models.models import User, Animal, Rating
from sqlalchemy import or_, and_, desc, asc, func

mod = Blueprint('rating_module', __name__)
api = Api(mod)

post_rating_data = reqparse.RequestParser()
post_rating_data.add_argument('user_id', required=True)
post_rating_data.add_argument('animal_id', required=True)
post_rating_data.add_argument('rating', required=True)


class PostRating(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = post_rating_data.parse_args()

        user_id = int(data['user_id'])
        animal_id = int(data['animal_id'])
        rating = int(data['rating'])

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(id=user_id).first()
                animal = Animal.query.filter_by(id=animal_id).first()

                if user is not None and animal is not None:
                    is_rating = Rating.query \
                        .filter(and_(Rating.user_id == user.id, Rating.animal_id == animal.id)) \
                        .first()

                    if is_rating is None:
                        if rating != 0:
                            rating_payload = Rating(
                                user_id=user.id,
                                animal_id=animal.id,
                                rating=rating
                            )
                            rating_payload.db_post()
                    else:
                        if rating != 0:
                            is_rating.user_id = user.id
                            is_rating.animal_id = animal.id
                            is_rating.rating = rating
                            is_rating.db_post()
                        else:
                            is_rating.db_delete()

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
                        for animal in rating_query:
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
                                  5 * rating_count_five) / (rating_count_one + rating_count_two + rating_count_three +
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

                    animal_query = Animal.query.filter_by(id=animal_id).first()
                    animal_query.rating = round(rating, 1)
                    animal_query.db_post()

                    data = {
                        "status": "success",
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
                        "rating": round(rating, 1)}
                    return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(PostRating, '/post-rating')

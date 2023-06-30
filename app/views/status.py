# -*- coding: utf-8 -*-
from app import app, db
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
import psutil
import time
from datetime import datetime, timedelta
from dateutil.parser import parse

mod = Blueprint('status_module', __name__)
api = Api(mod)


class GetStatus(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']

        if api_key == app.config['API_KEY']:
            try:
                now = datetime.now()
                uptime = time.time() - psutil.boot_time()
                days = uptime // (24 * 60 * 60)
                hours = (uptime % (24 * 60 * 60)) // (60 * 60)
                minutes = (uptime % (60 * 60)) // 60
                seconds = uptime % 60

                days_90_list = []

                for i in range(90):
                    item = {
                        "datetime": now - timedelta(days=90 - i)
                    }
                    days_90_list.append(item)

                data = {
                    "uptime": {
                        "days": days,
                        "hours": hours,
                        "minutes": minutes,
                        "seconds": seconds,
                        "datetime": days_90_list
                    }
                }
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(GetStatus, '/get-status')

# -*- coding: utf-8 -*-
from app import app
from config import _basedir
from flask import Blueprint, json, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from zeep import Client
import xml.etree.ElementTree as Et
from datetime import datetime, timedelta
import requests
import io

mod = Blueprint('exchange_module', __name__)
api = Api(mod)


class SetExchange(Resource):
    @staticmethod
    def get():
        api_key = request.headers['X-Api-Key']

        if api_key == app.config['API_KEY']:
            try:
                now = datetime.now()
                mnb_client = Client(app.config['MNB_HU_URL'])
                mnb_service = mnb_client.service
                mnb_tree = mnb_service.GetExchangeRates(startDate=now.strftime("%Y-%m-%d"),
                                                        endDate=now.strftime("%Y-%m-%d"), currencyNames="EUR")
                mnb_root = Et.fromstring(mnb_tree)
                mnb_rate = mnb_root.findall("./Day/Rate")
                mnb_huf = None
                for rate in mnb_rate:
                    mnb_huf = rate.text.replace(",", ".")

                url = app.config['EXCHANGE_RATES_API_URL'] + "?access_key=" + app.config['EXCHANGE_RATES_API_KEY']
                headers = {"Content-Type": "application/json"}
                r = requests.get(url, headers=headers, verify=app.config['TLS_VERIFY'])

                if r.status_code == 200:
                    data = r.json()

                    exchange_json = io.open(_basedir + "/app/json/exchange.json", 'r+')
                    exchange_json_read = json.loads(exchange_json.read())

                    app.logger.info(mnb_huf)

                    if mnb_huf is not None:
                        #  data['rates']['HUF_MNB'] = float(mnb_huf)
                        data['rates']['HUF'] = float(mnb_huf)
                        exchange_json.seek(0)
                        exchange_json.truncate()
                        exchange_json.write(json.dumps(data, indent=2))
                    else:
                        #  mnb_huf = exchange_json_read['rates']['HUF_MNB']
                        #  data['rates']['HUF_MNB'] = float(mnb_huf)
                        mnb_huf = exchange_json_read['rates']['HUF']
                        data['rates']['HUF'] = float(mnb_huf)
                        exchange_json.seek(0)
                        exchange_json.truncate()
                        exchange_json.write(json.dumps(data, indent=2))

                    exchange_json.close()
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


class GetExchange(Resource):
    @staticmethod
    def get():
        api_key = request.headers['X-Api-Key']

        if api_key == app.config['API_KEY']:
            try:
                exchange_json = io.open(_basedir + "/app/json/exchange.json", 'r')
                exchange_json_read = json.loads(exchange_json.read())
                return exchange_json_read
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(SetExchange, '/set-exchange')
api.add_resource(GetExchange, '/get-exchange')

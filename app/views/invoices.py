# -*- coding: utf-8 -*-
from app import app, db
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from app.models.models import User, BarionPayment, PayPalPayment
from dateutil.parser import parse
import math
from sqlalchemy import desc
from .utilities.utility import Pagination

mod = Blueprint('invoices_module', __name__)
api = Api(mod)

get_invoices = reqparse.RequestParser()
get_invoices.add_argument('email', required=True)
get_invoices.add_argument('page_number', required=True)


class GetInvoices(Resource):
    @staticmethod
    def post():
        api_key = request.headers['X-Api-Key']
        data = get_invoices.parse_args()

        email = data['email']

        if api_key == app.config['API_KEY']:
            try:
                user = User.query.filter_by(email=email).first()

                page_number = int(data['page_number'])
                invoices_limit = 5
                offset_number = (page_number * invoices_limit) - invoices_limit

                barion_query_count = BarionPayment.query.filter_by(user_id=user.id).count()
                paypal_query_count = PayPalPayment.query.filter_by(user_id=user.id).count()
                invoices_query_count = barion_query_count + paypal_query_count
                pagination_count = math.ceil(invoices_query_count / invoices_limit)
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
                    "invoices_limit": int(invoices_limit),
                    "invoices_count": int(invoices_query_count),
                    "pagination_count": int(pagination_count),
                    "pagination_first": int(pagination_first),
                    "pagination_last": int(pagination_last),
                    "pagination_next": int(pagination_next),
                    "pagination_previous": int(pagination_previous)
                }

                barion_payment_query = BarionPayment \
                    .query.join(User.barion_payment) \
                    .filter(User.id == user.id) \
                    .filter(BarionPayment.status == "Succeeded") \
                    .order_by(desc(BarionPayment.created_at)).offset(offset_number).limit(invoices_limit) \
                    .all()

                paypal_payment_query = PayPalPayment \
                    .query.join(User.paypal_payment) \
                    .filter(User.id == user.id) \
                    .filter(PayPalPayment.status == "APPROVED") \
                    .order_by(desc(PayPalPayment.created_at)).offset(offset_number).limit(invoices_limit) \
                    .all()

                invoices_list = []

                for barion in barion_payment_query:
                    days = int(barion.order_number.split("-")[2].split(".")[0])
                    if days > 200:
                        month = 12
                    elif days > 40:
                        month = 6
                    else:
                        month = 1
                    item = {
                        "payment_type": barion.payment_type,
                        "payment_id": barion.payment_id,
                        "payment_request_id": barion.payment_request_id,
                        "month": month,
                        "funding_source": barion.funding_source,
                        "price": float(barion.price),
                        "vat": float(barion.vat),
                        "total": float(barion.total),
                        "currency": barion.currency,
                        "billing_url": barion.billing_url,
                        "created_at": str(barion.updated_at),
                    }
                    invoices_list.append(item)

                for paypal in paypal_payment_query:
                    days = int(paypal.order_number.split("-")[2].split(".")[0])
                    if days > 200:
                        month = 12
                    elif days > 40:
                        month = 6
                    else:
                        month = 1
                    item = {
                        "payment_type": paypal.payment_type,
                        "payment_id": paypal.payment_id,
                        "payment_request_id": paypal.payment_request_id,
                        "month": month,
                        "funding_source": paypal.funding_source,
                        "price": float(paypal.price),
                        "vat": float(paypal.vat),
                        "total": float(paypal.total),
                        "currency": paypal.currency,
                        "billing_url": paypal.billing_url,
                        "created_at": str(paypal.created_at),
                    }
                    invoices_list.append(item)

                data = {"pagination_list": pagination_list, "pagination": pagination,
                        "data": sorted(invoices_list, key=lambda x: parse(str(x['created_at'])), reverse=True)}
                return make_response(jsonify(data), 200)
            except ValueError:
                data = {"status": 'error', "message": "internal server error"}
                return make_response(jsonify(data), 500)
        else:
            return make_response(jsonify(), 401)


api.add_resource(GetInvoices, '/get-invoices')

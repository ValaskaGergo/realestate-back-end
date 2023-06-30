# -*- coding: utf-8 -*-
import os

_basedir = os.path.abspath(os.path.dirname(__file__))
_static = os.path.join(_basedir, 'app/static')
_model = os.path.join(_basedir, 'app/models')


class Config(object):
    BRAND_NAME = "ANLI Realestate"

    #: python -c "print(repr(__import__('os').urandom(24)))"
    SECRET_KEY = '|\nrq\xe6\x8f8z\t\x9ex\x1a\x0c\xce\xd9\xd8\x03\xb0\xcf\x8a\xf2\xef'
    #: hashlib.sha256(os.urandom(32)).hexdigest()
    API_KEY = 'd330bd488282ed02d0256e0ee704114776dfd0b28ca1eb667a875193ca8d63d1'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    VATLAYER_API_URL = "https://apilayer.net/api"

    EXCHANGE_RATES_API_URL = "http://api.exchangeratesapi.io/v1/latest"

    MNB_HU_URL = "http://www.mnb.hu/arfolyamok.asmx?wsdl"

    BILLINGO_API_URL = "https://api.billingo.hu/v3"

    USER_TO_USER_FIRST_MESSAGE = "B2F5hG7KJ9X3M4tH6yC8KP"


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    TLS_VERIFY = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://development:11aaAA??@localhost/anlibreeders_production'

    VATLAYER_API_KEY = "d1faec9c29bf6cf008c45c153fc78572"

    EXCHANGE_RATES_API_KEY = "8853dbdf91a7f0f3d0887cbecb1f12dd"

    BARION_API_URL = "https://api.test.barion.com"
    BARION_API_KEY = "d97e43d0ccdd42bcb29307ae9c8b85cb"
    BARION_PIXEL_ID = "BPT-Exfw7hzWQ8-93"
    BARION_ACCOUNT_EMAIL = "robotharcos981@gmail.com"
    BARION_CALLBACK_URL = "https://api.anlibreeders.com"

    PAYPAL_API_URL = "https://api-m.sandbox.paypal.com"
    PAYPAL_URL = "https://www.sandbox.paypal.com"
    PAYPAL_CLIENT_ID = "Ae1bRTWg9jh0Lf7nlF246Ow9pjJij8m0n0RMMGJxtKrYRlojwpG2t_VIm8i3QBWRl0E2nwbQyfEkMgEZ"
    PAYPAL_SECRET = "ECHxQB5RuyJu_dX2ArZBJ7FA-ttkRfz2Qe8ydcsOK3jWo87mr4YsKOI22lNHr6Mbpv0PRb7yll9L9cT9"

    ACCOUNT_MINUTE = "600"

    BILLINGO_API_KEY = "4f1cfc1a-4842-11ec-973d-06ac9760f844"
    BILLINGO_DOCUMENTS_TYPE = "draft"

    DEEPL_API_KEY = "4a9d2826-79e9-b81b-0b79-7fe2309f17ae"

    DETECT_LANGUAGE_KEY = '2ce436bed0765bed1c101df83383e9d5'  # https://github.com/detectlanguage/detectlanguage-python

    SERVER_URL = "https://anlirealestate.com"
    API_SERVER_URL = "https://api.anlirealestate.com"
    SOCKET_SERVER_URL = "https://socket.anlirealestate.com"
    CORS_ALLOWED_ORIGINS = "https://anlirealestate.com"


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    TLS_VERIFY = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://development:11aaAA??@localhost/anlirealestate'
    SQLALCHEMY_ECHO = False

    VATLAYER_API_KEY = "d1faec9c29bf6cf008c45c153fc78572"

    EXCHANGE_RATES_API_KEY = "8853dbdf91a7f0f3d0887cbecb1f12dd"

    BARION_API_URL = "https://api.test.barion.com"
    BARION_API_KEY = "d97e43d0ccdd42bcb29307ae9c8b85cb"
    BARION_PIXEL_ID = "BPT-Exfw7hzWQ8-93"
    BARION_ACCOUNT_EMAIL = "robotharcos981@gmail.com"
    BARION_CALLBACK_URL = "https://api.anlibreeders.com"

    PAYPAL_API_URL = "https://api-m.sandbox.paypal.com"
    PAYPAL_URL = "https://www.sandbox.paypal.com"
    PAYPAL_CLIENT_ID = "Ae1bRTWg9jh0Lf7nlF246Ow9pjJij8m0n0RMMGJxtKrYRlojwpG2t_VIm8i3QBWRl0E2nwbQyfEkMgEZ"
    PAYPAL_SECRET = "ECHxQB5RuyJu_dX2ArZBJ7FA-ttkRfz2Qe8ydcsOK3jWo87mr4YsKOI22lNHr6Mbpv0PRb7yll9L9cT9"

    ACCOUNT_MINUTE = "600"

    BILLINGO_API_KEY = "4f1cfc1a-4842-11ec-973d-06ac9760f844"
    BILLINGO_DOCUMENTS_TYPE = "draft"

    DEEPL_API_KEY = "4a9d2826-79e9-b81b-0b79-7fe2309f17ae"

    DETECT_LANGUAGE_KEY = '2ce436bed0765bed1c101df83383e9d5'  # https://github.com/detectlanguage/detectlanguage-python

    SERVER_URL = "https://anlirealestate.com"
    API_SERVER_URL = "https://api.anlirealestate.com"
    SOCKET_SERVER_URL = "https://socket.anlirealestate.com"
    CORS_ALLOWED_ORIGINS = "https://anlirealestate.com"

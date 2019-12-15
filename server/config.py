import os


# Number of items per page
PAGINATE_VALUE = 3


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'too-much-secure'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@mysql/test_db?charset=utf8'
    FLASK_DEBUG=1

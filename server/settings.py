import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'too-much-secure'
    SQLALCHEMY_DATABASE_URI = 'postgres://test:test@localhost/test_db'

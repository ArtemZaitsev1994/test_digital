# Number of items per page
PAGINATE_VALUE = 3


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'too-much-secure'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/test_db?charset=utf8'
    FLASK_DEBUG = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'too-much-secure'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/testing?charset=utf8'
    FLASK_DEBUG = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
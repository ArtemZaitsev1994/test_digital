from os.path import isfile
from envparse import env


if isfile('.env'):
    env.read_envfile('.env')

# Number of items per page
PAGINATE_VALUE = env.int('PAGINATE_VALUE')


class Config(object):
    DEBUG = env.bool('DEBUG')
    TESTING = env.bool('TESTING')
    CSRF_ENABLED = env.bool('CSRF_ENABLED')
    SECRET_KEY = env.str('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool('SQLALCHEMY_TRACK_MODIFICATIONS')

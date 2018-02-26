import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'Thisissicret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
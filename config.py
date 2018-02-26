import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'Thisissicret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://localhost/TODO?user=postgres&password=JuliaIgnacio'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
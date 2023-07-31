import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'pump_it_up/'

    if os.environ.get('HEROKU_ENV'):  # heroku check?
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
    else: 
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or f'postgresql://USERNAME:PASSWORD@IP/DATABASE'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
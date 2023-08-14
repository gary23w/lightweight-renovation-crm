import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', b'pump_it_up/')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if os.environ.get('HEROKU_ENV'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                                  f'postgresql://{os.getenv("POSTGRES_USER", "USER")}:' \
                                  f'{os.getenv("POSTGRES_PASSWORD", "PASSWORD")}@{os.getenv("DATABASE_HOST", "DB")}/' \
                                  f'{os.getenv("POSTGRES_DB", "DATABASE")}'

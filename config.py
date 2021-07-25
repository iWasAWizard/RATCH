import os
from decouple import config


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Secret key config
    SECRET_KEY = config('SECRET_KEY')

    # PostgreSQL engine config
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='postgresql'),
        config('DB_DIALECT', default='psycopg2'),
        config('DB_USERNAME', default='ratch_user'),
        config('DB_PASS', default='ratch'),
        config('DB_HOST', default='postgres'),
        config('DB_PORT', default=5432),
        config('DB_NAME', default='ratch_db')
    )


class ProductionConfig(Config):
    DEBUG = False

    # Security config
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}

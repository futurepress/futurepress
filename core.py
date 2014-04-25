import os

from flask.ext.sqlalchemy import SQLAlchemy

from key import ( apiKey_id, apiKey_secret )
from settings import basedir

db = SQLAlchemy()

class Config(object):
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = 'my_precious'

    STORMPATH_API_KEY_ID = apiKey_id
    STORMPATH_API_KEY_SECRET = apiKey_secret
    STORMPATH_APPLICATION = 'flask-stormpath-sample'
    DATABASE_PATH = os.path.join(basedir, 'dev.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

class TestConfig(Config):
    DEBUG = True
    SECRET_KEY = 'my_precious'
    TESTING = True

    STORMPATH_API_KEY_ID = apiKey_id
    STORMPATH_API_KEY_SECRET = apiKey_secret
    STORMPATH_APPLICATION = 'flask-stormpath-sample'
    DATABASE_PATH = os.path.join(basedir, 'test', 'unittest.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

    USER_PASSWORD = 'Jake1234'
    USER_EMAIL = 'jake.hartnell@test.com'
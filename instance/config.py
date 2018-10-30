import os

class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    TESTING = False
    SECRET_KEY = 'fwefui32y8743jijfe0r0932EFIJFeiw8f32'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///api.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True



app_config = {
    'testing': TestingConfig,
    'production': Config,
}
import os

from flask import Flask


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = 'gamr.sqlite'
    HOST = '0.0.0.0'
    PORT = '5000'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True 
# -*- coding: utf-8 -*-

import os

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
DB_NAME = "rbm.db"
DB_PATH = os.path.join(PROJECT_ROOT, DB_NAME)
SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_PATH)
DEBUG = True
SECRET_KEY = 'shhhh'

redis_conn = None

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

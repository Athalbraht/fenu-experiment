# config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

ORIGINS = ["*"] 
SECRET_KEY = "ad39defhkasdf0avfdsiav90AOD0DFs1"
PORT = 8000
DEBUG = True
TESTING = False
ENV = 'dev'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join('static', 'img')





# config.py

import os

ORIGINS = ["*"] # for api calls
SECRET_KEY = "ad39defhkasdf0avfdsiav90AOD0DFs1"
PORT = 8000
DEBUG = True
TESTING = False
ENV = 'dev'
SQLALCHEMY_DATABASE_URI = "sqlite:////database/sqlite"
UPLOAD_FOLDER = os.path.join('static', 'img')





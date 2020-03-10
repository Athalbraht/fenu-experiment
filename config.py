# config.py

import os

domain = "https://fenu-exp.us.edu.pl"
languages = ["en","pl"]

ORIGINS = ["*"]
SECRET_KEY = "ad39defhkasdf0avfdsiav90AOD0DFs1"
PORT = 8000
DEBUG = True
TESTING = False
ENV = 'dev'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'database/sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

REPO = "https://github.com/aszadzinski/BINA-CCB.git"
UPLOAD_FOLDER = os.path.join('static', 'img')
PHOTOS_TYPE = ["BINA_window","Schemes", "Detector", "Others"]
HOMEPAGE_FOLDER = os.path.join(basedir, 'App/static/homepage')

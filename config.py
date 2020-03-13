# config.py

import os

# main information
main = {
    "author"    : "Albert Szadziński",
    "version"   : "v3.3",
    "domain"    : "https://fenu-exp.us.edu.pl",
    "internal"  : "https://fenu-experiment.pl/",
    "repo"      : "https://github.com/aszadzinski/BINA-CCB.git",
    }
languages = ["en","pl"]

# Internal config
PHOTOS_TYPE = ["BINA_window","Schemes", "Detector", "Others", "Target", "Public", "Production", "Salad", "Plans", "Target_chamber"]

# Server config
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

UPLOAD_FOLDER = os.path.join('static', 'img')
HOMEPAGE_FOLDER = os.path.join(basedir, 'App/static/homepage')

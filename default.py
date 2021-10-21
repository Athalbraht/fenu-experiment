# default.py

import os

# SERVER CONFIG

ORIGINS = ["*"]
SECRET_KEY = "ad39defhkastestowy00klucz00xdfdsiav90AOD0DFs1"
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True
TESTING = False
ENV = 'dev'
LOGS = True
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = os.path.join('static', 'img')
HOMEPAGE_FOLDER = os.path.join(basedir, 'App/static/homepage')
REPOSITORY_FOLDER = os.path.join(basedir, 'App/static/repository')

# PAGE CONFIG

PAGE_CONFIG = {
    "ENABLE_RSS"           :   True,
    "ENABLE_FORUM"         :   True,
    "ENABLE_LINKS"         :   True,
    "ENABLE_MEMBERS"       :   True,
    "ENABLE_PUBLICATIONS"  :   True,
    }

PAGE_INFO = {
    "AUTHOR"    :   "Albert Szadziński",
    "VERSION"   :   "v4.1b",
    "DOMAIN"    :   "https://fenu-exp.us.edu.pl",
    "INTERNAL"  :   "https://fenu-experiment.pl",
    "LOCAL"     :   "local-home-server",
    "LOCAL-DEV"	:   "your-dev-server",
    "REPO"      :   "https://github.com/fenu-exp/fenu-exp.internal.git",
    "TAGS"      :   "BINA, BINA detector, 3nf, space star, CCB, bronowice, nuclear forces, UŚ, UJ, IFJ PAN, experiments, 3-nucleon forces, breakup, elastic scattering, few nucleon systems",
    "LANGUAGES" :   ["en", "pl"],
    }


RSS = {
    "RSS"           :   10,
    "TITLE"         :   "Fenu-Exp",
    "DESCRIPTION"   :   "Fenu-Exp News",
    }

FORUM_CATEGORIES = {
        "Information"   : ["Announcements", "Bug Reports & Suggestions"],
        "General"       : ["Events", "Plans", "Orders"],
        "Discussions"   : ["Data Analysis", "Experiments", "Software"],
        "Off-Topic"     : ["General Discussions"]
    }

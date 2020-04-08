import logging
import config
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__,
            instance_relative_config=True,
            static_folder="static",
            static_url_path="")

if os.path.exists("config_user"):
    app.config.from_object("config_user")
else:
    print("config_user.py file not found. Using config.py")
    app.config.from_object("config")
    
db = SQLAlchemy(app)
migrate = Migrate(app, db)
log = logging.getLogger('werkzeug')
log.disabled = not config.LOGS

from App import models
from App import views

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
log = logging.getLogger('werkzeug')
log.disabled = True

from App import models
from App import views

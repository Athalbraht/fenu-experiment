import logging
import os
import config

from flask import Flask

app = Flask(__name__,
            instance_relative_config=True,
            static_folder="static",
            static_url_path="")

app.config.from_object("config")

#from App import models
from App import blueprints

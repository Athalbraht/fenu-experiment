# views/modules.py
import os
import time

from datetime import datetime as dt
from io import BytesIO

from App import app
from App import db
from App import config

from App.models import *
from App.tools.security import *
from App.tools.db_requests import *
from App.tools.translator import *
from App.tools.structures import *

from flask import render_template, request, redirect, url_for, session, flash, send_file, send_from_directory, g
from werkzeug.utils import secure_filename

def deploy_homepage():
    try:
        index_page = render_template("world/experiments.html",
                                        lang=translator('pl'))
        export_html(None, "index", index_page, index=True)
        for language in config.languages:
            experiment_page = render_template("world/experiments.html",
                                            lang=translator(language))
            students_page = render_template("world/home.html",
                                            lang=translator(language))
            publications_page = render_template("world/publications.html",
                                            lang=translator(language), publications=list_papers("publications"))
            members_page = render_template("world/members.html",
                                            lang=translator(language), members=get_members())
            export_html(language, "experiments", experiment_page)
            export_html(language, "students", students_page)
            export_html(language, "publications", publications_page)
            export_html(language, "members", members_page)
        flash("Deployed")
    except Exception as e:
        print(e)
        flash("FAILED!")
        return None
    # TODO
    # GIT-AUTOUPDATE
    return None


def permission_check(template, session):
    if "username" in session:
        _kwargs = {
                    "template_name_or_list" : template,
                    "session"               : session,
                    "state"                 : config.main
                    }
        return _kwargs
    else:
        _kwargs = {
                    "template_name_or_list" : "404.html",
                    "lang"                  : translator(session["lang"]),
                    }
        flash("Permission denied. Log in first.")
        return _kwargs

# views/session.py

from .modules import *


@app.before_request
def before_request():
    g.user = None
    g.lang = None
    if 'user' in session:
        g.user = session["user"]
        session["status"] = "Log out"
        session["guest"] = False
        session["logged_in"] = True
        session["admin"] = True
    else:
        session["status"] = "Log in"
        session["guest"] = True
        session["logged_in"] = False
        session["admin"] = False
        session["username"] = "Guest"
    if 'lang' in session:
        g.lang = session["lang"]
    else:
        session["lang"] = "en"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", **get_var(session),lang=translator(session["lang"])), 404

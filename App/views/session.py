# views/session.py

from .modules import *

@app.before_request
def before_request():
    g.user = None
    # g.lang = None
    if "username" in session:
        g.user = session["username"]
        session["lang"] = "en"
        #session["admin"] = False
    else:
        session["admin"] = False
        session["lang"] = "en"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", session=session, lang=translator(session["lang"])), 404

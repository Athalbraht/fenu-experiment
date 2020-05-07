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

@app.route("/login", methods=['GET', "POST"])
def login():
    if "username" in session:
        return redirect(url_for('dashboard_publications',paper='publications'))
    if request.method == "POST":
        password = request.form['password']
        user = check_password(password)
        if user[1]:
            session["username"] = user[2]
            session["admin"] = user[3]
            flash(user[0])
            return redirect(url_for('dashboard_publications',paper='publications'))
        else:
            flash(user[0])
    return render_template("world/login.html", session=session, lang=translator(session["lang"]))


@app.route("/logout", methods=['GET', "POST"])
def logout():
    # lang = session["lang"]
    session.pop("username", None)
    # session["lang"] = lang
    flash("Logged out")
    return redirect(url_for('login'))

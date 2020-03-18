# views/specials.py

from .modules import *

@app.route("/")
def main():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', "POST"])
def login():
    if session['status'] == "Log out":
        return redirect(url_for('dashboard_publications',paper='publications'))
    if request.method == "POST":
        #login = request.form['login']
        password = request.form['password']
        user = check_password("admin", password)
        if user[1]:
            session["user"] = user[2]
            session["username"] = user[2]
            session["status"] = "Log out"
            flash(user[0])
            return redirect(url_for('dashboard_publications',paper='publications'))
        else:
            flash(user[0])
    return render_template("world/login.html", **get_var(session),lang=translator(session["lang"]))


@app.route("/logout", methods=['GET', "POST"])
def logout():
    lang = session["lang"]
    session.pop("user", None)
    session["lang"] = lang
    flash("Logged out")
    return redirect(url_for('login'))


@app.route("/invite", methods=["POST", "GET"])
def invite():
    if request.method == "POST":
        passwd = request.form["password"]
        new_passwd = request.form["password"]
        name = request.form["name"]
        surname = request.form["surname"]
        title = request.form["title"]
        affil = request.form["affil"]
        email = request.form["email"]
        pubs = request.form["pubs"]

    return render_template("world/invite.html",
                            **get_var(session),
                            lang=translator(session["lang"]),
                            afil=Organizations.query.all())


@app.route("/dashboard/wiki", methods=['GET', "POST"])
def dashboard_wiki():
    if request.method == "POST":
        flash("Added")
    return "Permission denied"

    
@app.route("/sendfile/<types>/<folder>/<filename>", methods=['GET', "POST"])
def send_pub(types,folder,filename):
    path = paths[types]
    return send_from_directory(
        directory="../{}/{}/".format(path,folder), filename=filename, as_attachment=False)

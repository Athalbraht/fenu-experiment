# views/specials.py

from .modules import *

@app.route("/invite", methods=["POST", "GET"])
def invite():
    if request.method == "POST":
        passwd = request.form["password"]
        new_passwd = request.form["npassword"]
        name = request.form["name"]
        surname = request.form["surname"]
        affil = request.form["affil"]
        email = request.form["email"]
        orcid = request.form["orcid"]
        rgate = request.form["rgate"]
        page = request.form["page"]
        degree = request.form["degree"]
        function = request.form["function"]

        status = check_password(passwd)
        if not status[1]:
            flash(status[0])
            return redirect(url_for("invite"))
        else:
            new_member = Members(email=email, name=name, surname=surname, title=degree, affiliation=affil, orcid=orcid, rgate=rgate, link=page, desc=function)
            try:
                db.session.add(new_member)
                db.session.commit()
                flash("Added new member {}.".format(email))
                if new_passwd != '':
                    member = Members.query.filter(Members.email==email).first()
                    npasswd = hash_password(new_passwd)
                    new_user = Users(password_hash=npasswd, member=member.id, admin=0)
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Added new user {}.".format(email))
            except:
                flash("Failed to commit!")
                return redirect(url_for("invite"))
            finally:
                return redirect(url_for("login"))

    return render_template("world/invite.html",
                            session,
                            lang=translator(session["lang"]),
                            afil=Organizations.query.all())

@app.route("/sendfile/<types>/<folder>/<filename>", methods=['GET', "POST"])
def send_pub(types,folder,filename):
    path = paths[types]
    return send_from_directory(
        directory="../{}/{}/".format(path,folder), filename=filename, as_attachment=False)

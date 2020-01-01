# views.py

import os
from App import app
from App import db
from App.models import *
from App.extensions import *
from flask import render_template, request, redirect, url_for, session, flash, send_file, send_from_directory, g
from werkzeug.utils import secure_filename
exp_img = exp_imgs(app.config["UPLOAD_FOLDER"])


@app.route("/test")
def test():
    posts = list_posts()
    return str(paths["conferences"])

    #####################
    #####################
    ###  Main NavBar  ###
    #####################
    #####################


@app.route("/home")
def home():
    print(get_var(session))
    return render_template("world/home.html", **
                           get_var(session), posts=list_posts())


@app.route("/")
def main():
    return redirect(url_for('experiments'))


@app.route("/login", methods=['GET', "POST"])
def login():
    if request.method == "POST":
        #login = request.form['login']
        password = request.form['password']
        user = check_password("admin", password)
        if user[1]:
            session["user"] = user[2]
            session["username"] = user[2]
            session["status"] = "Log out"
            flash(user[0])
            return redirect(url_for('home'))
        else:
            flash(user[0])
    return render_template("world/login.html", **get_var(session))


@app.route("/logout", methods=['GET', "POST"])
def logout():
    session.pop("user", None)
    flash("Logged out")
    return redirect(url_for('home'))


@app.route("/experiments", methods=['GET', "POST"])
def experiments():
    return render_template("world/experiments.html", **
                           get_var(session), imagee=exp_img, collection=list_presentation_groups("detector",False))


@app.route("/members")
def members():
    return render_template("world/members.html", **
                           get_var(session), organizations=list_members())


@app.route("/publications")
def publications():
    return render_template("world/publications.html", **
                           get_var(session), publications=list_publications())

    #####################
    #####################
    ###   DashBoard   ###
    #####################
    #####################


def permission_check(template, *args, **kwargs):
    if session["admin"]:
        _kwargs = {"template_name_or_list": template}
        _kwargs.update(kwargs)
        return _kwargs
    else:
        _kwargs = {"template_name_or_list": "world/home.html"}
        _kwargs.update(get_var(session))
        flash("Permission denied. Log in first.")
        return _kwargs


@app.route("/dashboard")
def dashboard():
    return redirect(url_for('dashboard_publications'))

    #########
    # files #
    #########


@app.route("/dashboard/files")
def dashboard_files():
    return render_template(
        **permission_check("dashboard/files.html", **get_var(session)))


@app.route("/dashboard/publications", methods=['GET', "POST"])
def dashboard_publications():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="publication", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/publications.html",
                                              **get_var(session)), publications=list_publications())


@app.route("/dashboard/thesis", methods=['GET', "POST"])
def dashboard_thesis():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="thesis", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/thesis.html",
                                              **get_var(session)), publications=list_thesis())

@app.route("/dashboard/logbooks", methods=['GET', "POST"])
def dashboard_logbooks():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="logbook", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/logbooks.html",
                                              **get_var(session)), publications=list_thesis())

@app.route("/dashboard/manuals", methods=['GET', "POST"])
def dashboard_manuals():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="manual", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/manuals.html",
                                              **get_var(session)), publications=list_thesis())

@app.route("/dashboard/presentations/meetings", methods=['GET', "POST"])
def dashboard_presentations_meetings():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="presentation-m", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/presentations.html",
                                              **get_var(session)), publications=list_presentation_groups("meetings"))

@app.route("/dashboard/presentations/posters", methods=['GET', "POST"])
def dashboard_presentations_posters():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="presentation-p", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/presentations.html",
                                              **get_var(session)), publications=list_presentation_groups("posters"))

@app.route("/dashboard/presentations/conferences", methods=['GET', "POST"])
def dashboard_presentations_conferences():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="presentation-c", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/presentations.html",
                                              **get_var(session)), publications=list_presentation_groups("conferences"))
                                              
@app.route("/dashboard/miscellaneous", methods=['GET', "POST"])
def dashboard_miscellaneous():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        publication = Document(type="misc", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        db.session.add(publication)
        db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/presentations.html",
                                              **get_var(session)), publications=list_presentation_groups("miscellaneous"))

@app.route("/dashboard/gallery", methods=['GET', "POST"])
def dashboard_gallery():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        #publication = Photo(type="presentation-c", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        #db.session.add(publication)
        #db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/photos.html",
                                              **get_var(session)), collection=list_presentation_groups("gallery"), imgs=exp_img)


@app.route("/dashboard/gallery/<folder>", methods=['GET', "POST"])
def dashboard_gallery_open(folder):
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        #publication = Photo(type="presentation-c", title=title, author=author, reference=ref, year=year, desc=desc, doi=link, link="todo")
        #db.session.add(publication)
        #db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/gallery.html",
                                              **get_var(session)), collection=list_presentation_groups(folder,False), imgs=exp_img)

@app.route("/dashboard/data", methods=['GET', "POST"])
def dashboard_data():
    return render_template(
        **permission_check("dashboard/files/data.html", **get_var(session)))


@app.route("/dashboard/presentations", methods=['GET', "POST"])
def dashboard_presentations():
    return render_template(
        **permission_check("dashboard/files/presentations.html", **get_var(session)))

    ###############
    # notes & cal #
    ###############


@app.route("/dashboard/notes", methods=['GET', "POST"])
def dashboard_notes():
    return render_template(
        **permission_check("dashboard/notes.html", **get_var(session)))


@app.route("/dashboard/calendar", methods=['GET', "POST"])
def dashboard_calendar():
    return render_template(
        **permission_check("dashboard/calendar.html", **get_var(session)))

    #########################
    #########################
    ###   DashBoard EDIT  ###
    #########################
    #########################


@app.route("/dashboard/edit/home", methods=['GET', "POST"])
def dashboard_edit_home():
    if request.method == "POST":
        head = request.form['title']
        body = request.form['body']
        post = Post(head=head, body=body)
        db.session.add(post)
        db.session.commit()
        flash("Added")
    return render_template(**permission_check("dashboard/edit/home.html", **
                                              get_var(session)), posts=list_posts(), edit_header="Add new message")


@app.route("/dashboard/edit/home/<post_id>", methods=['GET', "POST"])
def dashboard_edit_home_post(post_id):
    post = get_post(post_id)
    if request.method == "POST":
        head = request.form['title']
        body = request.form['body']
        post.head = head
        post.body = body
        db.session.commit()
        flash("Updated")
    return render_template(**permission_check("dashboard/edit/home.html", **get_var(session)),
                           posts=list_posts(), edit_header="Editing {}".format(post.head), title=post.head, body=post.body)


@app.route("/dashboard/edit/members", methods=['GET', "POST"])
def dashboard_edit_members():
    if request.method == "POST":
        head = request.form['title']
        body = request.form['body']
        post = Post(head=head, body=body)
        db.session.add(post)
        db.session.commit()
        flash("Added")
    return render_template(**permission_check("dashboard/edit/members.html", **get_var(session)),
                           posts=list_posts(), edit_header="Add new message", organizations=list_members())


@app.route("/dashboard/edit/files", methods=['GET', "POST"])
def dashboard_edit_files():
    return render_template(
        **permission_check("dashboard/edit/files.html", **get_var(session)))

    #####################
    #####################
    ### Sending files ###
    #####################
    #####################


@app.route("/sendfile/<types>/<folder>/<filename>", methods=['GET', "POST"])
def send_pub(types,folder,filename):
    path = paths[types]
    print(path)
    print(filename)
    return send_from_directory(
        directory="../{}/{}/".format(path,folder), filename=filename, as_attachment=False)

    ###############
    ###############
    ### Session ###
    ###############
    ###############


@app.before_request
def before_request():
    g.user = None
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", **get_var(session)), 404

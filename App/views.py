# views.py

import os
import time
from datetime import datetime as dt
from io import BytesIO
from App import app
from App import db
from App import config
from App.models import *
from App.extensions import *
from flask import render_template, request, redirect, url_for, session, flash, send_file, send_from_directory, g
from werkzeug.utils import secure_filename
exp_img = exp_imgs(app.config["UPLOAD_FOLDER"])


def deploy_homepage():
    try:
        index_page = render_template("world/experiments.html", **get_var(session),
                                        lang=translator('en'))
        export_html(None, "index", index_page, index=True)
        for language in config.languages:
            experiment_page = render_template("world/experiments.html", **get_var(session),
                                            lang=translator(language))
            students_page = render_template("world/home.html", **get_var(session),
                                            lang=translator(language))
            publications_page = render_template("world/publications.html", **get_var(session),
                                            lang=translator(language), publications=list_papers("publications"))
            members_page = render_template("world/members.html", **get_var(session),
                                            lang=translator(language), organizations=list_members())
            export_html(language, "experiments", experiment_page)
            export_html(language, "students", students_page)
            export_html(language, "publications", publications_page)
            export_html(language, "members", members_page)
        flash("Deployed")
    except:
        flash("FAILED!")
        return None
    # TODO
    # GIT-AUTOUPDATE
    return None

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

    #####################
    #####################
    ###  Main NavBar  ###
    #####################
    #####################

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
        _kwargs = {"template_name_or_list": "index.html"}
        _kwargs.update(get_var(session))
        flash("Permission denied. Log in first.")
        return _kwargs


    #########
    # files #
    #########


@app.route("/dashboard/papers/<paper>", methods=['GET', "POST"])
def dashboard_publications(paper):
    searchOptions = {"author":"","title":"","year":""}
    if request.method == "POST":
        formname = request.form['form-name']
        if formname == "add":
            title = request.form['title']
            author = request.form['author']
            year = request.form['year']
            ref = request.form['ref']
            link = request.form['link']
            desc = request.form['desc']
            _file = request.files['file']

            publication = Documents(type="paper-{}".format(paper), title=title, author=author, reference=ref, year=int(year), desc=desc, link=link, filename=_file.filename, file=_file.read())
            db.session.add(publication)
            db.session.commit()
            flash("Added {}".format(title))

        else:
            search = request.form['form-name']
            year = request.form['year']
            author = request.form['author']
            title = request.form['title']
            searchOptions = {"author":author,"title":title,"year":year}
    return render_template(**permission_check("dashboard/files/papers.html".format(paper),
                                              **get_var(session)),
                                              publications=list_papers(paper,searchOptions),
                                              section=paper,
                                              lang=translator(session["lang"]))


@app.route("/dashboard/<paper>/download/<fileid>", methods=['GET', "POST"])
def dashboard_download(paper,fileid):
    _file = Documents.query.filter_by(id=fileid).first()
    return send_file(BytesIO(_file.file), attachment_filename=_file.filename+".pdf")

@app.route("/dashboard/delete/<f>/<item>", methods=['GET', "POST"])
def dashboard_delete(f,item):
    _file = Documents.query.filter_by(id=item).one()
    db.session.delete(_file)
    db.session.commit()
    flash("deleted file")
    return render_template(**permission_check("dashboard/files/papers.html"),lang=translator(session["lang"]))

@app.route("/dashboard/edit/<f>/<item>", methods=["GET", "POST"])
def dashboard_edit_document(f, item):
    doc = Documents.query.filter(Documents.id==item).first()
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]
        ref = request.form["ref"]
        filename = request.form["filename"]
        doc.title = title
        doc.author = author
        doc.year = year
        doc.reference = ref
        doc.filename = filename
        db.session.commit()
        flash("Updated")

    return render_template(**permission_check("dashboard/edit/files.html",
                                              **get_var(session)),
                                              edited=Documents.query.filter(Documents.id==item).first(),
                                              lang=translator(session["lang"]))

@app.route("/dashboard/presentations/<presentation>", methods=['GET', "POST"])
def dashboard_presentations(presentation):
    searchOptions = {"author":"","title":"","tag":""}
    if request.method == "POST":
        formname = request.form['form-name']
        if formname == "add":
            title = request.form['title']
            author = request.form['author']
            desc = request.form['desc']
            event = request.form['event']
            _file = request.files['file']
            publication = Documents(type="presentation-{}".format(presentation), title=title, author=author, desc=desc, filename=_file.filename, file=_file.read(), event=event)
            db.session.add(publication)
            db.session.commit()
            flash("Added {}".format(title))
        else:
            search = request.form['form-name']
            event = request.form['event']
            author = request.form['author']
            title = request.form['title']
            searchOptions = {"author":author,"title":title,"tag":tags}
    return render_template(**permission_check("dashboard/files/presentations.html".format(presentation),
                                              **get_var(session)),
                                              tags=list_presentation_groups(presentation,searchOptions),
                                              section=presentation,
                                              events=list_events(),
                                              lang=translator(session["lang"]))



@app.route("/dashboard/gallery", methods=['GET', "POST"])
def dashboard_gallery():
    if request.method == "POST":
        files = request.files.getlist("images")
        folder = request.form["folder"]
        for photo in files:
            pic = Photos(type=folder, title=photo.filename, filename=photo.filename, file=photo.read())
            db.session.add(pic)
            db.session.commit()
        flash("Uploaded")
    return render_template(**permission_check("dashboard/files/gallery.html",
                                              **get_var(session)),
                                              types = config.PHOTOS_TYPE,
                                              lang=translator(session["lang"]))

@app.route("/dashboard/gallery/<type>", methods=['GET', "POST"])
def dashboard_gallery_type(type):
    return render_template(**permission_check("dashboard/files/photos.html",
                                              **get_var(session)),
                                              collection = Photos.query.filter(Photos.type==type).all(),
                                              lang=translator(session["lang"]))

@app.route("/dashboard/gallery/send/<photo>", methods=['GET', "POST"])
def dashboard_gallery_return(photo):
    _file = Photos.query.filter_by(id=photo).first()
    return send_file(BytesIO(_file.file), attachment_filename=_file.filename)


    #########################
    #########################
    ###   DashBoard EDIT  ###
    #########################
    #########################


@app.route("/dashboard/edit/home", methods=['GET', "POST"])
def dashboard_edit_home():
    if request.method == "POST":
        headen = request.form['headen']
        headpl = request.form['headpl']
        bodyen = request.form['bodyen']
        bodypl = request.form['bodypl']
        post = Posts(head_pl=headpl, head_en=headen,
                    body_en=bodyen, body_pl=bodypl)
        db.session.add(post)
        db.session.commit()
        flash("Added")
    return render_template(**permission_check("dashboard/edit/home.html", **
                                              get_var(session)),
                                              posts=list_posts(),
                                              edit_header="Add new message",
                                              edited=None,
                                              lang=translator(session["lang"]))


@app.route("/dashboard/edit/home/<post_id>", methods=['GET', "POST"])
def dashboard_edit_home_post(post_id):
    post = get_post(post_id)
    if request.method == "POST":
        headen = request.form['headen']
        headpl = request.form['headpl']
        bodyen = request.form['bodyen']
        bodypl = request.form['bodypl']
        post.head_en = headen
        post.body_en = bodyen
        post.head_pl = headpl
        post.body_pl = bodypl
        db.session.commit()
        flash("Updated")
    return render_template(**permission_check("dashboard/edit/home.html", **get_var(session)),
                           posts=list_posts(),
                           edit_header="Editing message {}".format(post.id),
                           edited=post,
                           lang=translator(session["lang"]))


@app.route("/dashboard/edit/experiment", methods=['GET', "POST"])
def dashboard_edit_experiment():
    if request.method == "POST":
        bodypl = request.form['bodypl']
        bodyen = request.form['bodyen']
        post = Home(body_pl=bodypl, body_en=bodyen,
                    head_pl="", head_en="",loc="",lang="")
        db.session.add(post)
        db.session.commit()
        flash("Added")
        deploy_homepage()
    return render_template(**permission_check("dashboard/edit/experiment.html", **
                                              get_var(session)), posts=list_home(),
                                              edit_header="New Experiment description",
                                              edited=None,
                                              lang=translator(session["lang"]))


@app.route("/dashboard/edit/experiment/<post_id>", methods=['GET', "POST"])
def dashboard_edit_experiment_post(post_id):
    post = show_home(post_id)
    if request.method == "POST":
        bodypl = request.form['bodypl']
        bodyen = request.form['bodyen']
        post.body_pl = bodypl
        post.body_en = bodyen
        db.session.commit()
        flash("Updated")
        deploy_homepage()
    return render_template(**permission_check("dashboard/edit/experiment.html", **get_var(session)),
                           posts=list_home(),
                           edit_header="Editing info {}".format(post.id),
                           edited=post,
                           lang=translator(session["lang"]))

@app.route("/dashboard/edit/members", methods=['GET', "POST"])
def dashboard_edit_members():
    if request.method == "POST":
        head = request.form['title']
        body = request.form['body']
        post = Post(head=head, body=body)
        db.session.add(post)
        db.session.commit()
        flash("Added")
    return "Permission denied"
    #return render_template(**permission_check("dashboard/edit/members.html", **get_var(session)),
    #                       posts=list_posts(), edit_header="Add new message", organizations=list_members())


    ###############
    # notes & cal #
    ###############

@app.route("/dashboard/notes", methods=['GET', "POST"])
def dashboard_notes():
    return render_template(
        **permission_check("dashboard/notes.html", **get_var(session)),lang=translator(session["lang"]))


@app.route("/dashboard/events", methods=['GET', "POST"])
def dashboard_calendar():
    if request.method == "POST":
        title = request.form['title']
        localization = request.form['localization']
        y, m, d = [ int(i) for i in request.form['date'].split('-') ]
        desc = request.form['desc']
        members = " ".join(request.form.getlist('members'))
        print(members)
        event = Events(title=title, localization=localization,
                        time=dt(y,m,d), desc=desc, members=members)
        db.session.add(event)
        db.session.commit()
        flash("Added")
    return render_template(
        **permission_check("dashboard/events.html",
                            **get_var(session)),
                            events = list_events(),
                            members=Members.query.all(),
                            lang=translator(session["lang"]))


    #####################
    #####################
    ###   Projects    ###
    #####################
    #####################

@app.route("/dashboard/kanban/", methods=['GET', "POST"])
def dashboard_kanban():
    return "Permission denied"


    #####################
    #####################
    ###  git server   ###
    #####################
    #####################

@app.route("/dashboard/git/", methods=['GET', "POST"])
def dashboard_git():
    return render_template(
        **permission_check("dashboard/git/data.html",
                            **get_var(session)),
                            lang=translator(session["lang"]))


    #####################
    #####################
    ### Sending files ###
    #####################
    #####################

@app.route("/sendfile/<types>/<folder>/<filename>", methods=['GET', "POST"])
def send_pub(types,folder,filename):
    path = paths[types]
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

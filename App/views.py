# views.py

import os
import time
from io import BytesIO
from App import app
from App import db
from App.models import *
from App.extensions import *
from flask import render_template, request, redirect, url_for, session, flash, send_file, send_from_directory, g
from werkzeug.utils import secure_filename
exp_img = exp_imgs(app.config["UPLOAD_FOLDER"])



@app.route("/test")
def test():
    x = list_presentation_groups("p-meetings")
    print(x[0].content[1].title)
    return str(len(x))

    #####################
    #####################
    ###  Main NavBar  ###
    #####################
    #####################


@app.route("/lang/<lang>")
def language(lang):
    session["lang"] = lang
    flash("Language switched to {}".format(session["lang"]))
    return redirect(url_for('experiments'))

@app.route("/students")
def home():
    x = {"x":"xx"}
    return render_template("world/home.html", 
                           **get_var(session), posts=list_posts(),lang=translator(session["lang"]), langg=session["lang"])


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
            return redirect(url_for('experiments'))
        else:
            flash(user[0])
    return render_template("world/login.html", **get_var(session),lang=translator(session["lang"]))


@app.route("/logout", methods=['GET', "POST"])
def logout():
    lang = session["lang"]
    session.pop("user", None)
    session["lang"] = lang
    flash("Logged out")
    return redirect(url_for('home'))


@app.route("/experiments", methods=['GET', "POST"])
def experiments():
    print(session["lang"])
    return render_template("world/experiments.html", **
                           get_var(session), imagee=exp_img,lang=translator(session["lang"]), collection=list_photos("public", False))


@app.route("/members")
def members():
    return render_template("world/members.html", **
                           get_var(session), organizations=list_members(),lang=translator(session["lang"]))


@app.route("/publications")
def publications():
    return render_template("world/publications.html", **
                           get_var(session), publications=list_papers("publications"),lang=translator(session["lang"]))

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
        
            publication = Document(type=paper, title=title, author=author, reference=ref, year=int(year), desc=desc, link=link, path=_file.filename, files=_file.read())
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
                                              **get_var(session)), publications=list_papers(paper,searchOptions), section=paper)
                                              
@app.route("/dashboard/<paper>/download/<fileid>", methods=['GET', "POST"])
def dashboard_download(paper,fileid):
    _file = Document.query.filter_by(id=fileid).first()
    return send_file(BytesIO(_file.files), attachment_filename=_file.path)

@app.route("/dashboard/delete/<f>/<item>", methods=['GET', "POST"])
def dashboard_delete(f,item):
    _file = Document.query.filter_by(id=item).one()
    db.session.delete(_file)
    db.session.commit()
    flash("deleted file")
    return render_template(**permission_check("dashboard/files/papers.html"))

@app.route("/dashboard/presentations/<presentation>", methods=['GET', "POST"])
def dashboard_presentations(presentation):
    searchOptions = {"author":"","title":"","tag":""}
    if request.method == "POST":
        formname = request.form['form-name']
        if formname == "add":
            title = request.form['title']
            author = request.form['author']
            desc = request.form['desc']
            group = request.form['group']
            ngroup = request.form['ngroup']
            _file = request.files['file']
            if group == 'new':
                group = ngroup
                if group == "":
                    group = "Unsorted"
            publication = Document(type="p-{}".format(presentation), title=title, author=author, desc=desc, path=_file.filename, files=_file.read(), tags=group)
            db.session.add(publication)
            db.session.commit()
            flash("Added {}".format(title))
            print("add")
        else:
            search = request.form['form-name']
            tags = request.form['tags']
            author = request.form['author']
            title = request.form['title']
            searchOptions = {"author":author,"title":title,"tag":tags}
            print("else")
            print(tags,author,title)
    return render_template(**permission_check("dashboard/files/presentations.html".format(presentation),
                                              **get_var(session)), tags=list_presentation_groups("p-{}".format(presentation),searchOptions), section=presentation)



@app.route("/dashboard/gallery", methods=['GET', "POST"])
def dashboard_gallery():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        #publication = Photo(type="presentation-c", title=title, author=author, reference=ref, year=year, desc=desc, link=link, path="{}{}.pdf".format(paths[""], _filename))
        #db.session.add(publication)
        #db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/photos.html",
                                              **get_var(session)), collection=list_photos("gallery"), imgs=exp_img)

@app.route("/dashboard/gallery/download/<folder>/<fileid>", methods=['GET', "POST"])
def dashboard_gallery_download(folder,fileid):
    collection=list_photos(folder,False)
    return render_template(**permission_check("dashboard/files/img.html",
                                              **get_var(session)), picpath=collection[int(fileid)].path)

@app.route("/dashboard/gallery/<folder>", methods=['GET', "POST"])
def dashboard_gallery_open(folder):
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ref = request.form['ref']
        link = request.form['link']
        desc = request.form['desc']

        #publication = Photo(type="presentation-c", title=title, author=author, reference=ref, year=year, desc=desc, link=link, path="{}{}.pdf".format(paths[""], _filename))
        #db.session.add(publication)
        #db.session.commit()
        flash("Added {}".format(title))
    return render_template(**permission_check("dashboard/files/gallery.html",
                                              **get_var(session)), collection=list_photos(folder,False), imgs=exp_img, folder=folder)

@app.route("/dashboard/data", methods=['GET', "POST"])
def dashboard_data():
    return render_template(
        **permission_check("dashboard/files/data.html", **get_var(session)))


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


@app.route("/dashboard/edit/experiment", methods=['GET', "POST"])
def dashboard_edit_experiment():
    if request.method == "POST":
        head = request.form['title']
        body = request.form['body']
        loc = request.form['loc']
        lang = request.form["lang"]
        desc = request.form["desc"]
        post = Experiment(head=head, body=body, localization=loc, lang=lang,desc=desc)
        db.session.add(post)
        db.session.commit()
        flash("Added")
    return render_template(**permission_check("dashboard/edit/experiment.html", **
                                              get_var(session)), posts=list_exp(), edit_header="Add new message")


@app.route("/dashboard/edit/experiment/<post_id>", methods=['GET', "POST"])
def dashboard_edit_experiment_post(post_id):
    post = get_exp(post_id)
    if request.method == "POST":
        head = request.form['title']
        body = request.form['body']
        loc = request.form['loc']
        lang = request.form["lang"]
        desc = request.form["desc"]
        post.head = head
        post.body = body
        post.lang = lang
        post.desc = desc
        post.localization = loc
        db.session.commit()
        flash("Updated")
    return render_template(**permission_check("dashboard/edit/experiment.html", **get_var(session)),
                           posts=list_exp(), edit_header="Editing {}".format(post.head), title=post.head, body=post.body, loc=post.localization, lang=post.lang, desc=post.desc)

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

    #####################
    #####################
    ###  git server   ###
    #####################
    #####################

@app.route("/dashboard/git/", methods=['GET', "POST"])
def dashboard_git():
    return render_template(
        **permission_check("dashboard/git/home.html", **get_var(session)))

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
    return render_template("404.html", **get_var(session)), 404

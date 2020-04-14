# views/files.py

from .modules import *

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
                                              session),
                                              publications=list_papers(paper,searchOptions),
                                              section=paper)


@app.route("/dashboard/<paper>/download/<fileid>", methods=['GET', "POST"])
def dashboard_download(paper,fileid):
    _file = Documents.query.filter_by(id=fileid).first()
    return send_file(BytesIO(_file.file), attachment_filename=_file.filename+".pdf")

@app.route("/dashboard/delete/<f>/<item>", methods=['GET', "POST"])
def dashboard_delete(f,item):
    _file = Documents.query.filter_by(id=item).one()
    #db.session.delete(_file)
    _file.desc = "to delete"
    db.session.commit()
    flash("Report sent")
    return redirect(url_for('dashboard_publications',paper='publications'))
    #return render_template(**permission_check("dashboard/files/papers.html", session))

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
                                              session),
                                              edited=Documents.query.filter(Documents.id==item).first())

@app.route("/dashboard/presentations/<presentation>", methods=['GET', "POST"])
def dashboard_presentations(presentation):
    searchOptions = {"author":"","title":""}
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
        elif formname == "search":
            author = request.form['author']
            title = request.form['title']
            searchOptions = {"author":author,"title":title}
    return render_template(**permission_check("dashboard/files/presentations.html".format(presentation),
                                              session),
                                              tags=list_presentation_groups(presentation,searchOptions),
                                              section=presentation,
                                              events=list_events())



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
                                              session),
                                              types = config.PHOTOS_TYPE)

@app.route("/dashboard/gallery/<type>", methods=['GET', "POST"])
def dashboard_gallery_type(type):
    return render_template(**permission_check("dashboard/files/photos.html",
                                              session),
                                              collection = Photos.query.filter(Photos.type==type).all())

@app.route("/dashboard/gallery/send/<photo>", methods=['GET', "POST"])
def dashboard_gallery_return(photo):
    _file = Photos.query.filter_by(id=photo).first()
    return send_file(BytesIO(_file.file), attachment_filename=_file.filename)

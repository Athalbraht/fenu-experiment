# views/edit.py

from .modules import *

@app.route("/dashboard/edit/home", methods=['GET', "POST"])
def dashboard_edit_home():
    if request.method == "POST":
        headen = request.form['headen']
        headpl = request.form['headpl']
        bodyen = request.form['bodyen']
        bodypl = request.form['bodypl']
        post = Posts(head_pl=headpl, head_en=headen,
                    body_en=bodyen.replace('\n','<br>'), body_pl=bodypl.replace('\n','<br>'))
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
        post.body_en = bodyen.replace('\n','<br>')
        post.head_pl = headpl
        post.body_pl = bodypl.replace('\n','<br>')
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

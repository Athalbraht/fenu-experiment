# views/forum.py

from .modules import *

@app.route("/dashboard/forum")
def dashboard_forum():
    forum = ForumStruct()
    return render_template(
        **permission_check("dashboard/forum/sections.html",
                            session),
                            forum=forum.forum_sections,
                            new_ans=forum.new_anwsers,
                            new_threads=forum.new_threads,
                            without_ans=forum.without_anwser,
                            #session=locale(nav_p="Forum",nav_c="")
                            )


@app.route("/dashboard/forum/<topic>", methods=['GET', "POST"])
def dashboard_forum_topic(topic):
    if request.method == "POST":
        author = request.form["author"]
        body = request.form["body"]
        _topic = Topics.query.filter(Topics.id==topic).first()

        new_anwser = Anwsers(title="Re:"+_topic.title, body=body.replace('\n','<br>'), category=_topic.category, author=author, topic=topic )
        try:
            db.session.add(new_anwser)
            db.session.commit()
            flash("Added anwser: Re:{}".format(_topic.title))
        except:
            flash("Failed!")
        finally:
            redirect(url_for("dashboard_forum_topic",topic=topic))
    forum = ForumStruct()
    thread = forum.get_thread(topic)
    return render_template(
        **permission_check("dashboard/forum/topic.html",
                            session),
                            thread=thread,
                            forum=forum.forum_sections,
                            #session=locale(nav_p="Forum",nav_c="")
                            )

@app.route("/dashboard/forum/new", methods=['GET', "POST"])
def dashboard_forum_new():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        body = request.form["body"]
        category = request.form["section"]
        new_thread = Topics(title=title, author=author, body=body.replace('\n','<br>'), category=category)
        try:
            db.session.add(new_thread)
            db.session.commit()
            flash("New Thread added: {}".format(title))
        except:
            flash("Failed")
        finally:
            redirect(url_for("dashboard_forum"))
    forum = ForumStruct()
    return render_template(
        **permission_check("dashboard/forum/new_thread.html",
                            session),
                            forum=forum.forum_sections,
                            #session=locale(nav_p="Forum",nav_c="new")
                            )

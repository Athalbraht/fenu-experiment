# views/events.py

from .modules import *

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
                            **permission_check("dashboard/events.html", session),
                            events = list_events(),
                            members=Members.query.all(),
                            lang=translator(session["lang"])
                            )

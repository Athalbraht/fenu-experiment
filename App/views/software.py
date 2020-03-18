# views/software.py

from .modules import *


@app.route("/dashboard/git/", methods=['GET', "POST"])
def dashboard_git():
    return render_template(
        **permission_check("dashboard/git/data.html",
                            **get_var(session)),
                            lang=translator(session["lang"]))

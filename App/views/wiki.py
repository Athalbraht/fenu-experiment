# views/wiki.py

from .modules import *

@app.route("/dashboard/wiki", methods=['GET', "POST"])
def dashboard_wiki():
    if request.method == "POST":
        flash("Added")
    return "Permission denied"

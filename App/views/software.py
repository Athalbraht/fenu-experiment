# views/software.py

from .modules import *
from App.api import *


@app.route("/dashboard/git/", methods=['GET', "POST"])
def dashboard_git():
    repos = git.Repository()
    return render_template(
        **permission_check("dashboard/git/home.html",
                            **get_var(session)),
                            repos=repos.get_repos(),
                            session=locale(nav_p="Software",nav_c="New"),
                            lang=translator(session["lang"]))

@app.route("/dashboard/git/<commit>", methods=['GET', "POST"])
def dashboard_git_commit(commit):
    repos = git.Repository()
    return render_template(
        **permission_check("dashboard/git/data.html",
                            **get_var(session)),
                            repos=repos.get_repos(),
                            comm=Commits.query.filter(Commits.id==commit).first(),
                            session=locale(nav_p="Software",nav_c="Commit"),
                            lang=translator(session["lang"]))

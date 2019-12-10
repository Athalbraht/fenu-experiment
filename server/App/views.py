# views.py

from App import app
from App.models import *

from flask import render_template, request, redirect, url_for,  session, flash, send_file, send_from_directory, g

@app.route("/test", methods=['GET', "POST"])
def test():
	return render_template("test.html", status=session["status"])

#####################
###  Main NavBar  ###
#####################

@app.route("/")
def home():
	return render_template("index.html", **get_var(session))

@app.route("/login", methods=['GET', "POST"])
def login():
	if request.method == "POST":
		password = request.form['password']
		login = check_password(password)
		if login[1]:
			session["user"] = "Admin"
			session["status"] = "Log out"
			flash(login[0])
			return redirect(url_for('home'))
		else:
			if len(password)>2:
				flash(login[0])
	return render_template("login.html", **get_var(session))

@app.route("/logout", methods=['GET', "POST"])
def logout():
	session.pop("user", None)
	flash("Logged out")
	return redirect(url_for('home'))

@app.route("/experiments", methods=['GET', "POST"])
def experimants():
	return render_template("experiments.html", **get_var(session))

@app.route("/presentations", methods=['GET', "POST"])
def presentations():
	return render_template("presentations.html", **get_var(session))

@app.route("/members", methods=['GET', "POST"])
def members():
	return render_template("members.html", **get_var(session))

@app.route("/posters", methods=['GET', "POST"])
def posters():
	return render_template("posters.html", **get_var(session))

@app.route("/publications", methods=['GET', "POST"])
def publications():
	return render_template("publications.html", **get_var(session))

@app.route("/links", methods=['GET', "POST"])
def links():
	return render_template("links.html", **get_var(session))

#####################
###   DashBoard   ###
#####################

@app.route("/dashboard", methods=['GET', "POST"])
def dashboard():
	if session["admin"]:
		return render_template("dashboard.html", **get_var(session))
	else:
		flash("Permission denied. Log in first.")
		return redirect(url_for('login'))

#####################
### Sending files ###
#####################

@app.route("/publications/<filename>", methods=['GET', "POST"])
def send_pub(filename):
	return send_from_directory(directory="uploads/publications", filename=filename, as_attachment=False)

###############
### Session ###
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

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

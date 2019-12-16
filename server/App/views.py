# views.py

import os
from App import app
from App import db
from App.models import *
from App.extensions import *
from flask import render_template, request, redirect, url_for,  session, flash, send_file, send_from_directory, g
exp_img = exp_imgs(app.config["UPLOAD_FOLDER"])

@app.route("/test")
def test():
	u = User.query.get(2)
	o = Organization.query.get(1)
	return str(u.affilation.head)

#####################
###  Main NavBar  ###
#####################

@app.route("/home")
def home():
	return render_template("world/home.html", **get_var(session))

@app.route("/")
def main():
	return redirect(url_for('home'))

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
			flash(login[0])
	return render_template("world/login.html", **get_var(session))

@app.route("/logout", methods=['GET', "POST"])
def logout():
	session.pop("user", None)
	flash("Logged out")
	return redirect(url_for('home'))

@app.route("/experiments", methods=['GET', "POST"])
def experimants():
	return render_template("world/experiments.html", **get_var(session), imagee=exp_img)

@app.route("/presentations", methods=['GET', "POST"])
def presentations():
	return render_template("world/presentations.html", **get_var(session))

@app.route("/members", methods=['GET', "POST"])
def members():
	return render_template("world/members.html", **get_var(session))

@app.route("/posters", methods=['GET', "POST"])
def posters():
	return render_template("world/posters.html", **get_var(session))

@app.route("/publications", methods=['GET', "POST"])
def publications():
	return render_template("world/publications.html", **get_var(session))

@app.route("/links", methods=['GET', "POST"])
def links():
	return render_template("world/links.html", **get_var(session))

#####################
###   DashBoard   ###
#####################

def permission_check(template, *args, **kwargs):
	if session["admin"]:
		_kwargs = {"template_name_or_list":template}
		_kwargs.update(kwargs)
		return _kwargs
	else:
		_kwargs = {"template_name_or_list":"world/home.html"}
		_kwargs.update(get_var(session))
		flash("Permission denied. Log in first.")
		return _kwargs

@app.route("/dashboard", methods=['GET', "POST"])
def dashboard():
	return render_template(**permission_check("dashboard.html", **get_var(session)))

@app.route("/dashboard/files", methods=['GET', "POST"])
def dashboard_files():
	return render_template(**permission_check("dashboard/files.html", **get_var(session)))

@app.route("/dashboard/notes", methods=['GET', "POST"])
def dashboard_notes():
	return render_template(**permission_check("dashboard/notes.html", **get_var(session)))

@app.route("/dashboard/calendar", methods=['GET', "POST"])
def dashboard_calendar():
	return render_template(**permission_check("dashboard/calendar.html", **get_var(session)))

@app.route("/dashboard/publications", methods=['GET', "POST"])
def dashboard_publications():
	return render_template(**permission_check("dashboard/files/publications.html", **get_var(session)))
	
@app.route("/dashboard/photos", methods=['GET', "POST"])
def dashboard_photos():
	return render_template(**permission_check("dashboard/files/photos.html", **get_var(session), imgs=exp_img))

@app.route("/dashboard/data", methods=['GET', "POST"])
def dashboard_data():
	return render_template(**permission_check("dashboard/files/data.html", **get_var(session)))

@app.route("/dashboard/logbooks", methods=['GET', "POST"])
def dashboard_logboks():
	return render_template(**permission_check("dashboard/files/logbooks.html", **get_var(session)))

@app.route("/dashboard/posters", methods=['GET', "POST"])
def dashboard_posters():
	return render_template(**permission_check("dashboard/files/posters.html", **get_var(session)))

@app.route("/dashboard/presentations", methods=['GET', "POST"])
def dashboard_presentations():
	return render_template(**permission_check("dashboard/files/presentations.html", **get_var(session)))

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
	return render_template("404.html", **get_var(session)), 404

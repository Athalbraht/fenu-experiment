# views.py

from App import app

from flask import render_template, request, redirect, url_for,  session

@app.route("/")
def home():
	return render_template("index.html")



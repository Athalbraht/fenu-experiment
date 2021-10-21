from .misc import *

@app.route('/home')
def home_page():
    return render_template('main.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/xD')
def dashboard_pagexd():
    return render_template('dashboard2.html')

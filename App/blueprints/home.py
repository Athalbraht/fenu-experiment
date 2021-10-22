from .misc import *

@app.route('/home')
def home_page():
    return render_template('overview.html')


@app.route('/xD')
def dashboard_pagexd():
    return render_template('dashboard/overview.html')

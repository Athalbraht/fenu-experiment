from App import app

from .home import *

@app.route("/")
def main():
    return redirect(url_for('home_page'))

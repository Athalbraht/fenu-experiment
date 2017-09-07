###################################
# Author:       Albert Szadzinski #
# File name:    __init__.py       #
# Date:         06.09.17          #
# Version:      1.0b              #
###################################

import sys
from db_func import *
from flask import Flask, render_template, flash, request, session, redirect, url_for

#setting  default char coding as unicode
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

#creating flask app instance
app = Flask(__name__)
app.debug = True

#Routing

@app.route('/home',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        result = check_passwd(user, password)#getting request from db
        flash(result)#showing db request
        try:
            if result == 'Zalogowano':
                #creating new user session
                session['logged_in'] = True
                session['username'] = user
                #checking permissions
                if get_user_permissions(user) == 'admin':
                    session['permissions'] = True
                else:
                    session['permissions'] = False
                return redirect(url_for('report', username=user, logoutt=True))
        except Exception as e:
            return render_template('home.html', username=str(e))
        return render_template('home.html', username=user)
    else:
        #rendering home page for guest session
        return render_template('home.html', username="Gosc".decode('utf-8'))


@app.route('/report/<username>', methods=['GET','POST'])
def report(username):
    if request.method=='POST':
        topic = request.form['temat'].encode()
        text1 = request.form['text1'].encode()
        text2 = request.form['text2'].encode()
        text3 = 'None'
        #getting text from 3th area for admin users
        if session['permissions']:
            text3 = request.form['text3'].encode()
        #Sending messenges to db
        result = send_notification(get_user_id(session['username']),
                                   topic, text1, text2,text3)
        flash(str(result))#flashing db ans
        return render_template('report.html',username=session['username'],
                               usernav=True,
                               logoutt=True,
                               admin=session['permissions'])
    else:
        return render_template('report.html',
                               username=session['username'],
                               usernav=True,
                               logoutt=True,
                               admin=session['permissions'])


@app.route('/user/<username>', methods=['GET','POST'])
def user(username):
    return render_template('user.html',
                           username=session['username'],
                           usernav=True,
                           logout=True)

@app.route('/list/<username>')
def list_username(username):
    return render_template('list.html',
                           username=session['username'],
                           usernav=True,
                           logoutt=True,
                           admin=session['permissions'])

@app.route('/logout')
def logout():
    flash("Wylogowano")
    session.clear()#removing current user session
    return redirect(url_for('home'))

@app.route('/list/<username>/send')
def database_test(username):
    topic = get_topics(session['username'])
    return render_template('list_extend.html',
                           username=session['username'],
                           usernav=True,
                           logoutt=True,
                           admin=session['permissions'],
                           topic = topic[::-1],
                           )


if __name__ == "__main__":
    app.run()

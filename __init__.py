###################################
# Author:       Albert Szadzinski #
# File name:    __init__.py       #
# Date:         06.09.17          #
# Version:      1.0b              #
###################################

import sys, time, os
from db_func import *
from flask import Flask, render_template, flash, request, session, redirect, url_for
from notifications import *
from werkzeug import secure_filename

#setting  default char coding as unicode
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

upload_folder = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])

#creating flask app instance
app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = upload_folder


#fnc
def allowed_file(filename):
    return '.' in filename and \
filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#Routing
###################################################################################################################

@app.route('/home',methods = ['GET', 'POST'])
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
                    session['nadmin'] = False
                else:
                    session['permissions'] = False
                    session['nadmin'] = True
                return redirect(url_for('list_username',
                                        username = user,
                                        logoutt = True))
        except Exception as e:
            return render_template('home.html',
                                   username = str(e))
        return render_template('home.html',
                               username = user)
    else:
        #rendering home page for guest session
        return render_template('home.html',
                               username = "Gosc".decode('utf-8'))

@app.route('/logout')
def logout():
    flash("Wylogowano")
    session.clear()  # removing current user session
    return redirect(url_for('home'))

@app.route('/search', methods = ['GET','POST'])
def search():
    branches = get_branches()
    results = [[' ',' ',' ','']]
    if request.method == 'POST':
        select = request.form['dzialy']
        surname = request.form['surname']
        date = request.form['date']
        func = request.form['func']
        #flash(searching(surname, date, func, select))
        results = searching(surname, date, func, select)
    return render_template('searching_result.html',
                           username=session['username'],
                           usernav=True,
                           logoutt=True,
                           results = results,
                           branches = branches,
                           admin=session['permissions'])


##################################################################################################################
@app.route('/report/<username>/', methods = ['GET','POST'])
def report_list(username):
    headers = get_headers()[1:]
    j = zip(headers, range(1,len(headers)+1))
    return render_template('report_list.html', username=session['username'],
                           usernav=True,
                           logoutt=True,
                           headers = j,
                           admin=session['permissions'])

@app.route('/report/<username>/<typ>/incydenty')
def incydenty(username, typ):
    incydenty = get_incidents()

    return render_template('incydenty.html', username=session['username'],
                           usernav=True,
                           logoutt=True,
                           incydenty = incydenty,
                           admin=session['permissions'])

@app.route('/report/<username>/<typ>', methods = ['GET','POST'])
def report(username,typ):
    date = str(time.strftime('%d.%m.%y'))
    priorytet = '0'
    ostatniamodyfikacja = date
    delegacja = '0'
    user_data = get_info('*',
                         'users',
                         'login',
                         username)

    if request.method == 'POST':
        kom = request.form['kom'].encode()
        adresat = request.form['adresat'].encode()
        data_zlecenia = request.form['data_zlecenia'].encode()
        data_przyjecia = request.form['data_przyjecia'].encode()
        tresc = request.form['tresc'].encode()
        uzasadnienie_realizacji = request.form['uzasadnienie_realizacji'].encode()

        opis_prac = ""
        data_prac = ""
        uzasadnienie_zakupu = ""
        data_akceptacji_dyrektora = ""
        data_potwierdzenia = ""
        data_zakonczenia =""
        _typ = typ
        zalacznik = ''

        #getting text from 3th area for admin users
        if session['permissions']:
            opis_prac = request.form['opis_prac'].encode()
            data_prac = request.form['data_prac'].encode()
            uzasadnienie_zakupu = request.form['uzasadnienie_zakupu'].encode()
            data_akceptacji_dyrektora = request.form['data_akceptacji_dyrektora'].encode()
            data_potwierdzenia = request.form['data_potwierdzenia'].encode()
            data_zakonczenia = request.form['data_zakonczenia'].encode()
            priorytet = request.form['priorytet'].encode()
            ostatniamodyfikacja = request.form['ostatniamodyfikacja'].encode()
            delegacja = request.form['delegacja'].encode()
            zalacznik = request.form['zalacznik'].encode()

        #Sending messenges to db
        result = send_notification(get_user_id(session['username']),
                                   data_zlecenia, data_przyjecia, tresc, uzasadnienie_realizacji,
                                   opis_prac, data_prac, uzasadnienie_zakupu, data_akceptacji_dyrektora,
                                   data_potwierdzenia, data_zakonczenia, adresat, kom, typ, priorytet, ostatniamodyfikacja,
                                   delegacja, zalacznik)

        flash(str(result))#flashing db ans
        return render_template('report.html',username = session['username'],
                               usernav = True,
                               logoutt = True,
                               date = date,
                               branch = user_data[0][5],
                               priorytet = priorytet,
                               ostatniamodyfikacja = ostatniamodyfikacja,
                               delegacja = delegacja,
                               name = user_data[0][1],
                               surname = user_data[0][2],
                               admin = session['permissions'])
    else:
        return render_template('report.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               date=date,
                               branch=user_data[0][5],
                               priorytet=priorytet,
                               delegacja = delegacja,
                               ostatniamodyfikacja=ostatniamodyfikacja,
                               name=user_data[0][1],
                               surname=user_data[0][2],
                               admin = session['permissions'])

########################################################################################################################

@app.route('/list/<username>')
def list_username(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    tr2 = 0
    if session['permissions']:
        new = get_all_topics(session['username'])
        all_done = get_all_done(session['username'])
        return render_template('list.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               tr2=len(new),
                               admin = session['permissions'],
                               nadmin = session['nadmin'])
    else:
        return render_template('list.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               #tr2=len(new),
                               admin = session['permissions'],
                               nadmin = session['nadmin'])


@app.route('/list/<username>/send')
def database_test(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    tr2 = 0
    if session['permissions']:
        new = get_all_topics(session['username'])
        all_done = get_all_done(session['username'])
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               tr2=len(new),
                               topic=topic[::-1],
                               admin = session['permissions'],
                               nadmin = session['nadmin'])
    else:
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr=len(topic),
                               #tr2=len(done),
                               admin = session['permissions'],
                               topic = topic[::-1],
                               nadmin = session['nadmin']
                               )

@app.route('/list/<username>/old/<nid>')
def old(username, nid):
    notify = get_notification(nid)[0]
    return render_template('oldreport.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           admin = session['permissions'],
                           info = notify)


@app.route('/list/<username>/done')
def done(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    tr2 = 0
    if session['permissions']:
        new = get_all_topics(session['username'])
        all_done = get_all_done(session['username'])
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               tr2=len(new),
                               topic=done[::-1],
                               admin = session['permissions'],
                               nadmin = session['nadmin'])
    else:
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               #tr2 = len(new),
                               admin = session['permissions'],
                               topic = done[::-1],
                               nadmin = session['nadmin'])

@app.route('/list/<username>/new')
def news(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    new = get_all_topics_forme(session['username'])
    all_done = get_all_done(session['username'])
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           tr = len(topic),
                           tr2 = len(new),
                           admin = session['permissions'],
                           topic = new[::-1],
                           nadmin = session['nadmin'])

@app.route('/list/<username>/newall')
def newsall(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    new = get_all_topics_all()
    all_done = get_all_done(session['username'])
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           tr = len(topic),
                           tr2 = len(new),
                           admin = session['permissions'],
                           topic = new[::-1],
                           nadmin = session['nadmin'])


@app.route('/list/<username>/freeze')
def freeze(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    new = get_freeze()
    all_done = get_all_done(session['username'])
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           tr = len(topic),
                           tr2 = len(new),
                           admin = session['permissions'],
                           topic = new[::-1],
                           nadmin = session['nadmin'])

@app.route('/list/<username>/oldm')
def oldmine(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    new = get_done_forme(session['username'])
    all_done = get_all_done(session['username'])
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           tr = len(topic),
                           tr2 = len(new),
                           admin = session['permissions'],
                           topic = new[::-1],
                           nadmin = session['nadmin'])


@app.route('/list/<username>/all_done')
def all_done(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    new = get_all_topics(session['username'])
    all_done = get_all_done(session['username'])
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           tr = len(topic),
                           tr2 = len(new),
                           admin = session['permissions'],
                           topic = all_done[::-1],
                           nadmin = session['nadmin'])

@app.route('/list/<username>/new/<nid>', methods = ['GET','POST'])
def news_edit(username, nid):
    notify = get_notification(nid)[0]
    date = str(time.strftime('%d.%m.%y'))
    uid = get_info('uid',
                   'notifications',
                   'nid',
                   nid)
    branch = get_info('branch',
                      'users',
                      'uid',
                      uid)

    data = get_users_data(get_user_login(uid))

    if request.method == 'POST':
        kom = request.form['kom'].encode()
        adresat = request.form['adresat'].encode()
        data_zlecenia = request.form['data_zlecenia'].encode()
        data_przyjecia = request.form['data_przyjecia'].encode()
        tresc = request.form['tresc'].encode()
        uzasadnienie_realizacji = request.form['uzasadnienie_realizacji'].encode()
        chb = request.form.getlist('checkbox')
        flash(chb)
        opis_prac = ''
        data_prac = ''
        uzasadnienie_zakupu = ''
        data_akceptacji_dyrektora = ''
        data_potwierdzenia = ''


        #getting text from 3th area for admin users
        if session['permissions']:
            opis_prac = request.form['opis_prac'].encode()
            data_prac = request.form['data_prac'].encode()
            uzasadnienie_zakupu = request.form['uzasadnienie_zakupu'].encode()
            data_akceptacji_dyrektora = request.form['data_akceptacji_dyrektora'].encode()
            data_potwierdzenia = request.form['data_potwierdzenia'].encode()
            data_zakonczenia = request.form['data_zakonczenia'].encode()
        priorytet = request.form['priorytet'].encode()
        ostatniamodyfikacja = date.encode()
        delegacja = request.form['delegacja'].encode()
        zalacznik = request.form['zalacznik'].encode()
        if len(chb) != 0:
            data_zakonczenia = 'freeze'
        else:
            data_zakonczenia = ''
        #Sending messenges to db
        result = save_notification(nid, uid, data_zlecenia, data_przyjecia, tresc,
                                   uzasadnienie_realizacji, opis_prac, data_prac, uzasadnienie_zakupu,
                                   data_akceptacji_dyrektora, data_potwierdzenia, data_zakonczenia, adresat,
                                   kom,get_type_from_nid(nid), priorytet, ostatniamodyfikacja, delegacja, zalacznik)

        flash(str(result))#flashing db ans

        return render_template('oldreport_admin.html',
                               username=session['username'],
                               usernav=True,
                               logoutt=True,
                               admin=session['permissions'],
                               info=notify)
    else:
        return render_template('oldreport_admin.html',
                               username=session['username'],
                               usernav=True,
                               logoutt=True,
                               name = data[0][0],
                               surname = data[0][1],
                               admin=session['permissions'],
                               info=notify)

####################################################################################################################

@app.route('/adminpanel/<username>')
def adminpanel(username):
    _users = get_users()
    len_users = len(_users)
    return render_template('adminpanel.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           admin = session['permissions'],
                           inverse = True,
                           lenusers = len_users)


@app.route('/users')
def users():
    _users = get_users()
    len_users = len(_users)
    return render_template('user.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           admin = session['permissions'],
                           inverse = True,
                           users = _users,
                           lenusers = len_users)
#######################################################################################################################
'''@app.route('/users/<login>', methods=['GET','POST'])
def user_edit(login):
    notify = get_notification(nid)[0]
    date = str(time.strftime('%d.%m.%y'))
    branch = get_branch(username)

    if request.method == 'POST':
        kom = request.form['kom'].encode()


        #Sending messenges to db
        result =


        return render_template('user_edit.html',
                               username=session['username'],
                               usernav=True,
                               logoutt=True,
                               admin=session['permissions'],
                               info=notify)
    else:
        return render_template('user_edit.html',
                               username=session['username'],
                               usernav=True,
                               logoutt=True,
                               admin=session['permissions'],
                               info=notify)'''
#######################################################################################################################
if __name__ == "__main__":
    app.run()

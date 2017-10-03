#####################################
# Author:       Albert Szadzinski   #
# File name:    __init__.py         #
# Date:         16.09.17            #
# Version:      1.7                 #
#####################################

import sys, time, os, print_pdf
from db_func import *
from flask import Flask, render_template, flash, request, session, redirect, url_for, send_file
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

########################################## MAIN ROUTING ###########################################################
###################################################################################################################

@app.route('/home',methods = ['GET', 'POST'])
def home():
    #setting session variables for guest raporting
    session['guest'] = True
    session['username'] = 'Anonim'
    session['permissions'] = False
    session['logged_in'] = False
    session['nadmin'] = False

    #Opening session
    if request.method == 'POST':
        user = request.form['username'] #getting login
        password = request.form['password'] #getting password
        result = check_passwd(user, password) #getting request from db
        flash(result)#showing db request

        try:
            if result == 'Zalogowano':
                #creating new user session
                session['logged_in'] = True
                session['guest'] = False
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
                                        logoutt = session['logged_in']))
        except Exception as e:
            return render_template('home.html',
                                   username = str(e))

        return render_template('home.html',
                               username = user,
                               guest = session['guest'])
    else:
        #rendering home page for guest session
        return render_template('home.html',
                               username = "Gosc".decode('utf-8'),
                               guest = session['guest'])

@app.route('/logout')
def logout():
    flash("Wylogowano")
    session.clear()  # removing current user session
    return redirect(url_for('home'))



@app.route('/search', methods = ['GET','POST'])
def search():
    branches = get_branches() #getting branches from config file
    results = [['','','','']] #temporary list for db answer
    if request.method == 'POST':
        select = request.form['dzialy'].encode()
        surname = request.form['surname'].encode()
        date = request.form['date'].encode()
        func = request.form['func'].encode()
        #flash(searching(surname, date, func, select))
        results = searching(surname, date, func, select)

    return render_template('searching_result.html',
                           username=session['username'],
                           usernav= True,
                           logoutt=True,
                           results = results,
                           branches = branches,
                           admin=session['permissions'])
########################################################################################################################
@app.route('/print/<nid>')
def print_page(nid):
    notify = get_notification(nid)[0] #getting all info for given nid
    uid = get_info('uid',
                   'notifications',
                   'nid',
                   nid)

    data = get_users_data(get_user_login(uid))

    name = data[0][0]
    surname = data[0][1]
    kom = notify[13]
    adr = notify[12]
    dwys = notify[2]
    dprz = notify[3]
    tresc = notify[4]
    uzass = notify[5]
    opis = notify[6]
    dzak = notify[7]
    dwyk = notify[7]
    uzas = notify[8]
    akcep = notify[9]
    potw = notify[10]
    zak = notify[11]
    return render_template('print_template.html',
                           kom = kom,
                           name = name,
                           surname = surname,
                           adr = adr,
                           dwys = dwys,
                           dprz = dprz,
                           tresc = tresc,
                           uzass = uzass,
                           opis = opis,
                           dzak = dzak,
                           dwyk = dwyk,
                           uzas = uzas,
                           akcep = akcep,
                           potw = potw,
                           zak = zak)
########################################################################################################################
@app.route('/aktualnosci', methods=['GET','POST'])
def aktualnosci():
    date = str(time.strftime('%d.%m.%y')) #getting current server time
    if request.method == "POST":

        temat = request.form['temat'].encode()
        tresc = request.form['tresc'].encode()
        autor = request.form['autor'].encode()
        data_publikacji = request.form['data_publikacji'].encode()

        result = add_news(temat, tresc, autor, data_publikacji)
        flash(result)


    _news = get_info('tytul, tresc, autor, data_publikacji', 'news', '0','0') #getting all news
    _news = _news[::-1][:10] #inverting and cutting news to last ten
    return render_template('news.html',
                           username=session['username'],
                           usernav= session['logged_in'],
                           logoutt=True,
                           date = date,
                           news = _news,
                           guest = session['guest'],
                           admin=session['permissions'])



@app.route('/<username>/stats')
def stats(username):
    return render_template('working.html', username=session['username'],
                           usernav=True,
                           logoutt=True,
                           admin=session['permissions'])

@app.route('/dokumentacja')
def dokumentacja():
    return send_file('/var/www/FlaskApp/FlaskApp/doc/dokumentacja.pdf', attachment_filename='dokumentacja.pdf')

@app.route('/pgp')
def pgpkey():
    return send_file('/var/www/FlaskApp/FlaskApp/static/pgpkey.asc', attachment_filename='pgpkey.asc')

@app.route('/kontakt')
def kontakt():
    return render_template('docs.html', username=session['username'],
                           usernav=session['logged_in'],
                           logoutt=True,
                           guest=session['guest'],
                           admin=session['permissions'])
######################################## REPORTING ###############################################################
##################################################################################################################
@app.route('/report/<username>/', methods = ['GET','POST'])
def report_list(username):
    #Creating main labels with report types
    headers = get_headers()[1:] #getting headers from config file
    j = zip(headers, range(1,len(headers)+1)) #Mearging headers with numbers, its nessesery to primary linking
    return render_template('report_list.html', username=session['username'],
                           usernav=True,
                           logoutt=True,
                           headers = j,
                           admin=session['permissions'])

@app.route('/guest_report/', methods = ['GET','POST'])
def guest_report_list():
    #As upper func but for anonymouse report
    headers = get_headers()[1:]
    j = zip(headers, range(1,len(headers)+1))
    return render_template('guest_report_list.html', username=session['username'],
                           usernav=session['logged_in'],
                           logoutt=True,
                           headers = j,
                           guest = session['guest'],
                           admin=session['permissions'])
###################################################################################################################
@app.route('/report/<username>/<typ>/incydenty')
def incydenty(username, typ):
    #creating labels with incidents types
    incydenty = get_incidents() #getting enumerated incidents types from config file
    return render_template('incydenty.html', username=session['username'],
                           usernav=True,
                           logoutt=True,
                           incydenty = incydenty,
                           admin=session['permissions'])

@app.route('/guest_report/<typ>/incydenty')
def guest_incydenty(typ):
    #as upper for guests
    incydenty = get_incidents()
    return render_template('guest_report_incidents.html', username=session['username'],
                           usernav=session['logged_in'],
                           logoutt=True,
                           incydenty = incydenty,
                           guest=session['guest'],
                           admin=session['permissions'])
##################################################################################################################
@app.route('/guest_report/<typ>', methods = ['GET','POST'])
def guest_report(typ):
    #Generate report template for guests
    date = str(time.strftime('%d.%m.%y')) #current date
    priorytet = '0' #priorytet
    ostatniamodyfikacja = date # setting date to last modification label
    delegacja = '0'
    branches = load_branches() #getting branches from config file

    if request.method == 'POST':
        name = request.form['name'].encode()
        surname = request.form['surname'].encode()
        kom = request.form['dzialy'].encode()
        adresat = request.form['adresat'].encode()
        data_zlecenia = date.encode()
        data_przyjecia = date.encode()
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

        a = str(int(time.time()))
        add_user(name, surname, a.encode(), 'none'.encode(),''.encode(), kom, 'brak'.encode())
        uid = get_info('uid','users','login',a)

        #Sending messenges to db
        result = send_notification(uid,
                                   data_zlecenia, data_przyjecia, tresc, uzasadnienie_realizacji,
                                   opis_prac, data_prac, uzasadnienie_zakupu, data_akceptacji_dyrektora,
                                   data_potwierdzenia, data_zakonczenia, adresat, kom, typ, priorytet, ostatniamodyfikacja,
                                   delegacja, zalacznik)

        flash(str(result))#flashing db ans
        return render_template('report.html',username = session['username'],
                               usernav = session['logged_in'],
                               logoutt = True,
                               date = date,
                               guest=session['guest'],
                               priorytet = priorytet,
                               ostatniamodyfikacja = ostatniamodyfikacja,
                               delegacja = delegacja,
                               branches = branches,
                               admin = session['permissions'])
    else:
        return render_template('guest_report.html',
                               username = session['username'],
                               usernav = session['logged_in'],
                               logoutt = True,
                               date=date,
                               guest=session['guest'],
                               priorytet=priorytet,
                               branches = branches,
                               delegacja = delegacja,
                               ostatniamodyfikacja=ostatniamodyfikacja,
                               admin = session['permissions'])
###################################################################################################################
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
        #import subprocess as s
        #a = s.check_output('ls',shell = True)
        flash(result)
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
    #Generate notifications labels
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    #labesl for admins
    if session['permissions']:
        fr = get_freeze()
        nm = get_all_topics_forme(session['username'])
        nw = get_all_topics_all()
        nd = get_nd()
        return render_template('list.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               fr = len(fr),
                               nm=len(nm),
                               nw = len(nw),
                               nd = len(nd),
                               admin = session['permissions'],
                               nadmin = session['nadmin'])
    else:
        return render_template('list.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               tr2=len(done),
                               admin = session['permissions'],
                               nadmin = session['nadmin'])
######################################################################################################################
@app.route('/list/<username>/send')
def database_test(username):
    #send messages for usual user
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    if session['permissions']:
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               tr2=len(done),
                               topic=topic[::-1],
                               admin = session['permissions'],
                               nadmin = session['nadmin'])
    else:
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr=len(topic),
                               tr2=len(done),
                               admin = session['permissions'],
                               topic = topic[::-1],
                               nadmin = session['nadmin']
                               )

@app.route('/list/<username>/old/<nid>')
def old(username, nid):
    #Old messages label
    notify = get_notification(nid)[0]
    return render_template('oldreport.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           admin = session['permissions'],
                           info = notify)
######################################################################################################################

@app.route('/list/<username>/done')
def done(username):
    topic = get_topics(session['username'])
    done = get_done(session['username'])
    if session['permissions']:
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               tr2=len(done),
                               topic=done[::-1],
                               admin = session['permissions'],
                               nadmin = session['nadmin'])
    else:
        return render_template('list_extend.html',
                               username = session['username'],
                               usernav = True,
                               logoutt = True,
                               tr = len(topic),
                               tr2 = len(done),
                               admin = session['permissions'],
                               topic = done[::-1],
                               nadmin = session['nadmin'])
######################################################################################################################
                                     #ADMIN M.LABELS
@app.route('/list/<username>/new')
def news(username):
    # messanges for current user
    fr = get_freeze() #freezen mess.
    nm = get_all_topics_forme(session['username']) #Delegated for me
    nw = get_all_topics_all()
    nd = get_nd() # messages without tag
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           fr = len(fr),
                           nm = len(nm),
                           nw = len(nw),
                           nd = len(nd),
                           admin = session['permissions'],
                           topic = nm[::-1],
                           nadmin = session['nadmin'])
##################################################################################################################
@app.route('/list/<username>/newall')
def newsall(username):
    #all messanges
    fr = get_freeze()
    nd = get_nd()
    nm = get_all_topics_forme(session['username'])
    nw = get_all_topics_all()
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           fr = len(fr),
                           nw = len(nw),
                           nm = len(nm),
                           nd = len(nd),
                           admin = session['permissions'],
                           topic = nw[::-1],
                           nadmin = session['nadmin'])
#########################################################################
@app.route('/list/<username>/freeze')
def freeze(username):
    #freezen mess.
    topic = get_topics(session['username'])
    fr = get_freeze()
    nd = get_nd()
    nm = get_all_topics_forme(session['username'])
    nw = get_all_topics_all()
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           fr = len(fr),
                           nm = len(nm),
                           nw =len(nw),
                           nd = len(nd),
                           tr2 = len(topic),
                           admin = session['permissions'],
                           topic = fr[::-1],
                           nadmin = session['nadmin'])
######################################################################
@app.route('/list/<username>/oldm')
def oldmine(username):
    #messenges without delegation
    fr = get_freeze()
    nd = get_nd()
    nm = get_all_topics_forme(session['username'])
    nw = get_all_topics_all()
    return render_template('listadmin_extend.html',
                           username = session['username'],
                           usernav = True,
                           logoutt = True,
                           nm = len(nm),
                           nw = len(nw),
                           nd = len(nd),
                           fr = len(fr),
                           admin = session['permissions'],
                           topic = nd[::-1],
                           nadmin = session['nadmin'])
#######################################################################
@app.route('/list/<username>/all_done')
def all_done(username):
    #propably unnessesery but...
    topic = get_topics(session['username'])
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
##################################################################################################3####################
@app.route('/list/<username>/new/<nid>', methods = ['GET','POST'])                    # TO DO!!!!                               <-- CHECK THIS!
def news_edit(username, nid):
    notify = get_notification(nid)[0]
    date = str(time.strftime('%d.%m.%y'))
    admins = get_info('uid, surname','users','uprawnienia','admin')
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

        _delegacja = request.form['delegacja'].encode()
        delegacja = get_info('uid', 'users','surname',_delegacja)

        zalacznik = 'NONE'.encode()
        if len(chb) != 0:
            data_zakonczenia = 'freeze'
        else:
            data_zakonczenia = request.form['data_zakonczenia'].encode()
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
                               uid = nid,
                               admins = admins,
                               admin=session['permissions'],
                               info=notify)
    else:
        return render_template('oldreport_admin.html',
                               username=session['username'],
                               usernav=True,
                               uid = nid,
                               logoutt=True,
                               admins = admins,
                               name = data[0][0],
                               surname = data[0][1],
                               admin=session['permissions'],
                               info=notify,
                               deleg = get_info('surname', 'users','login',session['username'])[0][0])

######################################## ADMIN PANEL ##################################################################
#######################################################################################################################
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
#######################################################################################
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
###########################################################################################
@app.route('/delete_user/<uid>')
def delete_userr(uid):
    delete_user(uid)
    flash('Usunieto')
    return redirect(url_for('users'))
#################################################################
@app.route('/users/add', methods = ['GET','POST'])
def new_user():
    branches = load_branches()
    if request.method == 'POST':
        name = request.form['name'].encode()
        surname = request.form['surname'].encode()
        login = request.form['login'].encode()
        passwd = request.form['passwd'].encode()
        function = request.form['function'].encode()
        branch = request.form['branch'].encode()
        permissions = request.form['permissions'].encode()
        if check_login(login):
            result = add_user(name, surname, login, passwd, function, branch, permissions)
            flash('Dodano')
        else:
            flash('Istnieje taki login')
    return render_template('new_user.html',
                           username=session['username'],
                           usernav=True,
                           logoutt=True,
                           branches = branches,
                           admin=session['permissions'])
############################################################################################
@app.route('/users/<uid>', methods = ['GET','POST'])
def user_edit(uid):
    branches = load_branches()
    user_data = get_info('name, surname, login, passwd, function, uprawnienia, branch','users','uid',uid)
    if request.method == 'POST':
        name = request.form['name'].encode()
        surname = request.form['surname'].encode()
        login = request.form['login'].encode()
        passwd = request.form['passwd'].encode()
        function = request.form['function'].encode()
        branch = request.form['branch'].encode()
        permissions = request.form['permissions'].encode()

        result = edit_user(uid, name, surname, login, passwd, function, branch, permissions)
        flash(result)

    return render_template('user_edit.html',
                           username=session['username'],
                           usernav=True,
                           us = user_data[0],
                           logoutt=True,
                           branches = branches,
                           admin=session['permissions'])
#######################################################################################################################
#                                       FINALLY THE END............
#######################################################################################################################
if __name__ == "__main__":
    app.run()

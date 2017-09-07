#####################################
# this file is a part of Flask      #
# app project                       #
#####################################
from database_connect import connection
import gc, sys

#setting unicode char formatting
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

#verify user password
def check_passwd(login, passwd):
    c, cnn = connection()#creating cursor
    c.execute("""SELECT passwd FROM users WHERE login=(%s)""", (login,))#getting password from db
    try:
        temp = c.fetchall()[0][0]#request text format
        if temp != '' and temp == passwd:
            return 'Zalogowano'
        else:
            return 'Niepoprawne dane logowania!'
    except:
        return 'Niepoprawne dane logowania!'
    finally:
        c.close()
        cnn.close()
        #  gc.collect()

def show_current_users():
    pass

def send_notification(user, topic, text1, text2, text3):
    try:
        c, cnn = connection()
        c.execute("""INSERT INTO notifications (uid, topic, content, content2, content3) VALUES (%s, %s, %s, %s, %s)""", (user, topic, text1, text2, text3))
        cnn.commit()#accepting db changes
        return "Wyslane"
    except Exception as e:
        return str(e)
    finally:
        c.close()
        cnn.close()

def get_user_id(login):
    c, cnn = connection()
    c.execute("""SELECT uid FROM users WHERE login=(%s)""", (login,))
    try:
        temp = c.fetchall()[0][0]
        return temp
    except:
        return None
    finally:
        c.close()
        cnn.close()

def get_user_permissions(login):
    c, cnn = connection()
    c.execute("""SELECT uprawnienia FROM users WHERE login=(%s)""", (login,))
    try:
        temp = c.fetchall()[0][0]
        return temp
    except:
        return None
    finally:
        c.close()
        cnn.close()

def get_topics(login):
    c, cnn = connection()
    c.execute("""SELECT topic, content FROM notifications WHERE uid=(%s)""", (get_user_id(login),))
    temp = c.fetchall()
    try:
        return temp
    except:
        return ['blad'], ['odczytu']
    finally:
        c.close()
        cnn.close()
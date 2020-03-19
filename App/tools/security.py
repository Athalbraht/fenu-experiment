# tools/security.py

import os
import hashlib
from App import db
from App.models import *

def hash_password(passwd):
    _salt = os.urandom(32)
    _hash = hashlib.pbkdf2_hmac("sha256", passwd.encode("utf-8"), _salt, 100000)
    return _salt+_hash

def check_password(passwd, login="admin"):
    if login == 'admin':
        user = Users.query.filter(Users.id == 0).all()
    else:
        user = Users.query.filter(Members.email==login).all()
    if len(user) == 1:
        salt, _hash = user[0].password_hash[:32], user[0].password_hash[32:]
        _chash =  hashlib.pbkdf2_hmac("sha256", passwd.encode("utf-8"), salt, 100000)
        if salt+_chash == salt+_hash:
            return "Correct password. Dashboard unlocked.", True, user[0].id
        else:
            return "Wrong password. Try again.", False, None
    else:
        return "Wrong password. Try again.", False, None

def get_var(session):
    var = {
        "username": session["username"],
        "status": session["status"],
        "guest": session["guest"],
        "login": session["logged_in"],
        "admin": session["admin"],
    }
    return var

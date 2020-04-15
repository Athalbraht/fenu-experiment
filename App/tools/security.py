# tools/security.py

import os
import hashlib
import string
import random
from App import db
from App.models import *

def hash_password(passwd, n=32):
    _salt = os.urandom(n)
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
        username = "FeNu_user"
        if salt+_chash == salt+_hash:
            # return: Message, login status, username, admin
            return "Correct password. Dashboard unlocked for {}".format(username), True, username, user[0].admin
        else:
            return "Wrong password. Try again.", False, None, False
    else:
        return "Wrong password. Try again.", False, None, False

def get_random_string(_len):
    letters = string.ascii_letters+"1234567890"
    _string = [ random.choice(letters) for i in range(_len) ]
    return "".join(_string)

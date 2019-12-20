# extensions.py

import os
from App import db
from App.models import *


##################
# Database query #
##################

def check_password(login, passwd):
    user = User.query.filter(User.email == login)
    if len(user.all()) == 1 and passwd == user[0].password_hash:
        print(user[0].email, user[0].password_hash)
        return "Correct password", True, user[0].email
    else:
        return "Wrong email or password. Try again.", False, None


def list_publications():
    pubs = Document.query.filter(Document.type == "publication")
    pubs2 = pubs.order_by(Document.year.desc()).all()
    return(pubs2)


def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return posts


def get_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    return post


def list_members():
    affiliation = []
    for i, o in enumerate(Organization.query.all()):
        affiliation.append([o.head, []])
        for j, u in enumerate(User.query.filter(
                User.affiliation_id == o.id).all()):
            affiliation[i][1].append(u)
    return affiliation


def test_db():
    pass


###########
# Session #
###########

def get_var(session):
    var = {
        "username": session["username"],
        "status": session["status"],
        "guest": session["guest"],
        "login": session["logged_in"],
        "admin": session["admin"],
    }
    return var


def exp_imgs(folder):
    _exp_images = ["bina{}.jpg".format(i) for i in range(1, 7)]
    _exp_images2 = ["hbina{}.jpg".format(i) for i in range(1, 4)]
    _exp_images2.append("logo.png")
    exp_img = list(map(lambda x: os.path.join(
        folder, x), _exp_images + _exp_images2))
    return exp_img

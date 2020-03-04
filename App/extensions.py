# extensions.py

import os
import hashlib
import config
from App import db
from App.models import *


##################
# Database query #
##################

source = "uploads/"

def export_html(name, content, path=''):
    with open("{}/pl/{}.html".format(config.HOMEPAGE_FOLDER, name),"w") as html:
        html.write(content)
    return None

def translator(lang):
    translation_table = Contents.query.all()
    keys = [ item.loc for item in translation_table ]
    _translations = {}
    for key in keys:
        if lang == 'pl':
            _translations[key] = Contents.query.filter(Contents.loc == key).first().body_pl
        else:
            _translations[key] = Contents.query.filter(Contents.loc == key).first().body_en
    posts = Posts.query.all()
    _translations["icstud"] = []
    for post in posts:
        post2 = []
        if lang == "pl":
            post2 = [post.head_pl, post.body_pl, post.timestamp]
        else:
            post2 = [post.head_en, post.body_en, post.timestamp]
        _translations["icstud"].append(post2)
    exp = Home.query.all()[-1]
    if lang == "pl":
        _translations["icexp"] = exp.body_pl
    else:
        _translations["icexp"] = exp.body_en
    return _translations

def check_password(login, passwd):
    user = Users.query.filter(Users.id == 0)
    if len(user.all()) == 1 and user[0].id== 0:
        salt, _hash = user[0].password_hash[:32], user[0].password_hash[32:]
        _chash =  hashlib.pbkdf2_hmac("sha256", passwd.encode("utf-8"), salt, 100000)
        if salt+_chash == salt+_hash:
            return "Correct password. Dashboard unlocked.", True, user[0].id
        else:
            return "Wrong email or password. Try again.", False, None
    else:
        return "Wrong email or password. Try again.", False, None


def list_papers(_type,search=None):
    _pubs = Documents.query.filter(Documents.type == "paper-{}".format(_type))
    if search != None:
        pubs = _pubs.filter(Documents.title.contains(search["title"]), Documents.year.contains(search["year"]), Documents.author.contains(search["author"]))
    else:
        pubs = _pubs
    _sort = pubs.order_by(Documents.year.desc()).all()
    return(_sort)

def list_posts():
    posts = Posts.query.order_by(Posts.id.desc()).all()
    return posts

def list_exp():
    posts = Home.query.order_by(Home.id.desc()).all()
    return posts

def list_presentation_groups(_type,search=None):
    _presentations = Documents.query.filter(Documents.type == "presentation-{}".format(_type))
    print("presentation-{}".format(_type))
    if search != None:
        presentations = _presentations.filter(Documents.title.contains(search["title"]), Documents.event.contains(search["tag"]), Documents.author.contains(search["author"])).order_by(Documents.timestamp.desc()).all()
    else:
        presentations = _presentations.all()
    tags = set([ i.event for i in presentations ])
    class Tag():
        def __init__(self, id, name, content):
            self.id = id
            self.name = name
            self.content = content
    _tags = [ [] for i in tags]
    for i,tag in enumerate(tags):
        for record in presentations:
            if record.event == tag:
                _tags[i].append(record)
    newtags = []
    for j,sets in enumerate(_tags):
        _event = Events.query.filter(Events.id==list(tags)[j]).first()
        newtags.append(Tag(j,
                    "{}@{}  ({})".format(
                        _event.title, _event.localization, _event.time.strftime("%d-%m-%Y")),
                    sets))
    return newtags

def list_photos(_type,wc=True):
    folders = os.listdir(paths[_type])
    class Group():
        def __init__(self, id, filename,path,wc):
            self.types = _type
            self.filename = filename
            self.id = id
            self.path = path
            if wc:
                self.content = os.listdir(self.path)
                self.content_path = [ os.path.join(path, i) for i in self.content ]
    groups = [Group(i,folders[i], os.path.join(paths[_type],folders[i]),wc) for i in range(len(folders))]
    return groups

def upload_publications():

    return 1


def get_post(post_id):
    post = Posts.query.filter(Posts.id == post_id).first()
    return post

def get_exp(post_id):
    post = Experiments.query.filter(Experiments.id == post_id).first()
    return post

def list_members():
    affiliation = []
    for i, o in enumerate(Organizations.query.all()):
        affiliation.append([o, []])
        for j, u in enumerate(Members.query.filter(
                Members.affiliation == o.id).all()):
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

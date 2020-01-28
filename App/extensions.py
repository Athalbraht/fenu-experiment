# extensions.py

import os
import hashlib
from App import db
from App.models import *


##################
# Database query #
##################

source = "uploads/"

translations = {
               "ihexp":"",
               "ihpub":"",
               "ihmem":"",
               "ihstud":"",
               "ihcon":"",
               "ihdash":"",
               "icpub-year":"",
               "icpub-title":"",
               "icpub-author":"",
               "icpub-download":"",
               "gallery":"",
               "prev":"",
               "next":"",
               "up":"",
               "viewd":"",
               #"icexp-mainphoto":"",
               #"icexp-desc":"",
               

               
               }


paths = {
        "publications":"{}documents/papers/publications/".format(source),
        "thesis":"{}documents/papers/thesis".format(source),
        "manuals":"{}documents/papers/manuals".format(source),
        "loogbooks":"{}documents/papers/logbooks".format(source),
        "posters":"{}documents/presentations/posters".format(source),
        "conferences":"{}documents/presentations/conferences".format(source),
        "meetings":"{}documents/presentations/meetings".format(source),
        "miscellaneous":"{}documents/miscellaneous".format(source),
        "schemes":"{}gallery/schemes".format(source),
        "window":"{}gallery/window".format(source),
        "detector":"{}gallery/detector".format(source),
        "thumbn":"{}gallery/thumbnails".format(source),
        "other":"{}gallery/other".format(source),
        "plans":"{}gallery/plans".format(source),
        "production":"{}gallery/production".format(source),
        "target":"{}gallery/target".format(source),
        "targetchamber":"{}gallery/targetchamber".format(source),
        "salad":"{}gallery/salad".format(source),
        "public":"{}gallery/public".format(source),
        "gallery":"{}gallery".format(source)
       
        }

def translator(lang):
    _translations = translations.copy()
    for key in translations.keys():
        _translations[key] = Content.query.filter(Content.lang == lang, Content.localization == key).first().body
    posts = Post.query.filter(Post.head.contains("[{}]".format(lang))).all()
    _translations["icstud"] = []
    for post in posts:
        _translations["icstud"].append(post)
    exp = Experiment.query.filter(Experiment.lang.contains(lang)).all()
    _translations["icexp"] = []
    for post in exp:
        _translations["icexp"].append(post)
    return _translations

def check_password(login, passwd):
    user = User.query.filter(User.username == login)
    if len(user.all()) == 1 and user[0].username == login:
        salt, _hash = user[0].password_hash[:32], user[0].password_hash[32:]
        _chash =  hashlib.pbkdf2_hmac("sha256", passwd.encode("utf-8"), salt, 100000)
        if salt+_chash == salt+_hash:
            print(user[0].email, user[0].password_hash)
            return "Correct password. Dashboard unlocked.", True, user[0].email
        else:
            return "Wrong email or password. Try again.", False, None
    else:
        return "Wrong email or password. Try again.", False, None


def list_papers(_type,search=None):
    _pubs = Document.query.filter(Document.type == _type)
    if search != None:
        pubs = _pubs.filter(Document.title.contains(search["title"]), Document.year.contains(search["year"]), Document.author.contains(search["author"]))
    else:
        pubs = _pubs
    _sort = pubs.order_by(Document.year.desc()).all()
    return(_sort)

def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return posts
    
def list_exp():
    posts = Experiment.query.order_by(Experiment.id.desc()).all()
    return posts

def list_presentation_groups(_type,search=None):
    '''
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
    '''
    _presentations = Document.query.filter(Document.type == _type)
    if search != None:
        presentations = _presentations.filter(Document.title.contains(search["title"]), Document.tags.contains(search["tag"]), Document.author.contains(search["author"])).order_by(Document.timestamp.desc()).all()
    else:
        presentations = _presentations.all()
    tags = set([ i.tags for i in presentations ])
    class Tag():
        def __init__(self, id, name, content):
            self.id = id
            self.name = name
            self.content = content
    _tags = [ [] for i in tags]
    for i,tag in enumerate(tags):
        for record in presentations:
            if record.tags == tag:
                _tags[i].append(record)
    newtags = []
    for j,sets in enumerate(_tags):
        newtags.append(Tag(j, list(tags)[j], sets))
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
    post = Post.query.filter(Post.id == post_id).first()
    return post

def get_exp(post_id):
    post = Experiment.query.filter(Experiment.id == post_id).first()
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

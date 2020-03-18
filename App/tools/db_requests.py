# tools/db_requests.py

from App.models import *

def list_events():
    events = Events.query.order_by(Events.time.desc()).all()
    return events

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

def list_home():
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


def get_post(post_id):
    post = Posts.query.filter(Posts.id == post_id).first()
    return post

def show_home(post_id):
    post = Home.query.filter(Home.id == post_id).first()
    return post

def list_members():
    affiliation = []
    for i, o in enumerate(Organizations.query.all()):
        affiliation.append([o, []])
        for j, u in enumerate(Members.query.filter(
                Members.affiliation == o.id).all()):
            affiliation[i][1].append(u)
    return affiliation

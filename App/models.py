# models.py
from App import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(
        db.Integer,
        db.ForeignKey("members.id"))
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    title = db.Column(db.String(64))
    affiliation = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"))
    desc = db.Column(db.Text)
    orcid = db.Column(db.String(128))
    rgate = db.Column(db.String(128))
    link = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Member {}>'.format(self.username)


class Organizations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(128), unique=True)
    shortcut = db.Column(db.String(64))
    link = db.Column(db.String(128))
    desc = db.Column(db.Text)
    users = db.relationship("User", backref="affilation", lazy="dynamic")
    def __repr__(self):
        return '<Organization {}>'.format(self.head)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head_en = db.Column(db.Text, nullable=False)
    head_pl = db.Column(db.Text, nullable=False)
    body_en = db.Column(db.Text, nullable=False)
    body_pl = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Post {}>'.format(self.head)


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text)
    reference = db.Column(db.String(256))
    year = db.Column(db.Integer)
    link = db.Column(db.String(128))
    filename = db.Column(db.Text)
    file = db.Column(db.LargeBinary)
    desc = db.Column(db.Text)
    event = db.Column(
        db.Integer,
        db.ForeignKey("events.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Document {}>'.format(self.title)


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    filename = db.Column(db.Text)
    file = db.Column(db.LargeBinary)
    thumbnail = db.Column(db.LargeBinary)
    desc = db.Column(db.Text)
    event = db.Column(
        db.Integer,
        db.ForeignKey("events.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Photo {}>'.format(self.title)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(
        db.Integer,
        db.ForeignKey("events.id"))
    head = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Note {}>'.format(self.head)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    localization = db.Column(db.String(128))
    time = db.Column(db.DateTime)
    desc = db.Column(db.Text)
    members = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Event {}>'.format(self.head)


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(128), nullable=False)
    loc = db.Column(db.String(128), nullable=False)
    head_en = db.Column(db.String(128), nullable=False)
    body_en = db.Column(db.Text)
    head_pl = db.Column(db.String(128), nullable=False)
    body_pl = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Experiment_desc {}>'.format(self.id)


class Contents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.String(128), nullable=False)
    body_en = db.Column(db.Text)
    body_pl = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Content {}>'.format(self.id)

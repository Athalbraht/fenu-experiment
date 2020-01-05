# models.py

from App import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    affiliation_id = db.Column(
        db.String(128),
        db.ForeignKey("organization.id"))
    desc = db.Column(db.Text)
    orcid = db.Column(db.String(128))
    rgate = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(128), unique=True)
    shortcut = db.Column(db.String(64))
    link = db.Column(db.String(128))
    desc = db.Column(db.Text)
    users = db.relationship("User", backref="affilation", lazy="dynamic")

    def __repr__(self):
        return '<Organization {}>'.format(self.head)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.head)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text)
    reference = db.Column(db.String(256))
    year = db.Column(db.Float)
    desc = db.Column(db.Text)
    link = db.Column(db.String(128))
    path = db.Column(db.String(256))
    tags = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Document {}>'.format(self.title)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    path = db.Column(db.String(256))
    xsize = db.Column(db.Float)
    ysize = db.Column(db.Float)
    zoom = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Photo {}>'.format(self.title)


class Bina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)
    abstract = db.Column(db.Text)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Exp_page {}>'.format(self.title)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    head = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Note {}>'.format(self.head)
        
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(128), nullable=False)
    localization = db.Column(db.String(128))
    time = db.Column(db.DateTime)
    desc = db.Column(db.Text)
    members = db.Column(db.Text)
    files = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Note {}>'.format(self.head)

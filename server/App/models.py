# models.py

from App import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	surname = db.Column(db.String(64), index=True, unique=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	permission = db.Column(db.String(128))
	orcid = db.Column(db.String(128))
	rgate = db.Column(db.String(128))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	def __repr__(self):
		return '<User {}>'.format(self.username) 

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(300))
	head = db.Column(db.String(100))
	author = db.Column(db.String(64), index=True, unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	def __repr__(self):
		return '<Post {}>'.format(self.body)

class Document(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	author = db.Column(db.String(150))
	source = db.Column(db.String(150))
	path = db.Column(db.String(150))
	doi = db.Column(db.String(150))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	def __repr__(self):
		return '<Document {}>'.format(self.body)

class Bina(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	head1 = db.Column(db.String(100))
	head2 = db.Column(db.String(100))
	head3 = db.Column(db.String(100))
	body1 = db.Column(db.String(4000))
	body2 = db.Column(db.String(4000))
	body3 = db.Column(db.String(4000))
	body4 = db.Column(db.String(4000))
	body5 = db.Column(db.String(4000))
	body6 = db.Column(db.String(4000))
	author = db.Column(db.String(64), index=True, unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	def __repr__(self):
		return '<BINA {}>'.format(self.body)

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(300))
	head = db.Column(db.String(100))
	author = db.Column(db.String(64), index=True, unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	def __repr__(self):
		return '<Note {}>'.format(self.body)

class Picture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(150))
	xsize = db.Column(db.String(64))
	ysize = db.Column(db.String(64))
	zoom = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	def __repr__(self):
		return '<Picture {}>'.format(self.body)

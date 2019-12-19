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
	affiliation_id = db.Column(db.String(128), db.ForeignKey("organization.id"))
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
	doi = db.Column(db.String(128))
	link = db.Column(db.String(256))
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
	title = db.Column(db.String(128), nullable=False)
	header1 = db.Column(db.String(128), nullable=False)
	desc1 = db.Column(db.Text, nullable=False)
	logo_id1 = db.Column(db.Integer, db.ForeignKey('photo.id'))
	description1 = db.Column(db.Text, nullable=False)
	photo_id1 = db.Column(db.Integer, db.ForeignKey('photo.id'))
	header2 = db.Column(db.String(128), nullable=False)
	desc2 = db.Column(db.Text, nullable=False)
	logo_id2 = db.Column(db.Integer, db.ForeignKey('photo.id'))
	description2 = db.Column(db.Text, nullable=False)
	photo_id2 = db.Column(db.Integer, db.ForeignKey('photo.id'))
	header3 = db.Column(db.String(128), nullable=False)
	desc3 = db.Column(db.Text, nullable=False)
	logo_id3 = db.Column(db.Integer, db.ForeignKey('photo.id'))
	description3 = db.Column(db.Text, nullable=False)
	photo_id3 = db.Column(db.Integer, db.ForeignKey('photo.id'))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	def __repr__(self):
		return '<Exp_page {}>'.format(self.title)

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	head = db.Column(db.Text, nullable=False)
	body = db.Column(db.Text, nullable=False)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	def __repr__(self):
		return '<Note {}>'.format(self.head)


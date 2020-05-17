# models.py

'''
from App import db
from datetime import datetime
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(
        db.Integer,
        db.ForeignKey("members.id"))
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=False)
    affiliation = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    body_pl = db.Column(db.Text, nullable=False)
    file = db.Column(db.LargeBinary)
    def __repr__(self):
        return '<User {}>'.format(self.id)
'''

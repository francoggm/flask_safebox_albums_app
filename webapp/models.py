from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

from . import app

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(250))
    phone = db.Column(db.String(10))
    address = db.Column(db.String(250))
    photo = db.Column(db.LargeBinary)
    albums = db.relationship('Albums')
    def __init__(self, email, password, name, phone) -> None:
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone

class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    pin = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    imgs = db.relationship('Images')
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    img = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
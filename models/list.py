from app import db
from sqlalchemy.sql import func

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='list', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

from app import db
from sqlalchemy.sql import func

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    items = db.relationship('ListItem')
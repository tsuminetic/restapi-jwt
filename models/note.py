from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    
    @validates('due_date')
    def validate_due_date(self, key, due_date):
        if due_date < datetime.datetime.now().date(): 
            raise ValueError('Due date cannot be in the past.')
        return due_date

    
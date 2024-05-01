from app import db

class ListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    list_id=db.Column(db.Integer,db.ForeignKey('list.id'))
    

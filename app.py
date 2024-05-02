from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()



app=Flask(__name__)

app.config['SECRET_KEY']='dasjhghjasbdas'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

api = Api(app)
db.init_app(app)

from models.user import User
from models.note import Note
from models.list import List, Item


with app.app_context():
    db.create_all()

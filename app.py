from flask import Flask, request, make_response, jsonify,render_template
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
# jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])

db = SQLAlchemy()


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='dasjhghjasbdas'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        
        #initializing the db
    db.init_app(app)

    #importing and registering the blueprints
    from views import views

    app.register_blueprint(views, url_prefix='/')

    from models import User

    with app.app_context():
        db.create_all()
    
    return app
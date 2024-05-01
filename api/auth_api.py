from flask import Blueprint, request, make_response, jsonify,render_template,redirect,url_for
import jwt
import datetime
from models.user import User

from werkzeug.security import generate_password_hash,check_password_hash
from app import db

api=Blueprint('auth_api', __name__)


@api.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401


    token = jwt.encode({
        'user':request.form['username'],
        'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=1000)
    },
    'dasjhghjasbdas',algorithm="HS256")
    return redirect(url_for('example_api.protected', token=token))


@api.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
    
        if validatesignup(username,email,password):
            new_user = User(email=email,username=username, password = generate_password_hash(password, method='pbkdf2:sha256'))

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth_api.login'))


    return jsonify({'message':'doen signing up, go login'})


def validatesignup(username, email, password):
    if " " in username or len(username)<4:
        pass
    if len(password)<8:
        return False
    if not "@gmail.com" in email or " " in email:
        return False
    user = User.query.filter_by(email=email).first()
    if user:
        return False
    return True
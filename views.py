from flask import Blueprint, request, make_response, jsonify,render_template,redirect,url_for
import jwt
import datetime
from models import User, Note
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from sqlalchemy.orm import validates

views=Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('login.html')
    

def token_required(f):
    """a decorator to be used only after app.route which checks for token in header as AUthentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization')
        
        if not token:
            token=request.args.get('token')

        if not token:
            return jsonify({'message': 'token is missing!'}), 403
        
        try:
            token = (token.split(" ")[-1])
            print(token)
            data = jwt.decode(token, 'dasjhghjasbdas',algorithms=["HS256"])
            print(data)
            print(data['user'])
            print(User.query.filter_by(username=data['user']).first())
            current_user = User.query.filter_by(username=data['user']).first()
            
        except:
            return jsonify({'message': 'token is invalid!'}), 403

        return f(current_user,token, *args, **kwargs)
    
    return decorated


@views.route('/unprotected/')
def unprotected():
    return jsonify({'message':'Anyone can view this'})

@views.route('/protected')
@token_required
def protected(current_user,token):
    return jsonify({'message':f'welcome, {current_user.username}',
                    'token':token
                    })

@views.route('/allnotes')
@token_required
def allnotes(current_user, token):
    notes={
        'message':f'welcome, {current_user.username}',
        'notes':f'you have {len(current_user.notes)} note(s)',
    }
    for note in current_user.notes:
        if note.completed:
            x='✔'
        else:
            x='x'
        notes[f'{note.id}-----{x}------{note.due_date}']=f'{note.data}'
    return jsonify(notes)

@views.route('/delnote/<int:note_id>', methods=['POST','GET'])
@token_required
def delnote(current_user, token, note_id):
    note = Note.query.get(note_id)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({
        'message':'deleted!'
    })

@views.route('/notecompleted/<int:note_id>', methods=['POST','GET'])
@token_required
def notecompleted(current_user, token, note_id):
    note = Note.query.get(note_id)
    if note:
        if note.user_id==current_user.id:
            note.completed=True
            db.session.commit()
    return jsonify({
        'message':f'note id no {note.id} marked as completed!'
    })

@views.route('/addnote', methods=['POST','GET'])
@token_required
def addnote(current_user, token):
    if request.method=='POST':
        note=request.form['note']
        due_date_str = request.form.get('duedate')

        if len(note) < 1:
            return jsonify({
                    'error':'bad request'
                })
        else:
            try:
                due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                validate_due_date( None, due_date)
            except ValueError as e:
                return jsonify({
                    'error':'bad request'
                })
            new_note = Note(data=note, due_date=due_date, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

    return jsonify({
            'message':'new note added! check /allnotes'
        })

@validates('due_date')
def validate_due_date(key, due_date):
    if due_date < datetime.datetime.now().date(): 
        raise ValueError('Due date cannot be in the past.')
    return due_date



@views.route('/login', methods=['POST','GET'])
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
    return redirect(url_for('views.protected', token=token))


@views.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
    
        if validatesignup(username,email,password):
            new_user = User(email=email,username=username, password = generate_password_hash(password, method='pbkdf2:sha256'))

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('views.login'))


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
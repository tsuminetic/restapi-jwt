from flask import Blueprint, request, make_response, jsonify,render_template
import jwt
import datetime
from functools import wraps

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
            jwt.decode(token, 'dasjhghjasbdas',algorithms=["HS256"])
        except:
            return jsonify({'message': 'token is invalid!'}), 403

        return f(*args, **kwargs)
    
    return decorated


@views.route('/unprotected/')
def unprotected():
    return jsonify({'message':'Anyone can view this'})

@views.route('/protected')
@token_required
def protected():
    return jsonify({'message':'only people with valid tokens can view this'})



@views.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password']=='123456':
        token = jwt.encode({
            'user':request.form['username'],
            'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=10)
        },
        'dasjhghjasbdas',algorithm="HS256")
        return jsonify({'token':token})
    
    return make_response('Could not verify!', 401,{'WWW-Authenticate':'Basic realm:"Login required!"'})
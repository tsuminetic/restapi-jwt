from flask import Flask, request, make_response, jsonify,render_template
import jwt
import datetime
from functools import wraps
# jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])

app=Flask(__name__)
app.config['SECRET_KEY']='dasjhghjasbdas'

@app.route('/')
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
            jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
        except:
            return jsonify({'message': 'token is invalid!'}), 403

        return f(*args, **kwargs)
    
    return decorated


@app.route('/unprotected/')
def unprotected():
    return jsonify({'message':'Anyone can view this'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message':'only people with valid tokens can view this'})



@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password']=='123456':
        token = jwt.encode({
            'user':request.form['username'],
            'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=10)
        },
        app.config['SECRET_KEY'],algorithm="HS256")
        return jsonify({'token':token})
    
    return make_response('Could not verify!', 401,{'WWW-Authenticate':'Basic realm:"Login required!"'})

if __name__ == '__main__':
    app.run(debug=True)
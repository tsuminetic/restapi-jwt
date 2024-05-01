from functools import wraps
from flask import request, jsonify
import jwt
from models.user import User
from functools import wraps


def token_required(f):
    """a decorator to be used only after app.route which checks for token in header as notesentication
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
from flask import Blueprint, jsonify
from utils import auth

api=Blueprint('example_api', __name__)

@api.route('/unprotected/')
def unprotected():
    return jsonify({'message':'Anyone can view this'})

@api.route('/protected')
@auth.token_required
def protected(current_user,token):
    return jsonify({'message':f'welcome, {current_user.username}',
                    'token':token
                    })



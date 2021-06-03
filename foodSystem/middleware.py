from functools import wraps
from flask import Response, request, g, make_response, jsonify

from foodSystem.models import User


def is_authenticated(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').split('Bearer')[1].strip()
            playload = User.decode_auth_token(token)
            if type(playload) == str:
                response = {
                'status': 'fail',
                'message': playload
                }
                return make_response(jsonify(response)), 401
            user_id = playload.get('sub')
            request.user = User.query.filter_by(id=user_id).first()
            return func(*args, **kwargs)

        except Exception as e:
            print(e)
            response = {
                'status': 'fail',
                'message': "Sorry you are not authenticated"
                }
            return make_response(jsonify(response)), 401

    return decorated_function


def is_restaurant(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.user.is_restaurant:
            response = {
                'status': 'fail',
                'message': 'You are not restaurant to do this action'
            }
            return make_response(jsonify(response)), 403
        
        return func(*args, **kwargs)
    return decorated_function


def only_user(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.user.is_restaurant:
            response = {
                'status': 'fail',
                'message': 'restaurant can not make this action'
            }
            return make_response(jsonify(response)), 403
        return func(*args, **kwargs)
    return decorated_function

from flask import request, jsonify
from functools import wraps
from tabulation.config import SECRET_KEY
from tabulation.models.db import User, Role
import jwt


def token_required(allowed_guest):
    def decorator(f):
        wraps(f)
        def wrapper(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token and not allowed_guest:
                response = {
                    'status': 'failed',
                    'message': 'Token is missing.'
                }
                return jsonify(response), 401

            try:

                data = jwt.decode(token, SECRET_KEY)
                current_user = User.query.get(data['public_id'])
                
                if not current_user:
                    current_user = None

            except:

                if not allowed_guest:
                    response = {
                        'status': 'failed',
                        'message': 'Token is missing.'
                    }
                    return jsonify(response), 401

                current_user = None
            
            return f(current_user, *args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator



def is_admin(current_user):
    if not current_user:
        return False

    role = Role.query.get(current_user.role_id)

    if role.code == 1:
        return True
    return False


def is_judge(current_user):
    if not current_user:
        return False
    
    role = Role.query.get(current_user.role_id)

    if role.code == 3:
        return True
    return False


def unauthorized_access():
    return {'status': 'failed', 'message': 'Unauthorized access.'}
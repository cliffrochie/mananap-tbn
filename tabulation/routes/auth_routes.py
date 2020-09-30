from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from tabulation.models.db import *
from tabulation import db
from tabulation.config import SECRET_KEY
from tabulation.utils.functions.access_restriction import token_required

import jwt
import datetime

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = User.query.filter(User.username == auth.username).first()

    if not user:
        return make_response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    if check_password_hash(user.password, auth.password):
        data  =  {
            'public_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(data, SECRET_KEY)

        response = {
            'token': token.decode('UTF-8')
        }
        return jsonify(response)

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@auth.route('/guest', methods=['GET'])
def guest():
    data  =  {
        'public_id': "0",
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }
    token = jwt.encode(data, SECRET_KEY)

    response = {
        'token': token.decode('UTF-8')
    }
    return jsonify(response)


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if data['confirm_password']:
        if data['password'] != data['confirm_password']:
            response = {
                'status': 'failed',
                'message': 'Password does not match.'
            }

            return jsonify(response), 400

    user = User(
        data['username'],
        data['email'],
        generate_password_hash(data['password']),
        data['firstname'],
        data['middlename'],
        data['lastname'],
        data['role_id'],
        data['organization_id']
    )

    db.session.add(user)
    db.session.commit()


    response = {
        'status': 'success',
        'message': 'User created successfully.'
    }

    return jsonify(response), 201

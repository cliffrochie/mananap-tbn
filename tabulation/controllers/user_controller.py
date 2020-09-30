from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError


class UserController:
    """
    +--------------------------------------------------------------------------
    | Method resource
    +--------------------------------------------------------------------------
    | All of the method resources are here.
    | Method lists:
    |    all()
    |    find(id)
    |    create()
    |    update(id)
    |    delete(id)
    |
    """
    
    @staticmethod
    def all():
        try:

            users = User.query.all()
            result = []
            for user in users:
                result.append(format_user(user))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> UserController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }

            return jsonify(response), 400
        

    @staticmethod
    def find(id):
        try:

            user = User.query.get(id)
            return jsonify(format_user(user)), 200

        except AttributeError as e:
            print("\nAttributeError >>> UserController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'User not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400


    @staticmethod
    def create():
        try:

            data = request.get_json()
            user = User(
                data['username'],
                data['email'],
                data['password'],
                data['firstname'],
                data['middlename'],
                data['lastname'],
                data['role_id'],
                data['organization_id']
            )

            db.session.add(user)
            db.session.commit()

            result = format_user(user)

            return jsonify(result), 201

        except TypeError as e:
            print("\nTypeError >>> UserController.create: "+ str(e) +"\n")

            if "'NoneType' object is not subscriptable" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Submitted without data.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Type error'
            }
            return jsonify(response), 400

        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> UserController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the User account you tried to create already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> UserController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

        except InvalidRequestError as e:
            print("\nInvalidRequestError >>> UserController.create: "+ str(e) +"\n")

            if "1062" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the User account you tried to create already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed',
                'message': 'Something went wrong!'
            }
            return jsonify(response), 400


    @staticmethod
    def update(id):
        try:

            data = request.get_json()
            user = User.query.get(id)
            user.username = data['username']
            user.email = data['email']
            user.password = data['password']
            user.firstname = data['firstname']
            user.middlename = data['middlename']
            user.lastname = data['lastname']
            user.is_active = data['is_active']
            user.role_id = data['role_id']
            user.organization_id = data['organization_id']
            db.session.commit()

            result = format_user(user)

            return jsonify(result), 200

        except TypeError as e:
            print("\nTypeError >>> UserController.update: "+ str(e) +"\n")

            if "'NoneType' object is not subscriptable" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Submitted without data.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Type error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> UserController.update: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

        except AttributeError as e:
            print("\nAttributeError >>> UserController.update: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'User not found.'
                }
                return jsonify(response), 404
            
            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400


    @staticmethod
    def delete(id):
        try:
            
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()

            return jsonify({}), 204
        
        except AttributeError as e:
            print("\nAttributeError >>> UserController.delete: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'User not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400
        
        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> UserController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'User not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> UserController.delete: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this User, remove them first.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400
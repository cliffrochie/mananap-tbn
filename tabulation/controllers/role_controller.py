from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError


class RoleController:
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

            roles = Role.query.all()
            result = []
            for role in roles:
                result.append(format_role(role))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> RoleController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }

            return jsonify(response), 400

    

    @staticmethod
    def find(id):
        try:
            role = Role.query.get(id)
            result = format_role(role)

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> RoleController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Role not found.'
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
            role = Role(data['name'], data['code'])
            db.session.add(role)
            db.session.commit()

            result = format_role(role)
            return jsonify(result), 201


        except TypeError as e:
            print("\nTypeError >>> RoleController.create: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> RoleController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Role you tried to create already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> RoleController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

        except InvalidRequestError as e:
            print("\nInvalidRequestError >>> RoleController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Duplicate entry, the Role you tried to create already exists.'
            }

            return jsonify(response), 400


    @staticmethod
    def update(id):
        try:
                
            data = request.get_json()
            role = Role.query.get(id)
            role.name = data['name']
            role.code = data['code']
            db.session.commit()

            result = format_role(role)

            return jsonify(result), 200

        except TypeError as e:
            print("\nTypeError >>> RoleController.update: "+ str(e) +"\n")

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
            print("\nKeyError >>> RoleController.update: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

        except AttributeError as e:
            print("\nAttributeError >>> RoleController.update: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Role not found.'
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
                
            role = Role.query.get(id)
            db.session.delete(role)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> RoleController.delete: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Role not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400
        
        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> RoleController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Role not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> RoleController.delete: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this Role, remove them first.'
                }

                return jsonify(response), 400
            
            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400
from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class ParticipantTypeController:
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
            
            participant_types = ParticipantType.query.all()

            result = []
            for participant_type in participant_types:
                result.append(format_participant_type(participant_type))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> ParticipantTypeController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }

            return jsonify(response), 400

    @staticmethod
    def find(id):
        try:
                
            participant_type = ParticipantType.query.get(id)
            result = format_participant_type(participant_type)

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantTypeController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'ParticipantType not found.'
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
            participant_type = ParticipantType(
                data['name'],
                data['description']
            )
            db.session.add(participant_type)
            db.session.commit()

            result = format_participant_type(participant_type)
            return jsonify(result), 201

        except TypeError as e:
            print("\nTypeError >>> ParticipantTypeController.create: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> ParticipantTypeController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the ParticipantType you tried to create already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> ParticipantTypeController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400


    @staticmethod
    def update(id):
        try:
                
            data = request.get_json()
            participant_type = ParticipantType.query.get(id)
            participant_type.name = data['name']
            participant_type.description = data['description']
            db.session.commit()

            result = format_participant_type(participant_type)
            return jsonify(result), 200

        except TypeError as e:
            print("\nTypeError >>> ParticipantTypeController.update: "+ str(e) +"\n")

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
            print("\nKeyError >>> ParticipantTypeController.update: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantTypeController.update: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'ParticipantType not found.'
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
                
            participant_type = ParticipantType.query.get(id)
            db.session.delete(participant_type)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantTypeController.delete: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'ParticipantType not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400
        
        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> ParticipantTypeController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'ParticipantType not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> ParticipantTypeController.delete: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this ParticipantType, remove them first.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400
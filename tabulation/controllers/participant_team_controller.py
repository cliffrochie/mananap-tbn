from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class ParticipantTeamController:
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

            participant_teams = ParticipantTeam.query.all()

            result = []
            for participant_team in participant_teams:
                result.append(format_participant_team(participant_team))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> ParticipantTeamController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }

            return jsonify(response), 400

    @staticmethod
    def find(id):
        try:

            participant_team = ParticipantTeam.query.get(id)
            result = format_participant_team(participant_team)

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantTeamController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'ParticipantTeam not found.'
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
            participant_team = ParticipantTeam(
                data['name'],
                data['description']
            )
            db.session.add(participant_team)
            db.session.commit()

            result = format_participant_team(participant_team)
            return jsonify(result), 201

        except TypeError as e:
            print("\nTypeError >>> ParticipantTeamController.create: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> ParticipantTeamController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the ParticipantTeam you tried to create already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> ParticipantTeamController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

    @staticmethod
    def update(id):
        try:
                
            data = request.get_json()
            participant_team = ParticipantTeam.query.get(id)
            participant_team.name = data['name']
            participant_team.description = data['description']
            db.session.commit()

            result = format_participant_team(participant_team)
            return jsonify(result), 200

        except TypeError as e:
            print("\nTypeError >>> ParticipantTeamController.update: "+ str(e) +"\n")

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
            print("\nKeyError >>> ParticipantTeamController.update: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantTeamController.update: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'ParticipantTeam not found.'
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
                
            participant_team = ParticipantTeam.query.get(id)
            db.session.delete(participant_team)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantTeamController.delete: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'ParticipantTeam not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400
        
        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> ParticipantTeamController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'ParticipantTeam not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> ParticipantTeamController.delete: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this ParticipantTeam, remove them first.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400
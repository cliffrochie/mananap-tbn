from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class ParticipantController:
    """
    +--------------------------------------------------------------------------
    | Method resource
    +--------------------------------------------------------------------------
    | All of the method resources are here.
    | Method lists:
    |       all()
    |       find(id)
    |       create()
    |       update(id)
    |       delete(id)
    |       add_event(id)
    |       delete_event(id, event_id)
    |
    """

    @staticmethod
    def all():
        try:

            participants = Participant.query.all()
            result = []
            for participant in participants:
                result.append(format_participant(participant))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> ParticipantController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }

            return jsonify(response), 400


    @staticmethod
    def find(id):
        try:
                
            participant = Participant.query.get(id)
            result = format_participant(participant)
            result['events'] = []
            for i in participant.event_participants:
                result['events'].append(format_event(i.event))

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute 'id'" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Participant not found.'
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

            participant = Participant(
                data['email'],
                data['firstname'],
                data['middlename'],
                data['lastname'],
                data['img_path'],
                data['participant_type_id'],
                data['participant_team_id'],
                data['organization_id']
            )

            db.session.add(participant)
            db.session.commit()

            result = format_participant(participant)

            return jsonify(result), 201

        except TypeError as e:
            print("\nTypeError >>> ParticipantController.create: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> ParticipantController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Participant you tried to create already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> ParticipantController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400
        

    @staticmethod
    def update(id):
        try:

            data = request.get_json()

            participant = Participant.query.get(id)
            participant.email = data['email']
            participant.firstname = data['firstname']
            participant.middlename = data['middlename']
            participant.lastname = data['lastname']
            participant.img_path = data['img_path']
            participant.is_active = data['is_active']
            participant.participant_type_id = data['participant_type_id']
            participant.participant_team_id = data['participant_team_id']
            participant.organization_id = data['organization_id']
            db.session.commit()

            result = format_participant(participant)
            result['events'] = []
            for i in participant.event_participants:
                result['events'].append(format_event(i.event))

            return jsonify(result), 200

        except TypeError as e:
            print("\nTypeError >>> ParticipantController.update: "+ str(e) +"\n")

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
            print("\nKeyError >>> ParticipantController.update: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }

            return jsonify(response), 400

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantController.update: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Participant not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> ParticipantController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Participant you tried to create already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400


    @staticmethod
    def delete(id):
        try:
    
            event_participant = EventParticipant.__table__.delete().where(
                EventParticipant.participant_id == id
            )

            participant = Participant.query.get(id)
            db.session.delete(participant)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantController.delete: "+ str(e) +"\n")

            if "'NoneType' object has no attribute 'id'" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Participant not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> ParticipantController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Participant not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> ParticipantController.delete: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this Participant, remove them first.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

    """ Non-resource - Added methods """

    @staticmethod
    def add_event(id):
        try:
                
            data = request.get_json()
            event_participant = EventParticipant(
                data['event_id'],
                id
            )
            db.session.add(event_participant)
            db.session.commit()

            participant = Participant.query.get(id)
            result = format_participant(participant)
            result['events'] = []
            for i in participant.event_participants:
                result['events'].append(format_event(i.event))

            return jsonify(result), 200

        except TypeError as e:
            print("\nTypeError >>> ParticipantController.add_event: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> ParticipantController.add_event: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Event you tried to insert already exists.'
                }

                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> ParticipantController.add_event: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400

    @staticmethod
    def delete_event(id, event_id):
        try:
                
            event_participant = EventParticipant.query.filter(db.and_(
                EventParticipant.event_id == event_id,
                EventParticipant.participant_id == id
            ))
            db.session.delete(event_participant)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> ParticipantController.delete_event: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Event not found'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> ParticipantController.delete_event: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Event not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> ParticipantController.delete_event: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this Event, remove them first.'
                }
                return jsonify(response), 400
            
            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400



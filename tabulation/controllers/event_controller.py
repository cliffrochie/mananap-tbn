from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

import json


class EventController:
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
    |       delete_multiple(ids)
    |       get_unassigned_judges(id)
    |       find_judge(id, judge_id)
    |       add_judge(id)
    |       delete_judge(id, judge_id)
    |       get_unassigned_participants(id)
    |       add_participant(id)
    |       delete_participant(id, participant_id)
    |       all_criterias(id)
    |       find_criteria(id, criteria_id)
    |       add_criteria(id)
    |       update_criteria(id, criteria_id)
    |       delete_criteria(id, criteria_id)
    |
    """

    @staticmethod
    def all():
        try:

            events = Event.query.all()
            result = []
            for event in events:
                result.append(format_event(event))

            return jsonify(result), 200
        
        except Exception as e:
            print("\nException >>> EventController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }
            return jsonify(response), 400


    @staticmethod
    def find(id):
        try:

            event = Event.query.get(id)
            result = format_event(event)
            result['judges'] = []
            result['participants'] = []
            result['criterias'] = []

            for i in event.event_judges:
                judge = format_judge(i.judge)
                result['judges'].append(judge)

            for i in event.event_participants:
                data = {}
                data = format_participant(i.participant)
                data['participant_no'] = i.participant_no
                result['participants'].append(data)

            for criteria in event.criterias:
                result['criterias'].append(format_criteria(criteria))

            organization = Organization.query.get(event.organization_id)
            result['organization'] = organization.name

            event_type = EventType.query.get(event.event_type_id)
            result['event_type'] = event_type.name

            return jsonify(result), 200
            
        except AttributeError as e:
            print("\nAttributeError >>> EventController.find: "+ str(e) +"\n")

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
       

    @staticmethod
    def create():
        try:

            data = request.get_json()

            event = Event(
                data['name'],
                data['description'],
                data['img_path'],
                data['event_type_id'],
                data['organization_id']            
            )

            db.session.add(event)
            db.session.commit()

            result = format_event(event)

            return jsonify(result), 201
        
        except TypeError as e:
            print("\nTypeError >>> EventController.create: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> EventController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Event you tried to create already exists.'
                }
                return jsonify(response), 400
            
            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> EventController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400


    @staticmethod
    def update(id):
        try:

            data = request.get_json()
            event = Event.query.get(id)
            event.name = data['name']
            event.description = data['description']
            event.img_path = data['img_path']
            event.is_active = data['is_active']
            event.event_type_id = data['event_type_id']
            event.organization_id = data['organization_id']
            db.session.commit()

            result = format_event(event)
            
            organization = Organization.query.get(event.organization_id)
            result['organization'] = organization.name

            event_type = EventType.query.get(event.event_type_id)
            result['event_type'] = event_type.name
            
            return jsonify(result), 200
        
        except TypeError as e:
            print("\nTypeError >>> EventController.update: "+ str(e) +"\n")

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
            print("\nKeyError >>> EventController.update: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400

        except AttributeError as e:
            print("\nAttributeError >>> EventController.update: "+ str(e) +"\n")

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


    @staticmethod
    def delete(id):
        try:
            
            event_judge = EventJudge.__table__.delete().where(
                EventJudge.event_id == id
            )
            db.session.execute(event_judge)

            event_participant = EventParticipant.__table__.delete().where(
                EventParticipant.event_id == id
            )
            db.session.execute(event_participant)

            event = Event.query.get(id)
            db.session.delete(event)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> EventController.delete: "+ str(e) +"\n")

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
            print("\nUnmappedInstanceError >>> EventController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Event not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> EventController.delete: "+ str(e) +"\n")

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


    @staticmethod
    def delete_multiple():
        try:

            events = request.get_json()
            result = []
            for item in events:
                data = {}
                event = Event.query.get(item['id'])
                data['id'] = event.id
                data['name'] = event.name
                response = EventController.delete(event.id)
                data['response'] = response[1]
                result.append(data)

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> EventController.delete_multiple: "+ str(e) +"\n")

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
            print("\nUnmappedInstanceError >>> EventController.delete_multiple: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Event not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> EventController.delete_multiple: "+ str(e) +"\n")

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


    """
    +--------------------------------------------------------------------------
    | Added methods: Judge
    +--------------------------------------------------------------------------
    | All of the methods here are related to events handling judges
    |
    """
    @staticmethod
    def get_unassigned_judges(id):
        try:
            event = Event.query.get(id)

            users = User.query.join(Judge).outerjoin(EventJudge).filter(
                EventJudge.event_id == event.id).all()

            exclude_users = []
            for user in users:
                exclude_users.append(user.judges.first().id)


            unassigned_judges = Judge.query.join(User).filter(
                ~Judge.id.in_(exclude_users)).order_by(User.lastname)


            print("???? ", unassigned_judges)

            result = []

            for uj in unassigned_judges:
                result.append(format_judge(uj))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> EventController.get_unassigned_judges: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }
            return jsonify(response), 400


    @staticmethod
    def find_judge(id, judge_id):
        try:
                
            judge = Judge.query.get(judge_id)
            result = format_judge(judge)
            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> EventController.find_criteria: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Event or Criteria not found'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400


    @staticmethod
    def add_judge(id):
        try:

            data = request.get_json()
            event_judge = EventJudge(
                id,
                data['judge_id']
            )
            db.session.add(event_judge)
            db.session.commit()

            judge = Judge.query.get(data['judge_id'])
            result = format_judge(judge)

            return jsonify(result), 201

        except AttributeError as e:
            print("\nAttributeError >>> EventController.add_judge: "+ str(e) +"\n")

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

        except TypeError as e:
            print("\nTypeError >>> EventController.add_judge: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> EventController.add_judge: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Judge you tried to insert already exists.'
                }
                return jsonify(response), 400

            if "1452" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Judge not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> EventController.add_judge: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400

    
    @staticmethod
    def delete_judge(id, judge_id):
        try:
                
            event_judge = EventJudge.query.filter(db.and_(
                EventJudge.event_id == id, 
                EventJudge.judge_id == judge_id
            )).one_or_none()
            db.session.delete(event_judge)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> EventController.delete_judge: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Event or Judge not found'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> EventController.delete_judge: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Event or Judge not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> EventController.delete_judge: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this Judge, remove them first.'
                }
                return jsonify(response), 400
            
            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400
    
    """
    +--------------------------------------------------------------------------
    | Added methods: Participant
    +--------------------------------------------------------------------------
    | All of the methods here are related to events handling participants
    |
    """
    @staticmethod
    def get_unassigned_participants(id):
        try:
            event = Event.query.get(id)

            participants = Participant.query.join(
                EventParticipant
            ).filter(EventParticipant.event_id == event.id).all()

            exclude_participants = []
            for participant in participants:
                exclude_participants.append(participant.id)

            unassigned_participants = Participant.query.filter(
                ~Participant.id.in_(exclude_participants)).order_by(Participant.lastname)

            result = []
            for up in unassigned_participants:
                result.append(format_participant(up))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> EventController.get_unassigned_participants: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }
            return jsonify(response), 400


    @staticmethod
    def add_participant(id):
        try:
            data = request.get_json()
            event_participant = EventParticipant(
                id,
                data['id'],
                data['participant_no']
            )
            db.session.add(event_participant)
            db.session.commit()

            participant = Participant.query.get(data['id'])
            result = format_participant(participant)
            result['participant_no'] = event_participant.participant_no

            return jsonify(result), 201

        except AttributeError as e:
            print("\nAttributeError >>> EventController.add_participant: "+ str(e) +"\n")

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

        except TypeError as e:
            print("\nTypeError >>> EventController.add_participant: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> EventController.add_participant: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Participant you tried to create already exists.'
                }
                return jsonify(response), 400
            

            if "1452" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Participant not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> EventController.add_participant: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400


    @staticmethod
    def delete_participant(id, participant_id):
        try:
                
            event_participant = EventParticipant.query.filter(db.and_(
                EventParticipant.event_id == id,
                EventParticipant.participant_id == participant_id
            )).one_or_none()
            db.session.delete(event_participant)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> EventController.delete_participant: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Event or Participant not found'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(), 400

        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> EventController.delete_participant: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Event or Participant not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> EventController.delete_participant: "+ str(e) +"\n")

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





from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class EventTypeController:
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
                
            event_types = EventType.query.all()
            result = []
            for event_type in event_types:
                result.append(format_event_type(event_type))

            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> EventTypeController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }
            return jsonify(response), 400

    @staticmethod
    def find(id):
        try:
                
            event_type = EventType.query.get(id)
            result = format_event_type(event_type)
            result['events'] = []

            for event in event_type.events:
                result['events'].append(format_event(event))

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> EventTypeController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'EventType not found.'
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
            event_type = EventType(data['name'], data['description'])
            db.session.add(event_type)
            db.session.commit()

            result = format_event_type(event_type)

            return jsonify(result), 201

        except TypeError as e:
            print("\nTypeError >>> EventTypeController.create: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> EventTypeController.create: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the EventType you tried to create already exists.'
                }
                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> EventTypeController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400

    @staticmethod
    def update(id):
        try:
                
            data = request.get_json()

            event_type = EventType.query.get(id)
            event_type.name = data['name']
            event_type.description = data['description']
            db.session.commit()

            result = format_event_type(event_type)

            return jsonify(result), 200

        except TypeError as e:
            print("\nTypeError >>> EventTypeController.update: "+ str(e) +"\n")

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
            print("\nKeyError >>> EventTypeController.update: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400

        except AttributeError as e:
            print("\nAttributeError >>> EventTypeController.update: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'EventType not found.'
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

            event_type = EventType.query.get(id)
            db.session.delete(event_type)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> EventController.delete: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'EventType not found'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> EventTypeController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'EventType not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> EventTypeController.delete: "+ str(e) +"\n")

            if "foreign key constraint fails" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some other data is dependent to this EventType, remove them first.'
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
            
            event_types = request.get_json()
            result = []
            for item in event_types:
                data = {}
                event_type = EventType.query.get(item['id'])
                data['id'] = event_type.id
                data['name'] = event_type.name
                data['description'] = event_type.description
                response = EventTypeController.delete(event_type.id)
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
from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class CriteriaController:
    """ Route resources """
    
    @staticmethod
    def all():
        try:
                
            criterias = Criteria.query.filter(Criteria.event_id == id).all()
            result = []
            for criteria in criterias:
                result.append(format_criteria(criteria))

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> EventController.all_criterias: "+ str(e) +"\n")

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
    def find(event_id, criteria_id):
        try:
                
            criteria = Criteria.query.filter(db.and_(
                Criteria.id == criteria_id,
                Criteria.event_id == event_id
            )).first()

            result = format_criteria(criteria)

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
    def create(event_id):
        try:
                
            data = request.get_json()

            criteria = Criteria(
                data['name'],
                data['max_points'],
                event_id
            )
            db.session.add(criteria)
            db.session.commit()

            result = format_criteria(criteria)

            return jsonify(result), 201

        except AttributeError as e:
            print("\nAttributeError >>> EventController.add_criteria: "+ str(e) +"\n")

            if "'NoneType' object has no attribute 'id'" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Event not found.'
                }
                return jsonify(response), 404

            if "'NoneType' object has no attribute 'name'" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Some of the key attributes submitted are missing or mispelled..'
                }
                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

        except TypeError as e:
            print("\nTypeError >>> EventController.add_criteria: "+ str(e) +"\n")

            if "'NoneType' object is not subscriptable" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Failed to submit. Either empty payload or wrong event id.'
                }
                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Type error'
            }
            return jsonify(response), 400

        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> EventController.add_criteria: "+ str(e) +"\n")

            if "Duplicate entry" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the Criteria you tried to create already exists.'
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
            print("\nKeyError >>> EventController.add_criteria: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400

    @staticmethod
    def update(event_id, criteria_id):
        try:
            data = request.get_json()

            criteria = Criteria.query.filter(db.and_(
                Criteria.id == criteria_id,
                Criteria.event_id == event_id
            )).first()

            criteria.name = data['name']
            criteria.max_points = data['max_points']
            db.session.commit()

            result = format_criteria(criteria)
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
                    'message': 'Submitted without data.'
                }
                return jsonify(response), 400

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

    @staticmethod
    def delete(event_id, criteria_id):
        try:
            criteria = Criteria.query.filter(db.and_(
                Criteria.id == criteria_id,
                Criteria.event_id == event_id
            )).first() 
            db.session.delete(criteria)
            db.session.commit()

            return jsonify({}), 204      

        except AttributeError as e:
            print("\nAttributeError >>> EventController.delete_criteria: "+ str(e) +"\n")

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
            print("\nUnmappedInstanceError >>> EventController.delete_criteria: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Event not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> EventController.delete_criteria: "+ str(e) +"\n")

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
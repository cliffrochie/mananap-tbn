from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class JudgeController:
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

            judges = Judge.query.all()
            result = []
            for judge in judges:
                result.append(format_judge(judge))
                
            return jsonify(result), 200

        except Exception as e:
            print("\nException >>> JudgeController.all: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Oops! Something went wrong!'
            }
            return jsonify(response), 400


    @staticmethod
    def find(id):
        try:

            judge = Judge.query.get(id)
            result = format_judge(judge)
            result['events'] = []
            for i in judge.event_judges:
                result['events'].append(format_event(i.event))

            return jsonify(result), 200

        except AttributeError as e:
            print("\nAttributeError >>> JudgeController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Judge not found.'
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

            judge = Judge(data['user_id'])
            db.session.add(judge)
            db.session.commit()

            result = format_judge(judge)
            result['events'] = []

            return jsonify(result), 201

        except TypeError as e:
            print("\nTypeError >>> JudgeController.create: "+ str(e) +"\n")

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
            print("\nIntegrityError >>> JudgeController.create: "+ str(e) +"\n")

            if "1062" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Duplicate entry, the user you tried to add as Judge already exists.'
                }
                return jsonify(response), 400

            if "1452" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'User not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Integrity error'
            }
            return jsonify(response), 400

        except KeyError as e:
            print("\nKeyError >>> JudgeController.create: "+ str(e) +"\n")

            response = {
                'status': 'failed',
                'message': 'Some of the key attributes submitted are missing or mispelled.'
            }
            return jsonify(response), 400


    @staticmethod
    def delete(id):
        try:
            
            event_judge = EventJudge.__table__.delete().where(
                EventJudge.judge_id == id
            )
            db.session.execute(event_judge)

            judge = Judge.query.get(id)
            db.session.delete(judge)
            db.session.commit()

            return jsonify({}), 204

        except AttributeError as e:
            print("\nAttributeError >>> JudgeController.find: "+ str(e) +"\n")

            if "'NoneType' object has no attribute" in str(e):
                response = {
                    'status': 'failed',
                    'message': 'Judge not found.'
                }
                return jsonify(response), 404

            response = {
                'status': 'failed', 
                'message': 'Attribute error'
            }
            return jsonify(response), 400

        except UnmappedInstanceError as e:
            print("\nUnmappedInstanceError >>> JudgeController.delete: "+ str(e) +"\n")
            response = {
                'status': 'failed',
                'message': 'Judge not found.'
            }
            return jsonify(response), 404
        
        except IntegrityError as e:
            db.session.rollback()
            print("\nIntegrityError >>> JudgeController.delete: "+ str(e) +"\n")

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
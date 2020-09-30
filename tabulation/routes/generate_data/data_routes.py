# Main packages
from flask import Flask, Blueprint, request, jsonify
from tabulation.utils.sample_data import fake_data
from tabulation.models.db import *
from sqlalchemy.exc import IntegrityError



data = Blueprint('data', __name__)

@data.route('/generate-all', methods=['GET'])
def generate():
    fake_data.generate_organization_type()
    fake_data.generate_organization()
    fake_data.generate_roles()
    fake_data.generate_users()
    fake_data.generate_event_type()
    fake_data.generate_events()
    fake_data.generate_participant_type()
    fake_data.generate_participant_team()
    fake_data.generate_participants()
    fake_data.generate_judges()

    return jsonify({'message': 'Generate data success!'})


@data.route('/remove-all', methods=['GET'])
def remove_all():
    try:
        EventJudge.query.delete()
        Judge.query.delete()
        User.query.delete()
        Role.query.delete()

        EventScore.query.delete()
        Criteria.query.delete()
        EventParticipant.query.delete()
        Event.query.delete()
        EventType.query.delete()

        Participant.query.delete()
        ParticipantType.query.delete()
        ParticipantTeam.query.delete()

        Organization.query.delete()
        OrganizationType.query.delete()


        db.session.commit()
    
    except IntegrityError as e:
        print("IntegrityError >>>>>>>>>> remove_all: "+ str(e))
        if "1451, 'Cannot delete or update a parent row" in str(e):
            response = {
                'status': 'failed', 
                'message': 'Some of the data is dependent to other data. Remove them first!'
            }
            return jsonify(response), 400

        response = {
            'status': 'failed', 
            'message': 'There is something wrong with the action you have taken!'
        }
        return jsonify(response), 400

    return jsonify({'status':'success', 'message': 'All data removed successfully!'})


from flask import Blueprint, jsonify
from tabulation.controllers.user_controller import UserController
from tabulation.controllers.event_controller import EventController
from tabulation.controllers.criteria_controller import CriteriaController
from tabulation.controllers.judge_controller import JudgeController
from tabulation.controllers.participant_controller import ParticipantController
from tabulation.controllers.role_controller import RoleController
from tabulation.controllers.organization_controller import OrganizationController
from tabulation.controllers.organization_type_controller import OrganizationTypeController
from tabulation.controllers.event_type_controller import EventTypeController
from tabulation.controllers.participant_team_controller import ParticipantTeamController
from tabulation.controllers.participant_type_controller import ParticipantTypeController
from tabulation.controllers.event_score_controller import EventScoreController

from tabulation.models.db import *
from tabulation.utils.functions.access_restriction import *

main = Blueprint('main', __name__)

@main.route('/ping', methods=['GET'])
def ping():
    return jsonify({})

"""
+--------------------------------------------------------------------------
| User routes
+--------------------------------------------------------------------------
| Below are the routes related to users.
|
"""
# Get routes
@main.route('/users', methods=['GET'])
@token_required(allowed_guest=False)
def get_users(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return UserController.all()

@main.route('/users/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_user(current_user, id):
    
    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return UserController.find(id)

# Post routes
@main.route('/users', methods=['POST'])
@token_required(allowed_guest=False)
def create_user(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return UserController.create()

# Put routes
@main.route('/users/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_user(current_user, id):
    
    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return UserController.update(id)

# Delete routes
@main.route('/users/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_user(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return UserController.delete(id)



"""
+--------------------------------------------------------------------------
| Event routes
+--------------------------------------------------------------------------
| Below are the routes related to events.
|
"""

# Get routes
@main.route('/events', methods=['GET'])
@token_required(allowed_guest=True)
def get_events(current_user):
    return EventController.all()

@main.route('/events/<id>', methods=['GET'])
@token_required(allowed_guest=True)
def get_event(current_user, id):
    return EventController.find(id)

@main.route('/events/<id>/unassigned-judges', methods=['GET'])
@token_required(allowed_guest=True)
def get_unassigned_judges_from_event(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.get_unassigned_judges(id)

@main.route('/events/<id>/find-judge/<judge_id>', methods=['GET'])
@token_required(allowed_guest=True)
def get_judge_from_event(current_user, id, judge_id):
    return EventController.find_judge(id, judge_id)

@main.route('/events/<id>/unassigned-participants', methods=['GET'])
@token_required(allowed_guest=True)
def get_unassigned_participants_from_event(current_user, id):
    return EventController.get_unassigned_participants(id)

# Post routes
@main.route('/events', methods=['POST'])
@token_required(allowed_guest=False)
def create_event(current_user):
    
    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.create()

@main.route('/events/<id>/add-judge', methods=['POST'])
@token_required(allowed_guest=False)
def add_judge_from_event(current_user, id):
    
    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.add_judge(id)

@main.route('/events/<id>/add-participant', methods=['POST'])
@token_required(allowed_guest=False)
def add_participant_from_event(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401
        
    return EventController.add_participant(id)

@main.route('/events/delete', methods=['POST'])
@token_required(allowed_guest=False)
def delete_multiple_events(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.delete_multiple()


# Put routes
@main.route('/events/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_event(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.update(id)

# Delete routes
@main.route('/events/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_event(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.delete(id)

@main.route('/events/<id>/delete-judge/<judge_id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_judge_from_event(current_user, id, judge_id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.delete_judge(id, judge_id)

@main.route('/events/<id>/delete-participant/<participant_id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_participant_from_event(current_user, id, participant_id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventController.delete_participant(id, participant_id)



"""
+--------------------------------------------------------------------------
| Event Criteria routes
+--------------------------------------------------------------------------
| Below are the routes related to criterias.
|
"""
# Get routes
@main.route('/events/<event_id>/criterias', methods=['GET'])
@token_required(allowed_guest=True)
def get_criterias(current_user, event_id):
    return CriteriaController.all(event_id)

@main.route('/events/<event_id>/criterias/<criteria_id>', methods=['GET'])
@token_required(allowed_guest=True)
def get_criteria(current_user, event_id, criteria_id):
    return CriteriaController.find(event_id, criteria_id)

# Post routes
@main.route('/events/<event_id>/criterias', methods=['POST'])
@token_required(allowed_guest=False)
def create_criteria(current_user, event_id):
    return CriteriaController.create(event_id)

# Put routes
@main.route('/events/<event_id>/criterias/<criteria_id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_criteria(current_user, event_id, criteria_id):
    return CriteriaController.update(event_id, criteria_id)

# Delete routes
@main.route('/events/<event_id>/criterias/<criteria_id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_criteria(current_user, event_id, criteria_id):
    return CriteriaController.delete(event_id, criteria_id)



"""
+--------------------------------------------------------------------------
| Judge routes
+--------------------------------------------------------------------------
| Below are the routes related to judges.
|
"""
# Get routes
@main.route('/judges', methods=['GET'])
@token_required(allowed_guest=True)
def get_judges(current_user):
    return JudgeController.all()

@main.route('/judges/<id>', methods=['GET'])
@token_required(allowed_guest=True)
def get_judge(current_user, id):
    return JudgeController.find(id)

# Post routes
@main.route('/judges', methods=['POST'])
@token_required(allowed_guest=False)
def create_judge(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return JudgeController.create()

# Delete routes
@main.route('/judges/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_judge(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return JudgeController.delete(id)



"""
+--------------------------------------------------------------------------
| Participant routes
+--------------------------------------------------------------------------
| Below are the routes related to participants.
|
"""
# Get routes
@main.route('/participants', methods=['GET'])
@token_required(allowed_guest=True)
def get_participants(current_user):
    return ParticipantController.all()

@main.route('/participants/<id>', methods=['GET'])
@token_required(allowed_guest=True)
def get_participant(current_user, id):
    return ParticipantController.find(id)

# Post routes
@main.route('/participants', methods=['POST'])
@token_required(allowed_guest=False)
def create_participant(current_user):
    return ParticipantController.create()

# Put routes
@main.route('/participants/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_participant(current_user, id):
    return ParticipantController.update(id)

# Delete routes
@main.route('/participants/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_participant(current_user, id):
    return ParticipantController.delete(id)



"""
+--------------------------------------------------------------------------
| Role routes
+--------------------------------------------------------------------------
| Below are the routes related to roles.
|
"""
# Get routes
@main.route('/roles', methods=['GET'])
@token_required(allowed_guest=False)
def get_roles(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return RoleController.all()

@main.route('/roles/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_role(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return RoleController.find(id)

# Post routes
@main.route('/roles', methods=['POST'])
@token_required(allowed_guest=False)
def create_role(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return RoleController.create()

# Put routes
@main.route('/roles/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_role(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return RoleController.update(id)

# Delete routes
@main.route('/roles/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_role(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return RoleController.delete(id)



"""
+--------------------------------------------------------------------------
| Organization routes
+--------------------------------------------------------------------------
| Below are the routes related to organizations.
|
"""
# Get routes
@main.route('/organizations', methods=['GET'])
@token_required(allowed_guest=False)
def get_organizations(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationController.all()

@main.route('/organizations/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_organization(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationController.find(id)

# Post routes
@main.route('/organizations', methods=['POST'])
@token_required(allowed_guest=False)
def create_organization(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationController.create()

# Put routes
@main.route('/organizations/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_organization(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationController.update(id)

# Delete routes
@main.route('/organizations/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_organization(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationController.delete(id)



"""
+--------------------------------------------------------------------------
| OrganizationType routes
+--------------------------------------------------------------------------
| Below are the routes related to organization types.
|
"""
# Get routes
@main.route('/organization-types', methods=['GET'])
@token_required(allowed_guest=False)
def get_organization_types(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationTypeController.all()

@main.route('/organization-types/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_organization_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationTypeController.find(id)

# Post routes
@main.route('/organization-types', methods=['POST'])
@token_required(allowed_guest=False)
def create_organization_type(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationTypeController.create()

# Put routes
@main.route('/organization-types/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_organization_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationTypeController.update(id)

# Delete routes
@main.route('/organization-types/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_organization_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return OrganizationTypeController.delete(id)



"""
+--------------------------------------------------------------------------
| EventType routes
+--------------------------------------------------------------------------
| Below are the routes related to event types.
|
"""
# Get routes
@main.route('/event-types', methods=['GET'])
@token_required(allowed_guest=False)
def get_event_types(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventTypeController.all()

@main.route('/event-types/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_event_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventTypeController.find(id)

# Post routes
@main.route('/event-types', methods=['POST'])
@token_required(allowed_guest=False)
def create_event_type(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventTypeController.create()

@main.route('/event-types/delete', methods=['POST'])
@token_required(allowed_guest=False)
def delete_multiple_event_types(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventTypeController.delete_multiple()

# Put routes
@main.route('/event-types/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_event_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventTypeController.update(id)

# Delete routes
@main.route('/event-types/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_event_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return EventTypeController.delete(id)



"""
+--------------------------------------------------------------------------
| ParticipantTeam routes
+--------------------------------------------------------------------------
| Below are the routes related to participant teams.
|
"""
# Get routes
@main.route('/participant-teams', methods=['GET'])
@token_required(allowed_guest=False)
def get_participant_teams(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTeamController.all()

@main.route('/participant-teams/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_participant_team(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTeamController.find(id)

# Post routes
@main.route('/participant-teams', methods=['POST'])
@token_required(allowed_guest=False)
def create_participant_team(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTeamController.create()

# Put routes
@main.route('/participant-teams/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_participant_team(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTeamController.update(id)

# Delete routes
@main.route('/participant-teams/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_participant_team(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTeamController.delete(id)



"""
+--------------------------------------------------------------------------
| ParticipantType routes
+--------------------------------------------------------------------------
| Below are the routes related to participant types.
|
"""
# Get routes
@main.route('/participant-types', methods=['GET'])
@token_required(allowed_guest=False)
def get_participant_types(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTypeController.all()

@main.route('/participant-types/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_participant_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTypeController.find(id)

# Post routes
@main.route('/participant-types', methods=['POST'])
@token_required(allowed_guest=False)
def create_participant_type(current_user):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTypeController.create()

# Put routes
@main.route('/participant-types/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_participant_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTypeController.update(id)

# Delete routes
@main.route('/participant-types/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_participant_type(current_user, id):

    if is_admin(current_user):
        return jsonify(unauthorized_access()), 401

    return ParticipantTypeController.delete(id)



"""
+--------------------------------------------------------------------------
| EventScore routes
+--------------------------------------------------------------------------
| Below are the routes related to event scores.
|
"""
# Get routes
@main.route('/event-scores', methods=['GET'])
@token_required(allowed_guest=False)
def get_event_scores(current_user):

    if is_judge(current_user):
        return jsonify(unauthorized_access()), 401

    return EventScoreController.all()

@main.route('/event-scores/<id>', methods=['GET'])
@token_required(allowed_guest=False)
def get_event_score(current_user, id):

    if is_judge(current_user):
        return jsonify(unauthorized_access()), 401

    return EventScoreController.find(id)

# Post routes
@main.route('/event-scores', methods=['POST'])
@token_required(allowed_guest=False)
def create_event_score(current_user):

    if is_judge(current_user):
        return jsonify(unauthorized_access()), 401

    return EventScoreController.create()

# Put routes
@main.route('/event-scores/<id>', methods=['PUT'])
@token_required(allowed_guest=False)
def update_event_score(current_user, id):

    if is_judge(current_user):
        return jsonify(unauthorized_access()), 401

    return EventScoreController.update(id)

# Delete routes
@main.route('/event-scores/<id>', methods=['DELETE'])
@token_required(allowed_guest=False)
def delete_event_score(current_user, id):

    if is_judge(current_user):
        return jsonify(unauthorized_access()), 401

    return EventScoreController.delete(id)
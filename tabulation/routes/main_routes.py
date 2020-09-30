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
def get_users():
    return UserController.all()

@main.route('/users/<id>', methods=['GET'])
def get_user(id):
    return UserController.find(id)

# Post routes
@main.route('/users', methods=['POST'])
def create_user():
    return UserController.create()

# Put routes
@main.route('/users/<id>', methods=['PUT'])
def update_user(id):
    return UserController.update(id)

# Delete routes
@main.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
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
def get_events():
    return EventController.all()

@main.route('/events/<id>', methods=['GET'])
def get_event(id):
    return EventController.find(id)

@main.route('/events/<id>/unassigned-judges', methods=['GET'])
def get_unassigned_judges_from_event(id):
    return EventController.get_unassigned_judges(id)

@main.route('/events/<id>/find-judge/<judge_id>', methods=['GET'])
def get_judge_from_event(id, judge_id):
    return EventController.find_judge(id, judge_id)

@main.route('/events/<id>/unassigned-participants', methods=['GET'])
def get_unassigned_participants_from_event(id):
    return EventController.get_unassigned_participants(id)

# Post routes
@main.route('/events', methods=['POST'])
def create_event():
    return EventController.create()

@main.route('/events/<id>/add-judge', methods=['POST'])
def add_judge_from_event(id):
    return EventController.add_judge(id)

@main.route('/events/<id>/add-participant', methods=['POST'])
def add_participant_from_event(id):
    return EventController.add_participant(id)

@main.route('/events/delete', methods=['POST'])
def delete_multiple_events():
    return EventController.delete_multiple()


# Put routes
@main.route('/events/<id>', methods=['PUT'])
def update_event(id):
    return EventController.update(id)

# Delete routes
@main.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    return EventController.delete(id)

@main.route('/events/<id>/delete-judge/<judge_id>', methods=['DELETE'])
def delete_judge_from_event(id, judge_id):
    return EventController.delete_judge(id, judge_id)

@main.route('/events/<id>/delete-participant/<participant_id>', methods=['DELETE'])
def delete_participant_from_event(id, participant_id):
    return EventController.delete_participant(id, participant_id)



"""
+--------------------------------------------------------------------------
| Criteria routes
+--------------------------------------------------------------------------
| Below are the routes related to criterias.
|
"""
# Get routes
@main.route('/events/<event_id>/criterias', methods=['GET'])
def get_criterias(event_id):
    return CriteriaController.all(event_id)

@main.route('/events/<event_id>/criterias/<criteria_id>', methods=['GET'])
def get_criteria(event_id, criteria_id):
    return CriteriaController.find(event_id, criteria_id)

# Post routes
@main.route('/events/<event_id>/criterias', methods=['POST'])
def create_criteria(event_id):
    return CriteriaController.create(event_id)

# Put routes
@main.route('/events/<event_id>/criterias/<criteria_id>', methods=['PUT'])
def update_criteria(event_id, criteria_id):
    return CriteriaController.update(event_id, criteria_id)

# Delete routes
@main.route('/events/<event_id>/criterias/<criteria_id>', methods=['DELETE'])
def delete_criteria(event_id, criteria_id):
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
def get_judges():
    return JudgeController.all()

@main.route('/judges/<id>', methods=['GET'])
def get_judge(id):
    return JudgeController.find(id)

# Post routes
@main.route('/judges', methods=['POST'])
def create_judge():
    return JudgeController.create()

# Delete routes
@main.route('/judges/<id>', methods=['DELETE'])
def delete_judge(id):
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
def get_participants():
    return ParticipantController.all()

@main.route('/participants/<id>', methods=['GET'])
def get_participant(id):
    return ParticipantController.find(id)

# Post routes
@main.route('/participants', methods=['POST'])
def create_participant():
    return ParticipantController.create()

# Put routes
@main.route('/participants/<id>', methods=['PUT'])
def update_participant(id):
    return ParticipantController.update(id)

# Delete routes
@main.route('/participants/<id>', methods=['DELETE'])
def delete_participant(id):
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
def get_roles():
    return RoleController.all()

@main.route('/roles/<id>', methods=['GET'])
def get_role(id):
    return RoleController.find(id)

# Post routes
@main.route('/roles', methods=['POST'])
def create_role():
    return RoleController.create()

# Put routes
@main.route('/roles/<id>', methods=['PUT'])
def update_role(id):
    return RoleController.update(id)

# Delete routes
@main.route('/roles/<id>', methods=['DELETE'])
def delete_role(id):
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
def get_organizations():
    return OrganizationController.all()

@main.route('/organizations/<id>', methods=['GET'])
def get_organization(id):
    return OrganizationController.find(id)

# Post routes
@main.route('/organizations', methods=['POST'])
def create_organization():
    return OrganizationController.create()

# Put routes
@main.route('/organizations/<id>', methods=['PUT'])
def update_organization(id):
    return OrganizationController.update(id)

# Delete routes
@main.route('/organizations/<id>', methods=['DELETE'])
def delete_organization(id):
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
def get_organization_types():
    return OrganizationTypeController.all()

@main.route('/organization-types/<id>', methods=['GET'])
def get_organization_type(id):
    return OrganizationTypeController.find(id)

# Post routes
@main.route('/organization-types', methods=['POST'])
def create_organization_type():
    return OrganizationTypeController.create()

# Put routes
@main.route('/organization-types/<id>', methods=['PUT'])
def update_organization_type(id):
    return OrganizationTypeController.update(id)

# Delete routes
@main.route('/organization-types/<id>', methods=['DELETE'])
def delete_organization_type(id):
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
def get_event_types():
    return EventTypeController.all()

@main.route('/event-types/<id>', methods=['GET'])
def get_event_type(id):
    return EventTypeController.find(id)

# Post routes
@main.route('/event-types', methods=['POST'])
def create_event_type():
    return EventTypeController.create()

@main.route('/event-types/delete', methods=['POST'])
def delete_multiple_event_types():
    return EventTypeController.delete_multiple()

# Put routes
@main.route('/event-types/<id>', methods=['PUT'])
def update_event_type(id):
    return EventTypeController.update(id)

# Delete routes
@main.route('/event-types/<id>', methods=['DELETE'])
def delete_event_type(id):
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
def get_participant_teams():
    return ParticipantTeamController.all()

@main.route('/participant-teams/<id>', methods=['GET'])
def get_participant_team(id):
    return ParticipantTeamController.find(id)

# Post routes
@main.route('/participant-teams', methods=['POST'])
def create_participant_team():
    return ParticipantTeamController.create()

# Put routes
@main.route('/participant-teams/<id>', methods=['PUT'])
def update_participant_team(id):
    return ParticipantTeamController.update(id)

# Delete routes
@main.route('/participant-teams/<id>', methods=['DELETE'])
def delete_participant_team(id):
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
def get_participant_types():
    return ParticipantTypeController.all()

@main.route('/participant-types/<id>', methods=['GET'])
def get_participant_type(id):
    return ParticipantTypeController.find(id)

# Post routes
@main.route('/participant-types', methods=['POST'])
def create_participant_type():
    return ParticipantTypeController.create()

# Put routes
@main.route('/participant-types/<id>', methods=['PUT'])
def update_participant_type(id):
    return ParticipantTypeController.update(id)

# Delete routes
@main.route('/participant-types/<id>', methods=['DELETE'])
def delete_participant_type(id):
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
def get_event_scores():
    return EventScoreController.all()

@main.route('/event-scores/<id>', methods=['GET'])
def get_event_score(id):
    return EventScoreController.find(id)

# Post routes
@main.route('/event-scores', methods=['POST'])
def create_event_score():
    return EventScoreController.create()

# Put routes
@main.route('/event-scores/<id>', methods=['PUT'])
def update_event_score(id):
    return EventScoreController.update(id)

# Delete routes
@main.route('/event-scores/<id>', methods=['DELETE'])
def delete_event_score(id):
    return EventScoreController.delete(id)
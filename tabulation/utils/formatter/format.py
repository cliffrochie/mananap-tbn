from tabulation.models.db import *

def format_user(user):
    data = {}
    data['id'] = user.id
    data['username'] = user.username
    data['email'] = user.email
    data['firstname'] = user.firstname
    data['middlename'] = user.middlename
    data['lastname'] = user.lastname
    data['is_active'] = user.is_active
    data['role_id'] = user.role_id
    data['organization_id'] = user.organization_id
    data['created_at'] = user.created_at
    data['updated_at'] = user.updated_at
    return data


def format_role(role):
    data = {}
    data['id'] = role.id
    data['name'] = role.name
    data['created_at'] = role.created_at
    data['updated_at'] = role.updated_at
    return data
    

def format_organization(organization):
    data = {}
    data['id'] = organization.id
    data['name'] = organization.name
    data['description'] = organization.description
    data['organization_type_id'] = organization.organization_type_id
    data['created_at'] = organization.created_at
    data['updated_at'] = organization.updated_at
    return data


def format_organization_type(organization_type):
    data = {}
    data['id'] = organization_type.id
    data['name'] = organization_type.name
    data['description'] = organization_type.description
    return data


def format_judge(judge):
    data = {}
    data['id'] = judge.id
    data['user_details'] = format_user(User.query.get(judge.user_id))
    data['created_at'] = judge.created_at
    data['updated_at'] = judge.updated_at
    return data


def format_event_type(event_type):
    data = {}
    data['id'] = event_type.id
    data['name'] = event_type.name
    data['created_at'] = event_type.created_at
    data['updated_at'] = event_type.updated_at
    return data


def format_event(event):
    data = {}
    data['id'] = event.id
    data['name'] = event.name
    data['description'] = event.description
    data['img_path'] = event.img_path
    data['is_active'] = event.is_active
    data['event_type_id'] = event.event_type_id
    data['organization_id'] = event.organization_id
    data['created_at'] = event.created_at
    data['updated_at'] = event.updated_at
    return data


def format_event_judge(event_judge):
    data = {}
    data['id'] = event_judge.id
    data['event_id'] = event_judge.event_id
    data['judge_id'] = event_judge.judge_id
    data['created_at'] = event_judge.created_at
    data['updated_at'] = event_judge.updated_at
    return data


def format_criteria(criteria):
    data = {}
    data['id'] = criteria.id
    data['name'] = criteria.name
    data['max_points'] = criteria.max_points
    data['event_id'] = criteria.event_id
    data['created_at'] = criteria.created_at
    data['updated_at'] = criteria.updated_at
    return data


def format_participant(participant):
    data = {}
    data['id'] = participant.id
    data['email'] = participant.email
    data['firstname'] = participant.firstname
    data['middlename'] = participant.middlename
    data['lastname'] = participant.lastname
    data['img_path'] = participant.img_path
    data['is_active'] = participant.is_active
    data['participant_type_id'] = participant.participant_type_id
    data['participant_team_id'] = participant.participant_team_id
    data['organization_id'] = participant.organization_id
    data['created_at'] = participant.created_at
    data['updated_at'] = participant.updated_at
    return data


def format_participant_type(participant_type):
    data = {}
    data['id'] = participant_type.id
    data['name'] = participant_type.name
    data['created_at'] = participant_type.created_at
    data['updated_at'] = participant.updated_at
    return data


def format_participant_team(participant_team):
    data = {}
    data['id'] = participant_team.id
    data['name'] = participant_team.name
    data['created_at'] = participant_team.created_at
    data['updated_at'] = participant_team.updated_at
    return data


def format_event_participant(event_participant):
    data = {}
    data['id'] = event_participant.id
    data['event_id'] = event_participant.event_id
    data['participant_id'] = event_participant.participant_id
    data['created_at'] = event_participant.created_at
    data['updated_at'] = event_participant.updated_at
    return data


def format_event_score(event_score):
    data = {}
    data['id'] = event_score.id
    data['score'] = event_score.score
    data['event_judge_id'] = event_score.event_judge_id
    data['event_participant_id'] = event_score.event_participant_id
    data['criteria_id'] = event_score.criteria_id
    data['created_at'] = event_score.created_at
    data['updated_at'] = event_score.updated_at
    return data


def format_role(role):
    data = {}
    data['id'] = role.id
    data['name'] = role.name
    data['code'] = role.code
    data['created_at'] = role.created_at
    data['updated_at'] = role.updated_at
    return data


def format_organization(organization):
    data = {}
    data['id'] = organization.id
    data['name'] = organization.name
    data['description'] = organization.description
    data['organization_type_id'] = organization.organization_type_id
    data['created_at'] = organization.created_at
    data['updated_at'] = organization.updated_at
    return data


def format_organization_type(organization_type):
    data = {}
    data['id'] = organization_type.id
    data['name'] = organization_type.name
    data['description'] = organization_type.description
    data['created_at'] = organization_type.created_at
    data['updated_at'] = organization_type.updated_at
    return data


def format_event_type(event_type):
    data = {}
    data['id'] = event_type.id
    data['name'] = event_type.name
    data['description'] = event_type.description
    data['created_at'] = event_type.created_at
    data['updated_at'] = event_type.updated_at
    return data


def format_participant_type(participant_type):
    data = {}
    data['id'] = participant_type.id
    data['name'] = participant_type.name
    data['description'] = participant_type.description
    data['created_at'] = participant_type.created_at
    data['updated_at'] = participant_type.updated_at
    return data


def format_participant_team(participant_team):
    data = {}
    data['id'] = participant_team.id
    data['name'] = participant_team.name
    data['description'] = participant_team.description
    data['created_at'] = participant_team.created_at
    data['updated_at'] = participant_team.updated_at
    return data


def format_criteria(criteria):
    data = {}
    data['id'] = criteria.id
    data['event_id'] = criteria.event_id
    data['name'] = criteria.name
    data['max_points'] = criteria.max_points
    data['created_at'] = criteria.created_at
    data['updated_at'] = criteria.updated_at
    return data


def format_event_score(event_score):
    event_judge = EventJudge.query.get(event_score.event_judge_id)
    event_participant = EventParticipant.query.get(event_score.event_participant_id)
    criteria = Criteria.query.get(event_score.criteria_id)
    data = {}
    data['id'] = event_score.id
    data['score'] = event_score.score
    data['judge'] = format_judge(event_judge.judge)
    data['participant'] = format_participant(event_participant.participant)
    data['criteria'] = format_criteria(criteria)
    return data
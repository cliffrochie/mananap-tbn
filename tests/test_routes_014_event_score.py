import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *



# -- Test event prerequisites start here
def test_create_role(test_client, test_role):
    """
    Test 1: Create new role
        POST request: response = 201
    """
    response = test_client.post(
        "/api/roles",
        data=json.dumps(test_role),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_organization_type(test_client, test_organization_type):
    """
    Test 2: Create new organization type
        POST request: response = 201
    """
    response = test_client.post(
        "/api/organization-types",
        data=json.dumps(test_organization_type),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_organization(test_client, test_organization, test_organization_type_id):
    """
    Test 3: Create new organization
        POST request: response = 201
    """
    test_organization['organization_type_id'] = test_organization_type_id
    response = test_client.post(
        "/api/organizations",
        data=json.dumps(test_organization),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_user(test_client, test_user, test_role_id, test_organization_id):
    """
    Test 4: Create new user
        POST request: response = 201
    """
    test_user['role_id'] = test_role_id
    test_user['organization_id'] = test_organization_id
    response = test_client.post(
        "/api/users",
        data=json.dumps(test_user),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_judge(test_client, test_user_id):
    """
    Test 5: Create new judge
        POST request: response = 201
    """
    payload = {"user_id": test_user_id}
    response = test_client.post(
        "/api/judges",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_participant_type(test_client, test_participant_type):
    """
    Test 6: Create new participant type
        POST request: response = 201
    """
    response = test_client.post(
        "/api/participant-types",
        data=json.dumps(test_participant_type),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_participant_team(test_client, test_participant_team):
    """
    Test 7: Create new participant team
        POST request: response = 201
    """
    response = test_client.post(
        "/api/participant-teams",
        data=json.dumps(test_participant_team),
        content_type="application/json"
    )
    assert response.status_code == 201
 

def test_create_participant(
    test_client, 
    test_participant, 
    test_participant_type_id, 
    test_participant_team_id,
    test_organization_id
):
    """
    Test 8: Create new participant
        POST request: response = 201
    """
    test_participant['participant_type_id'] = test_participant_type_id
    test_participant['participant_team_id'] = test_participant_team_id
    test_participant['organization_id'] = test_organization_id
    response = test_client.post(
        "/api/participants",
        data=json.dumps(test_participant),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_event_type(test_client, test_event_type):
    """
    Test 9: Create new event type
        POST request: response = 201
    """
    response = test_client.post(
        "/api/event-types",
        data=json.dumps(test_event_type),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_event(test_client, test_event, test_event_type_id, test_organization_id):
    """
    Test 10: Create new event
        POST request: response = 201
    """
    test_event['event_type_id'] = test_event_type_id
    test_event['organization_id'] = test_organization_id
    response = test_client.post(
        "/api/events",
        data=json.dumps(test_event),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_add_criteria(test_client, test_criteria, test_event_id):
    """
    Test 11: Create new criteria
        POST request: response = 201
    """
    test_criteria['event_id'] = test_event_id
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/criterias",
        data=json.dumps(test_criteria),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_add_judge(test_client, test_event_id, test_judge_id):
    """
    Test 12: Add new judge
        POST request: response = 201
    """
    payload = {"judge_id": test_judge_id}
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/add-judge",
        data=json.dumps(payload),
        content_type="application/json"
    ) 
    assert response.status_code == 201


def test_create_add_participant(test_client, test_event_id, test_participant_id):
    """
    Test 13: Add new participant
        POST request: response = 201
    """
    payload = {"participant_id": test_participant_id}
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/add-participant",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 201



# -- Test event starts here
def test_create_event_score(
    test_client, 
    test_event_score, 
    test_event_judge_id, 
    test_event_participant_id, 
    test_criteria_id
):
    """
    Test 14: Add new event score
        POST request: response = 201
    """
    test_event_score['event_judge_id'] = test_event_judge_id
    test_event_score['event_participant_id'] = test_event_participant_id
    test_event_score['criteria_id'] = test_criteria_id
    response = test_client.post(
        "/api/event-scores",
        data=json.dumps(test_event_score),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_event_score_fail_duplicate(
    test_client, 
    test_event_score, 
    test_event_judge_id, 
    test_event_participant_id, 
    test_criteria_id
):
    """
    Test 15: Add new event score with duplicate entry
        POST request: response = 400
    """
    test_event_score['event_judge_id'] = test_event_judge_id
    test_event_score['event_participant_id'] = test_event_participant_id
    test_event_score['criteria_id'] = test_criteria_id
    response = test_client.post(
        "/api/event-scores",
        data=json.dumps(test_event_score),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_event_score_fail_empty(test_client):
    """
    Test 16: Add new event score with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/event-scores",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


# -- Beyond this are the tests that should be the last one
def test_delete_event_score(test_client, test_event_score_id):
    """
    Test X: Delete the test event score
        DELETE request: response = 204
    """
    response = test_client.delete(
        "/api/event-scores/"+ str(test_event_score_id)
    )
    assert response.status_code == 204


def test_delete_added_participant(test_client, test_event_id, test_participant_id):
    """
    Test X: Delete the test participant in event
        DELETE request: response = 204
    """
    response = test_client.delete(
        "/api/events/"+ str(test_event_id) +"/delete-participant/"+ str(test_participant_id)
    )
    assert response.status_code == 204


def test_delete_added_judge(test_client, test_event_id, test_judge_id):
    """
    Test X: Delete the test judge in event
        DELETE request: response = 204
    """
    response = test_client.delete(
        "/api/events/"+ str(test_event_id) +"/delete-judge/"+ str(test_judge_id)
    )
    assert response.status_code == 204


def test_delete_delete_criteria(test_client, test_criteria_id, test_event_id):
    """
    Test X: Delete the test event criteria
        DELETE request: response = 204
    """
    response = test_client.delete(
        "/api/events/"+ str(test_event_id) +"/criterias/"+ str(test_criteria_id)
    )
    assert response.status_code == 204


def test_delete_event(test_client, test_event_id):
    """
    Test X: Delete the test event
        DELETE request: response = 204
    """
    response = test_client.delete("/api/events/"+ str(test_event_id))
    assert response.status_code == 204


def test_delete_event_type(test_client, test_event_type_id):
    """
    Test X: Delete the test event type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/event-types/"+ str(test_event_type_id))
    assert response.status_code == 204


def test_delete_participant(test_client, test_participant_id):
    """
    Test X: Delete the test participant
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participants/"+ str(test_participant_id))
    assert response.status_code == 204

def test_delete_participant_type(test_client, test_participant_type_id):
    """
    Test X: Delete the test participant type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participant-types/"+ str(test_participant_type_id))
    assert response.status_code == 204


def test_delete_participant_team(test_client, test_participant_team_id):
    """
    Test X: Delete the test participant team
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participant-teams/"+ str(test_participant_team_id))
    assert response.status_code == 204


def test_delete_judge(test_client, test_judge_id):
    """
    Test X: Delete the test judge
        DELETE request: response = 204
    """
    response = test_client.delete("/api/judges/"+ str(test_judge_id))
    assert response.status_code == 204


def test_delete_user(test_client, test_user_id):
    """
    Test X: Delete the test user
        DELETE request: response = 204
    """
    response = test_client.delete("/api/users/"+ str(test_user_id))
    assert response.status_code == 204


def test_delete_role(test_client, test_role_id):
    """
    Test X: Delete the test role
        DELETE request: response = 204
    """
    response = test_client.delete("/api/roles/"+ str(test_role_id))
    assert response.status_code == 204


def test_delete_organization(test_client, test_organization_id):
    """
    Test X: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 204


def test_delete_organization_type(test_client, test_organization_type_id):
    """
    Test X: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 204
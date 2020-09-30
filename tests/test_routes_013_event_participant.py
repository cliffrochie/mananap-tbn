import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *



# -- Test event judges prerequisites start here
def test_create_organization_type(test_client, test_organization_type):
    """
    Test 1: Create new organization type
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
    Test 2: Create new organization
        POST request: response = 201
    """
    test_organization['organization_type_id'] = test_organization_type_id
    response = test_client.post(
        "/api/organizations",
        data=json.dumps(test_organization),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_participant_type(test_client, test_participant_type):
    """
    Test 3: Create new participant type
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
    Test 4: Create new participant team
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
    Test 5: Create new participant
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
    Test 6: Create new event type
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
    Test 7: Create new event
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


# -- Test event judges starts here
def test_create_add_participant(test_client, test_event_id, test_participant_id):
    """
    Test 8: Add new participant
        POST request: response = 201
    """
    payload = {"participant_id": test_participant_id}
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/add-participant",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_add_participant_fail_duplicate(test_client, test_event_id, test_participant_id):
    """
    Test 9: Add new participant with duplicate entry
        POST request: response = 400
    """
    payload = {"participant_id": test_participant_id}
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/add-participant",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_add_participant_fail_wrong_id(test_client, test_participant_id):
    """
    Test 10: Add new participant with non-existent event id
        POST request: response = 404
    """
    payload = {"participant_id": test_participant_id}
    response = test_client.post(
        "/api/events/0/add-participant",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_create_add_participant_fail_wrong_id_2(test_client, test_event_id):
    """
    Test 11: Add new participant with non-existent participant id
        POST request: response = 400
    """
    payload = {"participant_id": 0}
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/add-participant",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404  


def test_create_add_participant_fail_empty(test_client, test_event_id):
    """
    Test 12: Add new participant with empty payload
        POST request: response = 400
    """
    payload = {}
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/add-participant",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_add_participant_fail_duplicate(test_client, test_event_id, test_participant_id):
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
    assert response.status_code == 400


# -- Beyond this are the tests that should be the last one
def test_delete_added_participant(test_client, test_event_id, test_participant_id):
    """
    Test 14: Delete the test participant in event
        DELETE request: response = 204
    """
    response = test_client.delete(
        "/api/events/"+ str(test_event_id) +"/delete-participant/"+ str(test_participant_id)
    )
    assert response.status_code == 204

def test_delete_event(test_client, test_event_id):
    """
    Test 15: Delete the test event
        DELETE request: response = 204
    """
    response = test_client.delete("/api/events/"+ str(test_event_id))
    assert response.status_code == 204


def test_delete_event_type(test_client, test_event_type_id):
    """
    Test 16: Delete the test event type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/event-types/"+ str(test_event_type_id))
    assert response.status_code == 204


def test_delete_participant(test_client, test_participant_id):
    """
    Test 17: Delete the test participant
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participants/"+ str(test_participant_id))
    assert response.status_code == 204


def test_delete_organization(test_client, test_organization_id):
    """
    Test 18: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 204


def test_delete_organization_type(test_client, test_organization_type_id):
    """
    Test 19: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 204


def test_delete_participant_type(test_client, test_participant_type_id):
    """
    Test 20: Delete the test participant type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participant-types/"+ str(test_participant_type_id))
    assert response.status_code == 204


def test_delete_participant_team(test_client, test_participant_team_id):
    """
    Test 21: Delete the test participant team
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participant-teams/"+ str(test_participant_team_id))
    assert response.status_code == 204
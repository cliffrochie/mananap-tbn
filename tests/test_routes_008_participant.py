import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *

# -- Test participant prerequisites start here
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


# -- Test participant starts here
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


def test_create_participant_fail_empty(test_client):
    """
    Test 6: Create new participant with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/participants",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_participant_fail_duplicate(
    test_client, 
    test_participant, 
    test_participant_type_id, 
    test_participant_team_id,
    test_organization_id
):
    """
    Test 7: Create new participant with duplicate entry
        POST request: response = 400
    """
    test_participant['participant_type_id'] = test_participant_type_id
    test_participant['participant_team_id'] = test_participant_team_id
    test_participant['organization_id'] = test_organization_id
    response = test_client.post(
        "/api/participants",
        data=json.dumps(test_participant),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_participants(test_client):
    """
    Test 8: Fetch all participants
        GET request: response = 200
    """
    response = test_client.get("/api/participants")
    assert response.status_code == 200


def test_get_participant(test_client, test_participant_id):
    """
    Test 9: Fetch specific participant
        GET request: response = 200
    """
    response = test_client.get("/api/participants/"+ str(test_participant_id))
    assert response.status_code == 200


def test_get_participant_fail_wrong_id(test_client):
    """
    Test 10: Fetch specific participant with non-existent id
        GET request: response = 404
    """
    response = test_client.get("/api/participants/0")
    assert response.status_code == 404


def test_put_participant(
    test_client, 
    test_participant_id,
    test_participant_type_id, 
    test_participant_team_id,
    test_organization_id
):
    """
    Test 11: Update the firstname of the test participant
        PUT request: response = 200
    """
    payload = {
        "email": "test-email@test.com",
        "firstname": "test-firstname-updated",
        "middlename": "test-middlename",
        "lastname": "test-lastname",
        "img_path": "test-img_path",
        "is_active": 1,
        "participant_type_id": test_participant_type_id,
        "participant_team_id": test_participant_team_id,
        "organization_id": test_organization_id
    }
    response = test_client.put(
        "/api/participants/"+ str(test_participant_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_put_participant_fail_empty(test_client, test_participant_id):
    """
    Test 12: Update the firstname of the test participant with empty payload
        PUT request: response = 400
    """
    payload = {}
    response = test_client.put(
        "/api/participants/"+ str(test_participant_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_put_participant_fail_wrong_id(
    test_client, 
    test_participant_type_id, 
    test_participant_team_id,
    test_organization_id
):
    """
    Test 13: Update the firstname of the test participant with non-existent id
        PUT request: response = 404
    """
    payload = {
        "email": "test-email@test.com",
        "firstname": "test-firstname-updated",
        "middlename": "test-middlename",
        "lastname": "test-lastname",
        "img_path": "test-img_path",
        "is_active": 1,
        "participant_type_id": test_participant_type_id,
        "participant_team_id": test_participant_team_id,
        "organization_id": test_organization_id
    }
    response = test_client.put(
        "/api/participants/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_delete_participant_fail_wrong_id(test_client):
    """
    Test 14: Delete the test participant with non-existent id
        DELETE request: response = 404
    """
    response = test_client.delete("/api/participants/0")
    assert response.status_code == 404


def test_delete_organization_fail_constraint(test_client, test_organization_id):
    """
    Test 15: Delete the test organization type
        DELETE request: response = 400
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 400


# -- Beyond this are the tests that should be the last one
def test_delete_participant(test_client, test_participant_id):
    """
    Test 16: Delete the test participant
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participants/"+ str(test_participant_id))
    assert response.status_code == 204


def test_delete_organization(test_client, test_organization_id):
    """
    Test 17: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 204


def test_delete_organization_type(test_client, test_organization_type_id):
    """
    Test 18: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 204


def test_delete_participant_type(test_client, test_participant_type_id):
    """
    Test 19: Delete the test participant type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participant-types/"+ str(test_participant_type_id))
    assert response.status_code == 204


def test_delete_participant_team(test_client, test_participant_team_id):
    """
    Test 20: Delete the test participant team
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participant-teams/"+ str(test_participant_team_id))
    assert response.status_code == 204



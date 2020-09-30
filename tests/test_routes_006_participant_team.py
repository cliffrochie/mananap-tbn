import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *


def test_create_participant_team(test_client, test_participant_team):
    """
    Test 1: Create new participant team
        POST request: response = 201
    """
    response = test_client.post(
        "/api/participant-teams",
        data=json.dumps(test_participant_team),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_participant_team_fail_empty(test_client):
    """
    Test 2: Create new participant team with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/participant-teams",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_participant_team_fail_duplicate(test_client, test_participant_team):
    """
    Test 3: Create new participant team with duplicate data
        POST request: response = 400
    """
    response = test_client.post(
        "/api/participant-teams",
        data=json.dumps(test_participant_team),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_participant_teams(test_client):
    """
    Test 4: Fetch all participant teams
        GET request: response = 200
    """
    response = test_client.get("/api/participant-teams")
    assert response.status_code == 200


def test_get_participant_team(test_client, test_participant_team_id):
    """
    Test 5: Fetch specific participant team
        GET request: response = 200
    """
    response = test_client.get(
        "/api/participant-teams/"+ str(test_participant_team_id)
    )
    assert response.status_code == 200


def test_get_participant_team_fail_wrong_id(test_client):
    """
    Test 6: Fetch specific participant team with non-existent id
        GET request: response = 404
    """
    response = test_client.get(
        "/api/participant-teams/0"
    )
    assert response.status_code == 404


def test_put_participant_team(test_client, test_participant_team_id):
    """
    Test 7: Update the description value of the test participant team
        PUT request: response = 200
    """
    payload = {"name": "test-participant-team", "description": "test-description-updated"}
    response = test_client.put(
        "/api/participant-teams/"+ str(test_participant_team_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_put_participant_team_fail_empty(test_client, test_participant_team_id):
    """
    Test 8: Update the test participant team with empty payload
        PUT request: response = 400 
    """
    payload = {}
    response = test_client.put(
        "/api/participant-teams/"+ str(test_participant_team_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400  


def test_put_participant_team_fail_wrong_id(test_client):
    """
    Test 9: Update the test participant team with non-existent id
        PUT request: response = 404 
    """
    payload = {"name": "test-participant-team", "description": "test-description-updated"}
    response = test_client.put(
        "/api/participant-teams/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_delete_participant_team_fail_wrong_id(test_client):
    """
    Test 10: Delete the test participant team with wrong id
        DELETE request: response = 404
    """
    response = test_client.delete("/api/participant-teams/0")
    assert response.status_code == 404



# -- Beyond this are the tests that should be the last one
def test_delete_participant_team(test_client, test_participant_team_id):
    """
    Test 11: Delete the test participant team
        DELETE request: response = 204
    """
    response = test_client.delete("/api/participant-teams/"+ str(test_participant_team_id))
    assert response.status_code == 204
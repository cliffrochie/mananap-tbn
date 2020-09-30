import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *



# -- Test criteria prerequisites start here
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


def test_create_event_type(test_client, test_event_type):
    """
    Test 3: Create new event type
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
    Test 4: Create new event
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


# -- Test criteria starts here
def test_create_add_criteria(test_client, test_criteria, test_event_id):
    """
    Test 5: Create new criteria
        POST request: response = 201
    """
    test_criteria['event_id'] = test_event_id
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/criterias",
        data=json.dumps(test_criteria),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_create_add_criteria_fail_empty(test_client, test_event_id):
    """
    Test 6: Create new criteria with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/criterias",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_add_criteria_fail_wrong_event_id(test_client):
    """
    Test 7: Create new criteria with wrong event id
        POST request: response = 400
    """
    response = test_client.post("/api/events/0/criterias")
    assert response.status_code == 400


def test_create_add_criteria_fail_empty(test_client, test_event_id):
    """
    Test 8: Create new criteria with non-existent event id
        POST request: response = 400
    """
    response = test_client.post(
        "/api/events/"+ str(test_event_id) +"/criterias",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_update_update_criteria(test_client, test_event_id, test_criteria_id):
    """
    Test 9: Update criteria
        PUT request: response = 400
    """
    payload = {
        "name": "test-criteria",
        "max_points": 80,
        "event_id": test_event_id
    }
    response = test_client.put(
        "/api/events/"+ str(test_event_id) +"/criterias/"+ str(test_criteria_id),
        data=json.dumps(payload),
        content_type="application/json" 
    )
    assert response.status_code == 200


def test_update_update_criteria_fail_empty(test_client, test_event_id, test_criteria_id):
    """
    Test 10: Update criteria with empty payload
        PUT request: response = 400
    """
    response = test_client.put(
        "/api/events/" + str(test_event_id) +"/criterias/"+ str(test_criteria_id),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_update_update_criteria_fail_wrong_id(test_client, test_event_id):
    """
    Test 11: Update criteria
        PUT request: response = 400
    """
    payload = {
        "name": "test-criteria",
        "max_points": 80,
        "event_id": test_event_id
    }
    response = test_client.put(
        "/api/events/"+ str(test_event_id) +"/criterias/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400



def test_delete_delete_criteria_fail_wrong_id(test_client, test_event_id):
    """
    Test 12: Delete the test event criteria
        DELETE request: response = 404
    """
    response = test_client.delete(
        "/api/events/"+ str(test_event_id) +"/criterias/0"
    )
    assert response.status_code == 404


def test_delete_event_fail_constraint(test_client, test_event_id):
    """
    Test 13: Delete the test event
        DELETE request: response = 400
    """
    response = test_client.delete("/api/events/"+ str(test_event_id))
    assert response.status_code == 400


# -- Beyond this are the tests that should be the last one
def test_delete_delete_criteria(test_client, test_criteria_id, test_event_id):
    """
    Test 14: Delete the test event criteria
        DELETE request: response = 204
    """
    response = test_client.delete(
        "/api/events/"+ str(test_event_id) +"/criterias/"+ str(test_criteria_id)
    )
    assert response.status_code == 204


def test_delete_event(test_client, test_event_id):
    """
    Test 15: Delete the test event
        DELETE request: response = 204
    """
    response = test_client.delete("/api/events/"+ str(test_event_id))
    assert response.status_code == 204


def test_delete_organization(test_client, test_organization_id):
    """
    Test 16: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 204
    

def test_delete_organization_type(test_client, test_organization_type_id):
    """
    Test 17: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 204


def test_delete_event_type(test_client, test_event_type_id):
    """
    Test 18: Delete the test event type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/event-types/"+ str(test_event_type_id))
    assert response.status_code == 204
import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *



# -- Test event prerequisites start here
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
 

# -- Test event starts here
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


def test_create_event_fail_empty(test_client):
    """
    Test 5: Create new event with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/events",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_event_fail_duplicate(test_client, test_event, test_event_type_id, test_organization_id):
    """
    Test 6: Create new event
        POST request: response = 400
    """
    test_event['event_type_id'] = test_event_type_id
    test_event['organization_id'] = test_organization_id
    response = test_client.post(
        "/api/events",
        data=json.dumps(test_event),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_events(test_client):
    """
    Test 7: Fetch all events
        GET request: response = 200
    """
    response = test_client.get("/api/events")
    assert response.status_code == 200


def test_get_event(test_client, test_event_id):
    """
    Test 8: Fetch specific events
        GET request: response = 200
    """
    response = test_client.get("/api/events/"+ str(test_event_id))
    assert response.status_code == 200


def test_get_event_fail_wrong_id(test_client):
    """
    Test 9: Fetch specific events with non-existent id
        GET request: response = 404
    """
    response = test_client.get("/api/events/0")
    assert response.status_code == 404


def test_put_event(test_client, test_event_id, test_event_type_id, test_organization_id):
    """
    Test 10: Update the description value of test event
        PUT request: response = 200
    """
    payload = {
        "name": "test-event",
        "description": "test-description-updated",
        "img_path": "test-img_path",
        "is_active": 1,
        "event_type_id": test_event_type_id,
        "organization_id": test_organization_id
    }
    response = test_client.put(
        "/api/events/"+ str(test_event_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_put_event_fail_wrong_id(test_client, test_event_type_id, test_organization_id):
    """
    Test 11: Update the test event with non-existent id
        PUT request: response = 404
    """
    payload = {
        "name": "test-event",
        "description": "test-description-updated",
        "img_path": "test-img_path",
        "is_active": 1,
        "event_type_id": test_event_type_id,
        "organization_id": test_organization_id
    }
    response = test_client.put(
        "/api/events/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_put_event_fail_empty(test_client, test_event_id):
    """
    Test 12: Update the test event with empty payload
        PUT request: response = 400
    """
    payload = {}
    response = test_client.put(
        "/api/events/"+ str(test_event_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400

def test_delete_event_fail_wrong_id(test_client):
    """
    Test 13: Delete the test event
        DELETE request: response = 404
    """
    response = test_client.delete("/api/events/0")
    assert response.status_code == 404


def test_delete_event_type_fail_constraint(test_client, test_event_type_id):
    """
    Test 14: Delete the test event type
        DELETE request: response = 400
    """
    response = test_client.delete("/api/event-types/"+ str(test_event_type_id))
    assert response.status_code == 400


def test_delete_organization_fail_constraint(test_client, test_organization_id):
    """
    Test 15: Delete the test organization type
        DELETE request: response = 400
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 400


# -- Beyond this are the tests that should be the last one
def test_delete_event(test_client, test_event_id):
    """
    Test 16: Delete the test event
        DELETE request: response = 204
    """
    response = test_client.delete("/api/events/"+ str(test_event_id))
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


def test_delete_event_type(test_client, test_event_type_id):
    """
    Test 19: Delete the test event type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/event-types/"+ str(test_event_type_id))
    assert response.status_code == 204
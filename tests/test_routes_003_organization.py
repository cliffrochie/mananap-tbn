import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *


# -- Test organization prerequisites start here
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


# -- Test organization starts here
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


def test_create_organization_fail_empty(test_client):
    """
    Test 3: Create new organization with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/organization-types",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_organization_fail_duplicate(test_client, test_organization, test_organization_type_id):
    """
    Test 4: Create new organization with duplicate data
        POST request: response = 400
    """
    test_organization['organization_type_id'] = test_organization_type_id
    response = test_client.post(
        "/api/organizations",
        data=json.dumps(test_organization),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_organizations(test_client):
    """
    Test 5: Fetch all organizations
        GET request: response = 200
    """
    response = test_client.get("/api/organizations")
    assert response.status_code == 200


def test_get_organization_type(test_client, test_organization_id):
    """
    Test 6: Fetch specific organization
        POST request: response = 200
    """
    response = test_client.get("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 200


def test_get_organization_type_fail_wrong_id(test_client):
    """
    Test 7: Fetch specific organization with non-existent id
        POST request: response = 404
    """
    response = test_client.get("/api/organizations/0")
    assert response.status_code == 404


def test_put_organization(test_client, test_organization_id, test_organization_type_id):
    """
    Test 8: Update the description value of the test organization
        PUT request: response = 200
    """
    payload = {
        "name": "test-organization", 
        "description": "test-description-updated", 
        "organization_type_id": test_organization_type_id
    }
    response = test_client.put(
        "/api/organizations/"+ str(test_organization_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_put_organization_fail_empty(test_client, test_organization_id, test_organization_type_id):
    """
    Test 9: Update the description value of the test organization with empty payload
        PUT request: response = 400
    """
    payload = {}
    response = test_client.put(
        "/api/organizations/"+ str(test_organization_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_put_organization_fail_wrong_id(test_client, test_organization_type_id):
    """
    Test 10: Update the description value of the test organization with non-existent id
        PUT request: response = 404
    """
    payload = {
        "name": "test-organization", 
        "description": "test-description-updated", 
        "organization_type_id": test_organization_type_id
    }
    response = test_client.put(
        "/api/organizations/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_delete_organization_fail_wrong_id(test_client):
    """
    Test 11: Delete the test organization with non-existent id
        DELETE request: response = 404
    """
    response = test_client.delete("/api/organizations/0")
    assert response.status_code == 404


def test_delete_organization_type_fail_constraint(test_client, test_organization_type_id):
    """
    Test 12: Delete the test organization type with constraint
        DELETE request: response = 400
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 400



# -- Beyond this are the tests that should be the last one
def test_delete_organization(test_client, test_organization_id):
    """
    Test 13: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 204


def test_delete_organization_type(test_client, test_organization_type_id):
    """
    Test 14: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 204
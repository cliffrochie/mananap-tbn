import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *


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


def test_create_organization_type_fail_empty(test_client):
    """
    Test 2: Create new organization type with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/organization-types",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_organization_type_fail_duplicate(test_client, test_organization_type):
    """
    Test 3: Create new organization-types with duplicate data
        POST request: response = 400
    """
    response = test_client.post(
        "/api/organization-types",
        data=json.dumps(test_organization_type),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_organization_types(test_client):
    """
    Test 4: Fetch all organization types
        GET request: response = 200
    """
    response = test_client.get("/api/organization-types")
    assert response.status_code == 200


def test_get_organization_type(test_client, test_organization_type_id):
    """
    Test 5: Fetch specific organization type
        POST request: response = 200
    """
    response = test_client.get("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 200


def test_get_organization_type_fail_wrong_id(test_client):
    """
    Test 6: Fetch specific organization type with non-existent id
        POST request: response = 404
    """
    response = test_client.get("/api/organization-types/0")
    assert response.status_code == 404


def test_put_organization_type(test_client, test_organization_type_id):
    """
    Test 7: Update the description value of the test organization type
        PUT request: response = 200
    """
    payload = {"name": "test-organization-type", "description": "test-description-updated"}
    response = test_client.put(
        "/api/organization-types/"+ str(test_organization_type_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_put_organization_type_fail_empty(test_client, test_organization_type_id):
    """
    Test 8: Update organization type with empty data
        PUT request: response = 400
    """
    payload = {}
    response = test_client.put(
        "/api/organization-types/"+ str(test_organization_type_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_put_organization_type_fail_wrong_id(test_client):
    """
    Test 9: Update organization type with wrong id
        PUT request: response = 404
    """
    payload = {"name": "test-organization-type", "description": "test-description"}
    response = test_client.put(
        "/api/organization-types/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_delete_organization_type_fail_wrong_id(test_client):
    """
    Test 10: Delete the test organization type with non-existent id
        DELETE request: response = 404
    """
    response = test_client.delete("/api/organization-types/0")
    assert response.status_code == 404



# -- Beyond this are the tests that should be the last one
def test_delete_organization_type(test_client, test_organization_type_id):
    """
    Test 11: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 204
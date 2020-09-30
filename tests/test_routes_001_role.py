import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *
from factories.base_factory import *


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


def test_create_role_fail_empty(test_client):
    """
    Test 2: Create new role with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/roles",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_role_fail_duplicate(test_client, test_role):
    """
    Test 3: Create new role with duplicate data
        POST request: response = 400
    """
    response = test_client.post(
        "/api/roles",
        data=json.dumps(test_role),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_roles(test_client):
    """
    Test 4: Fetch all roles
        GET request: response = 200
    """
    response = test_client.get("/api/roles")
    assert response.status_code == 200


def test_get_role(test_client, test_role_id):
    """
    Test 5: Fetch specific role
        POST request: response = 200
    """
    response = test_client.get("/api/roles/"+ str(test_role_id))
    assert response.status_code == 200


def test_get_role_fail_wrong_id(test_client):
    """
    Test 6: Fetch specific role with non-existent id
        POST request: response = 404
    """
    response = test_client.get("/api/roles/0")
    assert response.status_code == 404


def test_put_role(test_client, test_role_id):
    """
    Test 7: Update the code value of the test role
        PUT request: response = 200
    """
    payload = {"name": "test-role", "code": 0}
    response = test_client.put(
        "/api/roles/"+ str(test_role_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_put_role_fail_empty(test_client, test_role_id):
    """
    Test 8: Update role with empty data
        PUT request: response = 400
    """
    payload = {}
    response = test_client.put(
        "/api/roles/"+ str(test_role_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_put_role_fail_wrong_id(test_client):
    """
    Test 9: Update role with wrong id
        PUT request: response = 404
    """
    payload = {"name": "test-role", "code": 99}
    response = test_client.put(
        "/api/roles/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404



def test_delete_role_fail_wrong_id(test_client):
    """
    Test 10: Delete the test role with non-existent id
        DELETE request: response = 404
    """
    response = test_client.delete("/api/roles/0")
    assert response.status_code == 404




# -- Beyond this are the tests that should be the last one
def test_delete_role(test_client, test_role_id):
    """
    Test 11: Delete the test role
        DELETE request: response = 204
    """
    response = test_client.delete("/api/roles/"+ str(test_role_id))
    assert response.status_code == 204
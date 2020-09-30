import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *



# -- Test judge prerequisites start here
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


# -- Test judge starts here
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


def test_create_judge_fail_empty(test_client):
    """
    Test 6: Create new judge
        POST request: response = 400
    """
    payload = {}
    response = test_client.post(
        "/api/judges",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_delete_judge_fail_wrong_id(test_client):
    """
    Test 7: Delete the test judge with non-existent id
        DELETE request: response = 404
    """
    response = test_client.delete("/api/judges/0")
    assert response.status_code == 404


# -- Beyond this are the tests that should be the last one
def test_delete_judge(test_client, test_judge_id):
    """
    Test 8: Delete the test judge
        DELETE request: response = 204
    """
    response = test_client.delete("/api/judges/"+ str(test_judge_id))
    assert response.status_code == 204


def test_delete_user(test_client, test_user_id):
    """
    Test 9: Delete the test user
        DELETE request: response = 204
    """
    response = test_client.delete("/api/users/"+ str(test_user_id))
    assert response.status_code == 204


def test_delete_role(test_client, test_role_id):
    """
    Test 10: Delete the test role
        DELETE request: response = 204
    """
    response = test_client.delete("/api/roles/"+ str(test_role_id))
    assert response.status_code == 204


def test_delete_organization(test_client, test_organization_id):
    """
    Test 11: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 204


def test_delete_organization_type(test_client, test_organization_type_id):
    """
    Test 12: Delete the test organization type
        DELETE request: response = 204
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 204
import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *

# -- Test user prerequisites start here
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


# -- Test user starts here
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


def test_create_user_fail_empty(test_client):
    """
    Test 5: Create new user with empty payload
        POST request: response = 400
    """
    response = test_client.post(
        "/api/users",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_create_user_fail_duplicate(test_client, test_user, test_role_id, test_organization_id):
    """
    Test 6: Create new user with duplicate data
        POST request: response = 400
    """
    test_user['role_id'] = test_role_id
    test_user['organization_id'] = test_organization_id
    response = test_client.post(
        "/api/users",
        data=json.dumps(test_user),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_users(test_client):
    """
    Test 7: Fetch all users
        GET request: response = 200
    """
    response = test_client.get("/api/users")
    assert response.status_code == 200


def test_get_user(test_client, test_user_id):
    """
    Test 8: Fetch specific user
        GET request: response = 200
    """
    response = test_client.get("/api/users/"+ str(test_user_id))
    assert response.status_code == 200


def test_get_user_fail_wrong_id(test_client):
    """
    Test 9: Fetch specific user with non-existent id
        GET request: response = 404
    """
    response = test_client.get("/api/users/0")
    assert response.status_code == 404


def test_put_user(test_client, test_user_id, test_role_id, test_organization_id):
    """
    Test 10: Update the email of the test user
        GET request: response = 200
    """
    payload = {
        'username': 'test-username',
        'email': 'test-email-update@test.com',
        'password': 'test-password',
        'firstname': 'test-firstname',
        'middlename': 'test-middlename',
        'lastname': 'test-lastname',
        'is_active': 1,
        'role_id': test_role_id,
        'organization_id': test_organization_id
    }
    response = test_client.put(
        "/api/users/"+ str(test_user_id),
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200


def test_put_use_fail_wrong_id(test_client, test_role_id, test_organization_id):
    """
    Test 11: Update the email of the test user with non-existent id
        GET request: response = 404
    """
    payload = {
        'username': 'test-username',
        'email': 'test-email-update@test.com',
        'password': 'test-password',
        'firstname': 'test-firstname',
        'middlename': 'test-middlename',
        'lastname': 'test-lastname',
        'is_active': 1,
        'role_id': test_role_id,
        'organization_id': test_organization_id
    }
    response = test_client.put(
        "/api/users/0",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_put_use_fail_empty(test_client, test_user_id):
    """
    Test 12: Update the test user with no data
        GET request: response = 400
    """
    response = test_client.put(
        "/api/users/"+ str(test_user_id),
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400

def test_delete_role_fail_constraint(test_client, test_role_id):
    """
    Test 13: Delete the test role
        DELETE request: response = 400
    """
    response = test_client.delete("/api/roles/"+ str(test_role_id))
    assert response.status_code == 400


def test_delete_organization_type_fail_constraing(test_client, test_organization_type_id):
    """
    Test 14: Delete the test organization type
        DELETE request: response = 400
    """
    response = test_client.delete("/api/organization-types/"+ str(test_organization_type_id))
    assert response.status_code == 400


def test_delete_organization_fail_constraint(test_client, test_organization_id):
    """
    Test 15: Delete the test organization type
        DELETE request: response = 400
    """
    response = test_client.delete("/api/organizations/"+ str(test_organization_id))
    assert response.status_code == 400


# -- Beyond this are the tests that should be the last one
def test_delete_user(test_client, test_user_id):
    """
    Test 16: Delete the test user
        DELETE request: response = 204
    """
    response = test_client.delete("/api/users/"+ str(test_user_id))
    assert response.status_code == 204


def test_delete_role(test_client, test_role_id):
    """
    Test 17: Delete the test role
        DELETE request: response = 204
    """
    response = test_client.delete("/api/roles/"+ str(test_role_id))
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
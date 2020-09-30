import sys, os
import pytest
import mysql.connector

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation import create_app, db
from tabulation.models.db import *

def db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='tabulation'
    )

    return conn


@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield test_client
    ctx.pop()


@pytest.fixture(scope="module")
def test_role():
    role = {
        'name': 'test-role',
        'code': 99
    }

    return role

@pytest.fixture(scope="module")
def test_role_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM role WHERE name = "test-role"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_organization_type():
    organization_type = {
        "name": "test-organization-type",
        "description": "test-description"
    }

    return organization_type


@pytest.fixture(scope="module")
def test_organization_type_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id from organization_type WHERE name = "test-organization-type"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_organization():

    data = {
        'name': 'test-organization',
        'description': 'test-description',
        'organization_type_id': 0
    }

    return data


@pytest.fixture(scope="module")
def test_organization_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM organization WHERE name = "test-organization"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_user():
    user = {
        'username': 'test-username',
        'email': 'test-email@test.com',
        'password': 'test-password',
        'firstname': 'test-firstname',
        'middlename': 'test-middlename',
        'lastname': 'test-lastname',
        'role_id': 0,
        'organization_id': 0
    }

    return user

@pytest.fixture(scope="module")
def test_user_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM user WHERE username = "test-username"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_participant_type():
    participant_type = {
        "name": "test-participant-type",
        "description": "test-description"
    }

    return participant_type


@pytest.fixture(scope="module")
def test_participant_type_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM participant_type WHERE name = "test-participant-type"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_participant_team():
    participant_team = {
        "name": "test-participant-team",
        "description": "test-description"
    }

    return participant_team


@pytest.fixture(scope="module")
def test_participant_team_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM participant_team WHERE name = "test-participant-team"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_participant():
    participant = {
        "email": "test-email@test.com",
        "firstname": "test-firstname",
        "middlename": "test-middlename",
        "lastname": "test-lastname",
        "img_path": "test-img_path",
        "participant_type_id": 0,
        "participant_team_id": 0,
        "organization_id": 0
    }

    return participant


@pytest.fixture(scope="module")
def test_participant_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM participant WHERE email = "test-email@test.com"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_judge_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM user WHERE username = "test-username"'
    cursor.execute(sql)
    result = cursor.fetchone()

    sql2 = 'SELECT id FROM judge WHERE user_id = '+ str(result[0])
    cursor.execute(sql2)
    result2 = cursor.fetchone()
    conn.close()

    return result2[0]


@pytest.fixture(scope="module")
def test_event_type():
    event_type = {
        "name": "test-event-type",
        "description": "test-description"
    }

    return event_type


@pytest.fixture(scope="module")
def test_event_type_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM event_type WHERE name = "test-event-type"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_event():
    event = {
        "name": "test-event",
        "description": "test-description",
        "img_path": "test-img_path",
        "event_type_id": 0,
        "organization_id": 0
    }

    return event


@pytest.fixture(scope="module")
def test_event_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM event WHERE name = "test-event"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_criteria():
    criteria = {
        "name": "test-criteria",
        "max_points": 100,
        "event_id": 0
    }

    return criteria


@pytest.fixture(scope="module")
def test_criteria_id():
    conn = db()
    cursor = conn.cursor()
    sql = 'SELECT id FROM criteria WHERE name = "test-criteria"'
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_event_judge_id():
    conn = db()
    cursor = conn.cursor()
    sql = """
        SELECT event_judge.id FROM event_judge
        INNER JOIN event ON event.id = event_judge.event_id
        WHERE event.name = "test-event"
    """
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]


@pytest.fixture(scope="module")
def test_event_participant_id():
    conn = db()
    cursor = conn.cursor()
    sql = """
        SELECT event_participant.id FROM event_participant
        INNER JOIN event ON event.id = event_participant.event_id
        WHERE event.name = "test-event"
    """
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()
    
    return result[0]


@pytest.fixture(scope="module")
def test_event_score():
    event_score = {
        "score": 50,
        "event_judge_id": 0,
        "event_participant_id": 0,
        "criteria_id": 0
    }

    return event_score


@pytest.fixture(scope="module")
def test_event_score_id():
    conn = db()
    cursor = conn.cursor()
    sql = """
        SELECT event_score.id FROM event_score
        INNER JOIN criteria ON criteria.id = event_score.criteria_id
        WHERE criteria.name = "test-criteria"
    """
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result[0]

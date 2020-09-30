import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *
from factories.base_factory import *


# TEST PING
def test_get_ping(test_client):
    """
    Test 1: Check connection
        GET request: response = 200
    """
    response = test_client.get("/api/ping")
    assert response.status_code == 200








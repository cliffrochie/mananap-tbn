
import sys, os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from tabulation.models.db import *

from tabulation import __version__

def test_version():
    assert __version__ == '0.1.0'

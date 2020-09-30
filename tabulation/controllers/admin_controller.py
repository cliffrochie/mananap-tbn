from flask import request, jsonify
from tabulation import db
from tabulation.models.db import *
from tabulation.utils.formatter.format import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class AdminController:
    """ Route resources """
    
    @staticmethod
    def all():
        pass

    @staticmethod
    def find(id):
        pass

    @staticmethod
    def create():
        pass

    @staticmethod
    def update(id):
        pass

    @staticmethod
    def delete(id):
        pass
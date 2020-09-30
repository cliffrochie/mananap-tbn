import sys, os
import factory.alchemy
from tabulation import db
from tabulation.models.db import *

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session




class RoleFactory(BaseFactory):
    class Meta:
        model = Role

    name = "Test"
    code = "test"


class OrganizationTypeFactory(BaseFactory):
    class Meta:
        model = OrganizationType

    name = "test"


class OrganizationFactory(BaseFactory):
    class Meta:
        model = Organization

    name = "organizationtest"
    description = "descriptiontest"
    organization_type_id = 1


class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = "usertest"
    email = "usertest@test.com"
    password = "password"
    firstname = "firstnametest"
    middlename = "middlenametest"
    lastname = "lastnametest"
    role_id = 1
    organization_id = 1
    

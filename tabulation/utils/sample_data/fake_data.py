from tabulation import db
from tabulation.models.db import *

from werkzeug.security import generate_password_hash

from sqlalchemy.sql.expression import func
from faker import Faker
import random

"""
Functions to be called:
    generate_organization_type -
    generate_organization -
    generate_roles -
    generate_users -
    generate_event_type - 
    generate_events -
    generate_participant_type -
    generate_participant_team -
    generate_participants -
    generate_judges -
    assign_event_judge
"""

def generate_organization_type():
    try:

        organization_type = [
            {
                'name': 'School',
                'description': 'Use for school activities.'
            },
            {
                'name': 'Private Entity',
                'description': 'I dunno what they really are.'
            },
            {
                'name': 'Government',
                'description': 'There rumor says they are corrupt.'
            }
        ]

        for data in organization_type:
            organization_type = OrganizationType(data['name'], data['description'])

            db.session.add(organization_type)
            db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_organization_type: ", str(e) +"\n")
        return "400"
    
    return "200"


def generate_organization():
    try:

        organization = [
            {
                'name': 'ACLC College of Butuan',
                'description': 'ACLC Butuan, para sa ato ning tanan!',
                'organization_type': 'School'
            },
            {
                'name': 'Obrero Warriors Club',
                'description': 'Ang lugar na daghay mamirahay!',
                'organization_type': 'Private Entity'
            },
            {
                'name': 'Balaanon',
                'description': 'Gamhanan makahubog!',
                'organization_type': 'Government'
            },
        ]

        for data in organization:
            
            organization_type = OrganizationType.query.filter(
                OrganizationType.name == data['organization_type']
            ).one_or_none()

            organization = Organization(
                data['name'], 
                data['description'], 
                organization_type.id
            )

            db.session.add(organization)
            db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_organization: ", str(e) +"\n")
        return "400"

    return "200"


def generate_roles():
    try:

        roles = [
            {'name': 'Admin', 'code': '1'},
            {'name': 'Manager', 'code': '2'},
            {'name': 'User', 'code': '3'},
        ]

        for data in roles:

            role = Role(data['name'], data['code'])
            db.session.add(role)
            db.session.commit()
    
    except Exception as e:
        print("\nException >>>>> generate_roles: ", str(e) +"\n")
        return "400"

    return "200"


def generate_users():
    try:

        role_user = Role.query.filter(Role.name == 'User').one_or_none()

        organization_user = Organization.query.filter(
            Organization.name == 'ACLC College of Butuan'
        ).one_or_none()

        for data in range(10):
            f = Faker()
            profile = f.simple_profile()

            if len(profile['name'].split()) == 2:
                user = User(
                    profile['username'],
                    profile['mail'],
                    generate_password_hash('password'),
                    profile['name'].split()[0],
                    '',
                    profile['name'].split()[1],
                    role_user.id,
                    organization_user.id
                )
                
                db.session.add(user)
                db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_users: ", str(e) +"\n")
        return "400"

    return "200"


def generate_event_type():
    try:

        event_type = [
            {'name': 'Individual', 'description': 'Event for individual participant'},
            {'name': 'Group', 'description': 'Event for group participant'}
        ]

        for data in event_type:
            event_type = EventType(data['name'], data['description'])
                    
            db.session.add(event_type)
            db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_event_types: ", str(e) +"\n")
        return "400"

    return "200"


def generate_events():
    events = [
        {
            'name': 'The Voice Teens', 
            'description': '', 
            'event_type': 'Individual', 
            'organization': 'ACLC College of Butuan'
        },
        {
            'name': 'Miss Beauty Pageant', 
            'description': '', 
            'event_type': 'Individual', 
            'organization': 'ACLC College of Butuan'
        },
        {
            'name': 'Awesome Dance Competition', 
            'description': '', 
            'event_type': 'Group', 
            'organization': 'ACLC College of Butuan'
        },
        {
            'name': 'Macho Gay', 
            'description': '', 
            'event_type': 'Individual',
            'organization': 'ACLC College of Butuan'
        }
    ]

    for data in events:
        event_type = EventType.query.filter(EventType.name == data['event_type']).one_or_none()
        organization = Organization.query.filter(Organization.name == data['organization']).one_or_none()

        event = Event(
            data['name'], 
            data['description'], 
            '', 
            event_type.id, 
            organization.id
        )

        try:

            db.session.add(event)
            db.session.commit()

        except Exception as e:
            print("\nException >>>>> generate_events: ", str(e) +"\n")
            return "400"

    return "200"


def generate_participant_type():
    try:
        participant_type = [
            {'name': 'Individual', 'description': 'Individual description'},
            {'name': 'Group', 'description': 'Group description'}
        ]

        for data in participant_type:
            participant_type = ParticipantType(data['name'], data['description'])

            db.session.add(participant_type)
            db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_participant_types: ", str(e) +"\n")
        return "400"

    return "200"

        

def generate_participant_team():
    try:

        p = ParticipantTeam('None', 'None description')

        db.session.add(p)
        db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_participant_team: ", str(e) +"\n")
        return "400"

    return "200"


def generate_participants():
    try:
        participant_type = ParticipantType.query.filter(ParticipantType.name == 'Individual').one_or_none()
        participant_team = ParticipantTeam.query.filter(ParticipantTeam.name == 'None').one_or_none()
        organization = Organization.query.filter(Organization.name == 'ACLC College of Butuan').one_or_none()

        for i in range(20):
            f = Faker()
            profile = f.simple_profile()

            if len(profile['name'].split()) == 2:
                participant = Participant(
                    profile['mail'],
                    profile['name'].split()[0],
                    '',
                    profile['name'].split()[1],
                    '',
                    participant_type.id,
                    participant_team.id,
                    organization.id
                )

                db.session.add(participant)
                db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_participants: ", str(e) +"\n")
        return "400"

    return "200"


def generate_judges():
    try:
        for i in range(6):
            user = User.query.order_by(func.rand()).first()
            check_exists = Judge.query.filter(Judge.user_id == user.id).first()

            if not check_exists:
                judge = Judge(user.id)

                db.session.add(judge)
                db.session.commit()

    except Exception as e:
        print("\nException >>>>> generate_judges: ", str(e) +"\n")
        return "400"

    return "200"
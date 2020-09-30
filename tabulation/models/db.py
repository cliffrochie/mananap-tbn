from tabulation import db
from datetime import datetime as dt


""" Models for every tables """

class User(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(225), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50))
    lastname = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=0)
    # Relationship: Foreign Key
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    # Relationship
    judges = db.relationship('Judge', backref='user', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(
        self,
        username,
        email,
        password,
        firstname,
        middlename,
        lastname,
        role_id,
        organization_id
    ):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.role_id = role_id
        self.organization_id = organization_id


    def __repr__(self):
        return "<User %r>" % self.username


class Role(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.Integer, unique=True, nullable=False)
    # Relationship
    users = db.relationship('User', backref='role', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)
    
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return "<Role %r>" % self.name

    
class Organization(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    # Relationship: Foreign Key
    organization_type_id = db.Column(db.Integer, db.ForeignKey('organization_type.id'), nullable=False)
    # Relationship
    users = db.relationship('User', backref='organization', lazy='dynamic')
    events = db.relationship('Event', backref='organization', lazy='dynamic')
    participants = db.relationship('Participant', backref='organization', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, name, description, organization_type_id):
        self.name = name
        self.description = description
        self.organization_type_id = organization_type_id

    def __repr__(self):
        return "<Organization %r>" % self.name


class OrganizationType(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    # Relationship
    organizations = db.relationship('Organization', backref='organization_type', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<OrganizationType %r>" % self.name


class Judge(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    # Relationship: Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    # Relationship
    event_judges = db.relationship('EventJudge', backref='judge', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return "<Judge %r>" % self.id


class EventType(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    # Relationship
    events = db.relationship('Event', backref='event_type', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<EventType %r>" % self.name


class Event(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    img_path = db.Column(db.String(100))
    is_active = db.Column(db.Integer, nullable=False, default=0)
    # Relationship: Foreign Key
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    # Relationship
    criterias = db.relationship('Criteria', backref='event', lazy='dynamic')
    event_judges = db.relationship('EventJudge', backref='event', lazy='dynamic')
    event_participants = db.relationship('EventParticipant', backref='event', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, name, description, img_path, event_type_id, organization_id):
        self.name = name
        self.description = description
        self.img_path = img_path
        self.event_type_id = event_type_id
        self.organization_id = organization_id

    def __repr__(self):
        return "<Event %r>" % self.name


class EventJudge(db.Model):
    __table_args__ = (db.UniqueConstraint('event_id', 'judge_id'),)
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    # Relationship: Foreign Key
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'), nullable=False)
    # Relationship
    event_scores = db.relationship('EventScore', backref='event_judge', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)
    
    def __init__(self, event_id, judge_id):
        self.event_id = event_id
        self.judge_id = judge_id

    def __repr__(self):
        return "<EventJudge %r>" % self.id


class Criteria(db.Model):
    __table_args__ = (db.UniqueConstraint('name', 'event_id'),)
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    max_points = db.Column(db.Float, nullable=False, default=0)
    # Relationship: Foreign Key
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    # Relationship
    event_scores = db.relationship('EventScore', backref='criteria', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, name, max_points, event_id):
        self.name = name
        self.max_points = max_points
        self.event_id = event_id

    def __repr__(self):
        return "<Criteria %r>" % self.name


class Participant(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50))
    lastname = db.Column(db.String(50), nullable=False)
    img_path = db.Column(db.String(200))
    is_active = db.Column(db.Integer, nullable=False, default=0)
    # Relationship: Foreign Key
    participant_type_id = db.Column(db.Integer, db.ForeignKey('participant_type.id'), nullable=False)
    participant_team_id = db.Column(db.Integer, db.ForeignKey('participant_team.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    # Relationship
    event_participants = db.relationship('EventParticipant', backref='participant', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(
        self, 
        email, 
        firstname, 
        middlename, 
        lastname, 
        img_path, 
        participant_type_id, 
        participant_team_id, 
        organization_id
    ):
        self.email = email
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.img_path = img_path
        self.participant_type_id = participant_type_id
        self.participant_team_id = participant_team_id
        self.organization_id = organization_id

    def __repr__(self):
        return "<Participant %r>" % self.firstname + " " + self.lastname


class ParticipantType(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    # Relationship
    participants = db.relationship('Participant', backref='participant_type', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<ParticipantType %r>" % self.name


class ParticipantTeam(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    # Relationship
    participants = db.relationship('Participant', backref='participant_team', lazy='dynamic')
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<ParticipantTeam %r>" % self.name


class EventParticipant(db.Model):
    __table_args__ = (db.UniqueConstraint('event_id', 'participant_id', 'participant_no'),)
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    participant_no = db.Column(db.Integer)
    # Relationship: Foreign Key
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, event_id, participant_id, participant_no):
        self.event_id = event_id
        self.participant_id = participant_id
        self.participant_no = participant_no

    def __repr__(self):
        return "<EventParticipant %r>" % self.id


class EventScore(db.Model):
    __table_args__ = (db.UniqueConstraint('event_judge_id', 'event_participant_id', 'criteria_id'),)
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False, default=0)
    # Relationship: Foreign Key
    event_judge_id = db.Column(db.Integer, db.ForeignKey('event_judge.id'), nullable=False)
    event_participant_id = db.Column(db.Integer, db.ForeignKey('event_participant.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('criteria.id'), nullable=False)
    # Timestamp
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, onupdate=dt.now)

    def __init__(self, score, event_judge_id, event_participant_id, criteria_id):
        self.score = score
        self.event_judge_id = event_judge_id
        self.event_participant_id = event_participant_id
        self.criteria_id = criteria_id

    def __repr__(self):
        return "<EventScore %r>" % self.id


if __name__ == "__main__":
    app.run()
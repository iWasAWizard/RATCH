from flask_login import UserMixin
from sqlalchemy import (
    Binary,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey
)

from app import db, login_manager
from app.base.utils import hash_pass


class Users(db.Model, UserMixin):
    """Table that stores user information, such as credentials"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32))
    password = Column(Binary)
    created = Column(DateTime)
    lastseen = Column(DateTime)
    notes = Column(Text)
    authentication_token = Column(String, unique=True, nullable=False)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # Password is stored in the database as a bytes object, so this gets that.

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.filter_by(user_id=user_id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class Classifications(db.Model):
    __tablename__ = 'classifications'

    classification_id = Column(Integer, primary_key=True)
    classification_name = Column(String(32), unique=True, nullable=False)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.classification_name)


class RequirementTypes(db.Model):
    __tablename__ = 'requirementtypes'

    type_id = Column(Integer, primary_key=True)
    type_name = Column(String(32), unique=True, nullable=False)
    type_description = Column(Text)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.type_name)


class Requirements(db.Model):
    __tablename__ = 'requirements'

    requirement_id = Column(Integer, primary_key=True)
    requirement_name = Column(String(32), unique=True, nullable=False)
    release_version = Column(String(64))
    requirement_description = Column(Text)
    parent_project = Column(Integer, ForeignKey('projects.project_id'))
    parent_requirement = Column(
        Integer, ForeignKey('requirements.requirement_id'))
    requirement_type = Column(Integer, ForeignKey('requirementtypes.type_id'))
    classification = Column(Integer, ForeignKey(
        'classifications.classification_id'))
    created = Column(DateTime)
    last_modified = Column(DateTime)
    last_modified_by = Column(Integer, ForeignKey('users.user_id'))
    created_by = Column(Integer, ForeignKey('users.user_id'))

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'classification':
                value = Classifications.query.filter_by(
                    classification_name=value).first().classification_id

            setattr(self, property, value)

    def __repr__(self):
        return str(self.requirement_name)


class TestCaseFormats(db.Model):
    __tablename__ = 'testcaseformats'

    format_id = Column(Integer, primary_key=True)
    format_name = Column(String(32), unique=True, nullable=True)
    format_description = Column(Text)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.format_name)


class TestCaseTypes(db.Model):
    __tablename__ = 'testcasetypes'

    case_type_id = Column(Integer, primary_key=True)
    case_type_name = Column(String(32), unique=True, nullable=False)
    case_type_description = Column(Text)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.case_type_name)


class TestCases(db.Model):
    __tablename__ = 'testcases'

    case_id = Column(Integer, primary_key=True)
    case_name = Column(String(64), unique=True, nullable=False)
    case_type = Column(Integer, ForeignKey('testcasetypes.case_type_id'))
    case_format = Column(Integer, ForeignKey('testcaseformats.format_id'))
    case_objective = Column(Text)
    case_overview = Column(Text)
    prerequisites = Column(Text)
    created = Column(DateTime)
    last_modified = Column(DateTime)
    last_modified_by = Column(Integer, ForeignKey('users.user_id'))
    created_by = Column(Integer, ForeignKey('users.user_id'))

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.case_name)


class TestStepTypes(db.Model):
    __tablename__ = 'teststeptypes'

    step_type_id = Column(Integer, primary_key=True)
    step_type_name = Column(String(32), unique=True, nullable=False)
    step_type_description = Column(Text)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.step_type_name)


class TestSteps(db.Model):
    __tablename__ = 'teststeps'

    step_id = Column(Integer, primary_key=True)
    procedure_text = Column(Text)
    verification_text = Column(Text)
    notes = Column(Text)
    test_case = Column(Integer, ForeignKey('testcases.case_id'))
    step_number = Column(Integer)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.step_id)


class Projects(db.Model):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(32), unique=True, nullable=False)
    project_description = Column(Text)
    project_welcome_message = Column(Text)
    classification = Column(Integer, ForeignKey(
        'classifications.classification_id'))
    created = Column(DateTime)
    last_modified = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.user_id'))

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'classification':
                value = Classifications.query.filter_by(
                    classification_name=value).first().classification_id

            setattr(self, property, value)

    def __repr__(self):
        return str(self.project_name)


class ReleaseVersions(db.Model):
    __tablename__ = 'releaseversions'

    project_id = Column(Integer, ForeignKey(
        'projects.project_id'), primary_key=True)
    release_version_name = Column(String(64), nullable=False, primary_key=True)
    release_version_description = Column(Text)

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.release_version_name)

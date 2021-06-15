# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, \
                       String, DateTime, Text, ForeignKey
from sqlalchemy.orm import synonym

from app import db, login_manager

from app.base.util import hash_pass


class Users(db.Model, UserMixin):

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

    id = synonym('user_id')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class Classifications(db.Model):

    __tablename__ = 'classifications'

    classification_id = Column(Integer, primary_key=True)
    classification_name = Column(String(32), unique=True, nullable=False)

    id = synonym('classification_id')

    def __repr__(self):
        return self.classification_name


class RequirementTypes(db.Model):

    __tablename__ = 'requirementtypes'

    type_id = Column(Integer, primary_key=True)
    type_name = Column(String(32), unique=True, nullable=False)
    type_description = Column(Text)

    id = synonym('type_id')

    def __repr__(self):
        return self.type_name


class Requirements(db.Model):

    __tablename__ = 'requirements'

    requirement_id = Column(Integer, primary_key=True)
    requirement_name = Column(String(32), unique=True, nullable=False)
    release_version = Column(String(64))
    requirement_description = Column(Text)
    parent_id = Column(Integer, ForeignKey('requirements.id'))
    requirement_type = Column(Integer, ForeignKey('requirementtypes.id'))
    classification = Column(Integer, ForeignKey('classifications.id'))
    created = Column(DateTime)
    last_modified = Column(DateTime)
    last_modified_by = Column(Integer, ForeignKey('users.id'))
    created_by = Column(Integer, ForeignKey('users.id'))

    id = synonym('requirement_id')

    def __repr__(self):
        return self.requirement_name


class TestCaseFormats(db.Model):

    __tablename__ = 'testcaseformats'

    format_id = Column(Integer, primary_key=True)
    format_name = Column(String(32), unique=True, nullable=True)
    format_description = Column(Text)

    id = synonym('format_id')

    def __repr__(self):
        return self.format_name


class TestCaseTypes(db.model):

    __tablename__ = 'testcasetypes'

    case_type_id = Column(Integer, primary_key=True)
    case_type_name = Column(String(32), unique=True, nullable=False)
    case_type_description = Column(Text)

    id = synonym('case_type_id')

    def __repr__(self):
        return self.case_type_name


class TestCases(db.Model):

    __tablename__ = 'testcases'

    case_id = Column(Integer, primary_key=True)
    case_name = Column(String(64), unique=True, nullable=False)
    case_type = Column(Integer, ForeignKey('testcasetypes.id'))
    case_format = Column(Integer, ForeignKey('testcaseformats.id'))
    case_objective = Column(Text)
    case_overview = Column(Text)
    prerequisites = Column(Text)
    created = Column(DateTime)
    last_modified = Column(DateTime)
    last_modified_by = Column(Integer, ForeignKey('users.id'))
    created_by = Column(Integer, ForeignKey('users.id'))

    id = synonym('case_id')

    def __repr__(self):
        return self.case_name


class TestStepTypes(db.Model):

    __tablename__ = 'teststeptypes'

    step_type_id = Column(Integer, primary_key=True)
    step_type_name = Column(String(32), unique=True, nullable=False)
    step_type_description = Column(Text)

    id = synonym('step_type_id')

    def __repr__(self):
        return self.step_type_name


class TestSteps(db.Model):

    __tablename__ = 'teststeps'

    step_id = Column(Integer, primary_key=True)
    procedure_text = Column(Text)
    verification_text = Column(Text)
    notes = Column(Text)
    test_case = Column(Integer, ForeignKey('testcases.id'))
    step_number = Column(Integer)

    id = synonym('step_id')

    def __repr__(self):
        return self.step_id


class Projects(db.Model):

    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(32), unique=True, nullable=False)
    project_description = Column(Text)
    project_welcome_message = Column(Text)
    classification = Column(Integer, ForeignKey('classifications.id'))
    created = Column(DateTime)
    last_modified = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'))

    id = synonym('project_id')

    def __repr__(self):
        return self.project_name

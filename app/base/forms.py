# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired
from app.base.models import (
    RequirementTypes,
    Classifications,
    Requirements,
    ReleaseVersions
)


# login and registration

class LoginForm(FlaskForm):
    username = TextField('Username', id='username_login',
                         validators=[DataRequired()])

    password = PasswordField('Password', id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create',
                         validators=[DataRequired()])

    email = TextField('Email', id='email_create',
                      validators=[DataRequired(), Email()])

    first_name = TextField('First Name', id='first_name_create',
                           validators=[DataRequired()])

    last_name = TextField('Last Name', id='last_name_create',
                          validators=[DataRequired()])

    password = PasswordField('Password', id='pwd_create',
                             validators=[DataRequired()])


class CreateProjectForm(FlaskForm):
    classification_choices = Classifications.get_classification_levels()

    project_name = TextField('Name', id='project_name',
                             validators=[DataRequired()])

    classification = SelectField(
        'Classification', id='classification', choices=classification_choices)

    project_description = TextAreaField('Project Description',
                                        id='project_description')

    project_welcome_message = TextAreaField('Project Welcome Message',
                                            id='project_welcome_message')


class CreateRequirementForm(FlaskForm):
    project_id = None
    parent_choices = Requirements.get_project_requirements(project_id)
    release_versions = ReleaseVersions.get_project_release_versions(project_id)
    type_choices = RequirementTypes.get_requirement_types()
    classification_choices = Classifications.get_classification_levels()

    requirement_type = SelectField(
        'Requirement Type', id='requirement_type', choices=type_choices)

    classification = SelectField(
        'Classification', id='classification', choices=classification_choices)

    parent_requirement = SelectField('Parent Requirement',
                                     id='parent_requirement',
                                     description='The parent requirement. Leave \
                                         blank to create a root requirement.',
                                     choices=parent_choices)

    requirement_name = TextField('Name', id='requirement_name',
                                 validators=[DataRequired()])

    release_version = SelectField(id='release_version',
                                  description='The project release version in \
                                      which this requirement is to be \
                                      implemented.',
                                  choices=release_versions)

    requirement_description = TextAreaField('Requirement Body',
                                            id='requirement_description',
                                            validators=[DataRequired()])


class CreateTestCaseForm(FlaskForm):
    pass



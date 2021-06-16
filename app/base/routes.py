# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import (
    LoginForm,
    CreateAccountForm,
    CreateProjectForm,
    CreateRequirementForm,
    CreateTestCaseForm
)
from app.base.models import Users, Projects, Requirements, TestCases, ReleaseVersions

from app.base.util import verify_pass, create_api_authentication_token


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Incorrect user or password.',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(created=datetime.utcnow(),
                     lastseen=datetime.utcnow(),
                     authentication_token=create_api_authentication_token(),
                     **request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created! Please <a href="/login">login</a>.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html',
                               form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/create/project', methods=['GET', 'POST'])
def create_project():
    create_project_form = CreateProjectForm(request.form)
    if 'create' in request.form:

        project_name = request.form['project_name']

        # Check if project exists.
        project = Projects.query.filter_by(project_name=project_name).first()
        if project:
            return render_template('projects/create.html',
                                   msg="A project with that name already \
                                       exists.",
                                   success=False, form=create_project_form)

        # Else create the project.
        project = Projects(created=datetime.utcnow(),
                           last_modified=datetime.utcnow(),
                           created_by=current_user.user_id,
                           **request.form)

        db.session.add(project)
        db.session.commit()

        return render_template('projects/create.html',
                               msg='Project created!',
                               success=True,
                               form=create_project_form)

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    else:
        return render_template('projects/create.html',
                               form=create_project_form)


@blueprint.route('/<project_id>/create/requirement/', methods=['GET', 'POST'])
def create_requirement(project_id):
    create_requirement_form = CreateRequirementForm(request.form)
    create_requirement_form.project_id = project_id

    project = Projects.query.filter_by(project_id=project_id).first()
    if not project:
        return render_template('not-found.html', msg=f"Project with ID \
            '{project_id}' not found!")

    if 'create' in request.form:

        requirement_name = request.form['requirement_name']

        # Check if a requirement with that name already exists.
        requirement = Requirements.query.filter_by(parent_project=project_id,
                                                   requirement_name=requirement_name).first()

        if requirement:
            return render_template('requirements/create.html',
                                   msg="A requirement with that name already \
                                       exists in this project.",
                                   success=False, form=create_requirement_form)

        # Else create the requirement
        requirement = Requirements(created=datetime.utcnow(),
                                   last_modified=datetime.utcnow(),
                                   created_by=current_user.user_id,
                                   last_modified_by=current_user.user_id,
                                   parent_project=project_id,
                                   **request.form)

        db.session.add(requirement)
        db.session.commit()

        return render_template('requirements/create.html',
                               msg='Requirement created!',
                               success=True,
                               form=create_requirement_form)

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    else:
        return render_template('requirements/create.html',
                               form=create_requirement_form)

# Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500

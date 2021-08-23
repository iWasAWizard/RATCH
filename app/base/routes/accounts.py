from datetime import datetime
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from app.database import db
from app.base import blueprint
from app.base.forms.accounts import LoginForm, CreateAccountForm
from app.database.models import Users

from app.base.login_manager import verify_pass, create_api_authentication_token


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # Read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user in Users table
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            # Update the current user's last_seen time
            user.last_seen = datetime.utcnow()
            db.session.commit()

            login_user(user)

            return redirect(url_for('base_blueprint.route_default'))

        # Either the username or password is incorrect.
        return render_template('accounts/login.html',
                               msg='Incorrect user or password.',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)

    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route"""
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check if username exists in Users table
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check if email address exists in Users table
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # Create the new user
        user = Users(created=datetime.utcnow(),
                     last_seen=datetime.utcnow(),
                     authentication_token=create_api_authentication_token(),
                     **request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created! \
                                   Please <a href="/login">login</a>.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html',
                               form=create_account_form)


@blueprint.route('/logout')
def logout():
    """Route to log the current user out"""
    logout_user()
    return redirect(url_for('base_blueprint.login'))

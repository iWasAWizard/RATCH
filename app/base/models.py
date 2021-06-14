# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, DateTime, Table
from sqlalchemy.orm import synonym

from app import db, login_manager

from app.base.util import hash_pass


class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    user_id    = Column(Integer, primary_key=True)
    username   = Column(String(32), unique=True, nullable=False)
    email      = Column(String(64), unique=True, nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name  = Column(String(32))
    password   = Column(Binary)
    created    = Column(DateTime)
    lastseen   = Column(DateTime)
    notes      = Column(String)

    id         = synonym('user_id')

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

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
import app.api as api_routes
import app.home.routes as home_routes
import app.base.routes as base_routes

# from logging import basicConfig, DEBUG, getLogger, StreamHandler

db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module in home_routes.__all__:
        bp = import_module(f'app.home.routes.{module}')
        app.register_blueprint(bp.blueprint)

    for module in base_routes.__all__:
        bp = import_module(f'app.base.routes.{module}')
        app.register_blueprint(bp.blueprint)

    app.register_blueprint(api_routes.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.reflect(bind='__all__', app=None)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    configure_database(app)
    register_extensions(app)
    register_blueprints(app)
    return app

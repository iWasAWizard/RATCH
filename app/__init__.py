from flask import Flask
from importlib import import_module
from app.base.database import db
from app.base.login_manager import login_manager
import app.home.routes as home_routes
import app.base.routes as base_routes
from app import base, home
import app.base.api as api


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

    app.register_blueprint(api.blueprint)


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

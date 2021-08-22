from flask import Flask, Blueprint
from flask_restful import Api
from importlib import import_module
from app.database import db
from app.base.login_manager import login_manager
import app.home.routes as home_routes
import app.base.routes as base_routes
from app import base, home
import app.base.api as api


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.reflect(bind='__all__', app=None)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_routes(app):
    for module in home_routes.__all__:
        bp = import_module(f'app.home.routes.{module}')
        app.register_blueprint(bp.blueprint)

    for module in base_routes.__all__:
        bp = import_module(f'app.base.routes.{module}')
        app.register_blueprint(bp.blueprint)


def initialize_api(app):
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    rest_api = Api(api_bp)

    rest_api.add_resource(api.UserApi, '/users/<string:username>')
    rest_api.add_resource(api.UsersApi, '/users')
    rest_api.add_resource(api.ProjectApi, '/projects/<string:project_name>')
    rest_api.add_resource(api.ProjectsApi, '/projects')

    app.register_blueprint(api_bp)


def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    configure_database(app)
    register_extensions(app)
    register_routes(app)
    initialize_api(app)
    return app

from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint(
    'api_blueprint',
    __name__,
    url_prefix='/api'
)
api = Api(blueprint)

from . import routes

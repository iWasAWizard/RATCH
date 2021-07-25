from app.base.models import Projects, Users
from flask_restful import Resource, Api
from flask import Blueprint

blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api')
rest_api = Api(blueprint)


class Project(Resource):
    def get(self, project_name):
        return Projects.query.filter_by(project_name=project_name).first().with_entities(Projects.project_id,
                                                                                         Projects.project_name,
                                                                                         Projects.created_by,
                                                                                         Projects.classification,
                                                                                         Projects.created,
                                                                                         Projects.last_modified)


class User(Resource):
    def get(self, username):
        return Users.query.filter_by(username=username).first().with_entities(Users.user_id,
                                                                              Users.username,
                                                                              Users.created,
                                                                              Users.lastseen)


rest_api.add_resource(User, '/users/<string:username>')
rest_api.add_resource(Project, '/projects/<string:project_name>')

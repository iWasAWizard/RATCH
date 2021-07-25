# from app.base.models import Projects, Users
from . import api
from flask_restful import Resource


class Project(Resource):
    def get(self, project_name):
        # return Projects.query.filter_by(project_name=project_name).first().with_entities(Projects.project_id,
        #                                                                                  Projects.project_name,
        #                                                                                  Projects.created_by,
        #                                                                                  Projects.classification,
        #                                                                                  Projects.created,
        #                                                                                  Projects.last_modified)
        pass

class User(Resource):
    def get(self, username):
        # return Users.query.filter_by(username=username).first().with_entities(Users.user_id,
        #                                                                       Users.username,
        #                                                                       Users.created,
        #                                                                       Users.lastseen)
        pass

api.add_resource(User, '/users/<string:username>')
api.add_resource(Project, '/projects/<string:project_name>')

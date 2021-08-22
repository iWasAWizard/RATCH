from app.database.models import Projects, Users
from flask_restful import Resource


class ProjectApi(Resource):
    def get(self, project_name):
        p = Projects()
        return p.to_dict(project_name=project_name)


class ProjectsApi(Resource):
    def get(self):
        p = Projects()
        return p.to_dict()


class UserApi(Resource):
    def get(self, username):
        u = Users()
        return u.to_dict(username=username)


class UsersApi(Resource):
    def get(self):
        u = Users()
        return u.to_dict()

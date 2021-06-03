from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from RATCH.db import Database
import psycopg2

database = Database(host='postgres')
database.init()

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('text')
parser.add_argument('type')
parser.add_argument('user')
parser.add_argument('first_name')
parser.add_argument('last_name')
parser.add_argument('email')
parser.add_argument('username')
parser.add_argument('password')


class requirement(Resource):
    def get(self):
        return database.query("""SELECT * FROM Requirements""")

    def post(self):
        args = parser.parse_args()
        cur = database.cursor()
        cur.execute("""INSERT INTO Requirements(requirement_name,
                                              requirement_description,
                                              type,
                                              last_modified_by,
                                              created_by)
                                              VALUES (%s, %s, %s, %s, %s)""",
                    (args['name'],
                     args['text'],
                     args['type'],
                     args['user'],
                     args['user']))
        try:
            database.conn.commit()
        except psycopg2.Error as e:
            return f"PostgreSQL Error: {e}"
        cur.close()
        return database.query("""SELECT * FROM Requirements""")


class user(Resource):
    def get(self):
        return database.query("""SELECT user_id,
                                 username,
                                 first_name,
                                 last_name,
                                 email
                                 FROM Users""")

    def post(self):
        args = parser.parse_args()
        cur = database.cursor()
        cur.execute("""INSERT INTO Users (first_name,
                                          last_name,
                                          email,
                                          username,
                                          password)
                                          VALUES (%s, %s, %s, %s, %s)""",
                    (args['first_name'],
                     args['last_name'],
                     args['email'],
                     args['username'],
                     args['password']))
        try:
            database.conn.commit()
        except psycopg2.Error as e:
            return f"PostgreSQL Error: {e}"
        cur.close()
        return database.query("""SELECT
                                 user_id,
                                 username,
                                 first_name,
                                 last_name,
                                 email
                                 FROM Users""")


class project(Resource):
    def get(self):
        return database.query("""SELECT * FROM Projects""")

    def post(self):
        args = parser.parse_args()
        cur = database.cursor()
        cur.execute("""INSERT INTO Projects (project_name,
                                             project_description)
                                             VALUES (%s, %s)""",
                    (args['name'],
                     args['text']))
        try:
            database.conn.commit()
        except psycopg2.Error as e:
            return f"PostgreSQL Error: {e}"
        cur.close()
        return database.query("""SELECT * FROM Projects""")


api.add_resource(requirement, '/requirements/')
api.add_resource(user, '/users/')
api.add_resource(project, '/projects')

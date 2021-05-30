from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
import database as db

app = Flask(__name__)
api = Api(app)

requirements = {}
testcases = {}
users = {}
projects = {}

database = db.Database(host='postgres')
database.init()

@app.route('/')
def index():
    return render_template('index.html')

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('text')
parser.add_argument('type')
parser.add_argument('user')

class requirement(Resource):
    def get(self):
        cur = database.cursor()
        cur.execute("""SELECT * FROM Requirements""")
        return cur.fetchall()

    def post(self):
        args = parser.parse_args()
        cur = database.cursor()
        cur.execute("""INSERT INTO Requirements (requirement_name, requirement_description, type, last_modified_by, created_by) VALUES (%s, %s, %s, %s, %s)""",
                   (args['name'], args['text'], args['type'], args['user'], args['user']))
        database.conn.commit()
        cur.execute("""SELECT * FROM Requirements""")
        return cur.fetchall()


api.add_resource(requirement, '/api/requirement/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

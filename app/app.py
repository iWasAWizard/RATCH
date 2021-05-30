from flask import Flask, request, render_template
from flask_restful import Api, Resource
import database as db

app = Flask(__name__)
api = Api(app)

requirements = {}
testcases = {}
users = {}
projects = {}

database = db.Database('postgres')
database.connect()


@app.route('/')
def index():
    return render_template('index.html')


class Requirement(Resource):
    def get(self, requirement_id):
        return {requirement_id: requirements[requirement_id]}

    def put(self, requirement_id):
        requirements[requirement_id] = request.form['data']
        return {requirement_id: requirements[requirement_id]}


api.add_resource(Requirement, '/api/requirements/<int:requirement_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

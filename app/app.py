from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

requirements = {}
testcases = {}
users = {}
projects = {}

@app.route('/')
def hello_world():
    return "Hello, world!"

class Requirement(Resource):
    def get(self, requirement_id):
        return {requirement_id: requirements[requirement_id]}
    def put(self, requirement_id):
        requirements[requirement_id] = request.form['data']
        return {requirement_id: requirements[requirement_id]}

api.add_resource(Requirement, '/api/requirements/<integer:requirement_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

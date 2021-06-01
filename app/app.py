from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
import database as db
import psycopg2
import hashlib

app = Flask(__name__)
api = Api(app)

requirements = {}
testcases = {}
users = {}
projects = {}

database = db.Database(host='postgres')
database.init()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("register.html", t_message="Register Here")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    firstname = request.form.get("firstname", "")
    lastname = request.form.get("lastname", "")
    email = request.form.get("email", "")

    # Check for user name field is empty
    if username == "":
        t_message = "Register - empty field: Please provide a username."
        # Send user back to the dynamic html page (template), with a message
        return render_template("register.html", t_message=t_message)

    if password == "":
        t_message = "Register - empty field: Please provide a password."
        return render_template("register.html", t_message=t_message)

    if firstname == "":
        t_message = "Register - empty field: Please provide a first name."
        return render_template("register.html", t_message=t_message)

    if lastname == "":
        t_message = "Register - empty field: Please provide a last name."
        return render_template("register.html", t_message=t_message)

    if email == "":
        t_message = "Register - empty field: Please provide an email address."
        return render_template("register.html", t_message=t_message)

    # Hash the password they entered into a encrypted hex string
    hashed = hashlib.sha256(password.encode())
    password = hashed.hexdigest()

    cur = database.cursor()
    cur.execute("""INSERT INTO Users (first_name,
                                      last_name,
                                      email,
                                      username,
                                      password)
                                      VALUES (%s, %s, %s, %s, %s)""",
                firstname,
                lastname,
                email,
                username,
                password)
    try:
        database.conn.commit()
        return "Registration successful!"
    except psycopg2.Error as e:
        t_message = "Database error: " + e
    cur.close()
    
    if username in database.query("""SELECT * FROM Users"""):
        t_message = "Registration successful!"
        return render_template("register.html", t_message=t_message)


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


api.add_resource(requirement, '/api/requirements/')
api.add_resource(user, '/api/users/')
api.add_resource(project, '/api/projects')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

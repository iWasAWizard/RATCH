from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from RATCH.db import Database
import psycopg2
import functools

database = Database(host='postgres')
database.init()

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("auth/register.html", t_message="Register Here")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    firstname = request.form.get("firstname", "")
    lastname = request.form.get("lastname", "")
    email = request.form.get("email", "")

    error = None

    # Check for user name field is empty
    if username == "":
        error = "Register - empty field: Please provide a username."

    user = database.query('SELECT id FROM user WHERE username = ?')
    user.fetchone()
    if user is not None:
        error = f"User {username} is already registered."

    if password == "":
        error = "Register - empty field: Please provide a password."

    if firstname == "":
        error = "Register - empty field: Please provide a first name."

    if lastname == "":
        error = "Register - empty field: Please provide a last name."

    if email == "":
        error = "Register - empty field: Please provide an email address."

    # Hash the password they entered into a encrypted hex string
    password = generate_password_hash(password=password, salt_length=8)

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

    if error is None:
        try:
            database.conn.commit()
            if username in database.query("""SELECT * FROM Users"""):
                return redirect(url_for('login'))
        except psycopg2.Error as e:
            error = "Database error: " + e
            return error
        cur.close()
    else:
        return error


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = database.query(
            'SELECT * FROM user WHERE username = ?'
        )
        user.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        elif username is None:
            error = 'Please enter a username.'
        elif password is None:
            error = 'Please enter a password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = database.execute(
            'SELECT * FROM user WHERE user_id = ?')
        g.user.fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

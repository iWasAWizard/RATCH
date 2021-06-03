from flask import Flask, render_template
from RATCH import auth, db, rest_api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SECRET_KEY='develop')

    database = db.Database(host='postgres')
    database.init()

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/', methods=['POST', 'GET'])
    def index():
        return render_template('webapp/index.html')

    app.register_blueprint(auth.bp)
    app.register_blueprint(rest_api.bp)

    return app

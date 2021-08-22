from flask import redirect, url_for

from app.base import blueprint


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

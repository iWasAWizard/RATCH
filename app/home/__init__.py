from flask import Blueprint

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

__all__ = ["blueprint", "routes"]

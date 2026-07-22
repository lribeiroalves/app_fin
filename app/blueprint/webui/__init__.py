from flask import Blueprint
from .views import index
from app import get_base_path
import os

base_path = get_base_path()

bp = Blueprint('webui', __name__, static_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'static'), template_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'templates'), static_url_path='/webui/static')


# URLs
bp.add_url_rule('/', view_func=index)


def init_app(app):
    app.register_blueprint(bp)
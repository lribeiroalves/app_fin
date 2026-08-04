from flask import Blueprint
from .views import index, users, bancos
from app import get_base_path
import os
from datetime import datetime

base_path = get_base_path()

bp = Blueprint('webui', __name__, static_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'static'), template_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'templates'), static_url_path='/webui/static')


# URLs
bp.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
bp.add_url_rule('/users', view_func=users)
bp.add_url_rule('/bancos', view_func=bancos)


def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.globals['datetime'] = datetime
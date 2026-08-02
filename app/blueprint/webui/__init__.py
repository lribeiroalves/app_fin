from flask import Blueprint
from .views import index, users, bancos, form_index, form_entrada
from app import get_base_path
import os
from datetime import datetime

base_path = get_base_path()

bp = Blueprint('webui', __name__, static_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'static'), template_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'templates'), static_url_path='/webui/static')


# URLs
bp.add_url_rule('/', view_func=index)
bp.add_url_rule('/users', view_func=users)
bp.add_url_rule('/bancos', view_func=bancos)
bp.add_url_rule('/form-index', view_func=form_index, methods=['POST'])
bp.add_url_rule('/form-entrada', view_func=form_entrada, methods=['POST'])


def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.globals['datetime'] = datetime
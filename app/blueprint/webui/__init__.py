from flask import Blueprint
from .views import index, users, bancos, form_filtro, form_transaction, form_saldo, form_banco, config
from app import get_base_path
import os
from datetime import datetime

base_path = get_base_path()

bp = Blueprint('webui', __name__, static_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'static'), template_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'templates'), static_url_path='/webui/static')


# URLs
bp.add_url_rule('/', view_func=index, methods=['GET'])
bp.add_url_rule('/form-filtro', view_func=form_filtro, methods=['POST'])
bp.add_url_rule('/form-transaction', view_func=form_transaction, methods=['POST'])
bp.add_url_rule('/form-saldo', view_func=form_saldo, methods=['POST'])
bp.add_url_rule('/form-banco', view_func=form_banco, methods=['POST'])
bp.add_url_rule('/users', view_func=users)
bp.add_url_rule('/bancos', view_func=bancos)
bp.add_url_rule('/config', view_func=config)


def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.globals['datetime'] = datetime
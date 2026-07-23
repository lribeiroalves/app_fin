from flask import Flask, jsonify
import os
import sys
from pathlib import Path
from .ext import configuration
from .ext.database import db
from .ext.database.models import Users, Bancos


def get_base_path():
    if getattr(sys, 'frozen', False):
        # se o app estiver rodando pelo .exe ele criar o atributo frozen
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_path(base_path):
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).resolve().parent / 'data'
    else:
        base_dir = Path(base_path) / 'instance'

    base_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{base_dir / 'database.db'}"


def populate_db(app:Flask):
    with app.app_context():
        if not db.session.query(Users).first():
            default_users = ['Sandra', 'Samantha', 'Mercedes']
            for nome in default_users:
                if not db.session.query(Users).filter_by(nome=nome).first():
                    db.session.add(Users(nome=nome))
            db.session.commit()
        if not db.session.query(Bancos).first():
            default_bancos = ['Nubank', 'Mercado Pago', 'Sofisa', 'Banco do Brasil']
            for banco in default_bancos:
                if not db.session.scalars(db.select(Bancos).where(Bancos.nome == banco)).first():
                    db.session.add(Bancos(nome=banco))
                db.session.commit()


def create_app():
    base_path = get_base_path()

    template_dir = os.path.join(base_path, 'app', 'templates')
    static_dir = os.path.join(base_path, 'app', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Salva o diretorio base e o caminho absoluto do armazenamento do banco de dados nas configs do app
    app.config['APP_BASE_PATH'] = base_path
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_path(base_path)

    configuration.init_app(app)

    # Popula a base de dados com os dados default
    populate_db(app)

    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({
            'error': 'Bad Request',
            'message': error.description
        })
        response.status_code = 400
        return response
    
    return app

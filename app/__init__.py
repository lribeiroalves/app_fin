from flask import Flask, jsonify
import os
import sys
from pathlib import Path
from .ext import configuration
from .ext.database import db, init_app as init_database_app
from .ext.database.models import Users


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


def create_app():
    base_path = get_base_path()

    template_dir = os.path.join(base_path, 'app', 'templates')
    static_dir = os.path.join(base_path, 'app', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_path(base_path)
    configuration.init_app(app, base_path)

    init_database_app(app)

    with app.app_context():
        db.create_all()
        if not db.session.query(Users).first():
            default_users = ['Sandra', 'Samantha', 'Mercedes']
            for nome in default_users:
                if not db.session.query(Users).filter_by(nome=nome).first():
                    db.session.add(Users(nome=nome))
            db.session.commit()

    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({
            'error': 'Bad Request',
            'message': error.description
        })
        response.status_code = 400
        return response
    
    get_base_path()
    
    return app

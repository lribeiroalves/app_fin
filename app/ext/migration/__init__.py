from flask_migrate import Migrate, upgrade as migrate_upgrade
from app.ext.database import db
from app.ext.database.models import *
import os
from flask import Flask


def init_app(app:Flask):
    migrations_dir = os.path.join(app.config['APP_BASE_PATH'], 'migrations')

    migrate = Migrate(app, db, directory=migrations_dir)

    with app.app_context():
        try:
            migrate_upgrade(directory=migrations_dir)
            print("Migrações aplicadas com sucesso.")
        except Exception as e:
            print(f'Erro ao aplicar migrações: {e}')

from flask_migrate import Migrate
from app.ext.database import db
from app.ext.database.models import *


def init_app(app):
    migrate = Migrate(app, db)

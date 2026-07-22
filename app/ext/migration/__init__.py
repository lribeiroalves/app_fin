try:
    from flask_migrate import Migrate
except ImportError:
    Migrate = None

from app.ext.database import db
from app.ext.database.models import *


def init_app(app):
    if Migrate is None:
        return

    Migrate(app, db)

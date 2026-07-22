from dynaconf import FlaskDynaconf
import os
from flask import Flask


def init_app(app:Flask):
    base_path = app.config['APP_BASE_PATH']
    config_path = os.path.join(base_path, 'config', 'settings.toml')
    secrets_path = os.path.join(base_path, 'config', 'secrets.toml')
    FlaskDynaconf(app=app, settings_files=[config_path, secrets_path], extensions_list='EXTENSIONS')
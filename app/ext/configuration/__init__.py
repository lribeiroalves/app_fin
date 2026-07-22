from dynaconf import FlaskDynaconf
import os


def init_app(app, base_path):
    config_path = os.path.join(base_path, 'config', 'settings.toml')
    secrets_path = os.path.join(base_path, 'config', 'secrets.toml')
    FlaskDynaconf(app=app, settings_files=[config_path, secrets_path], extensions_list='EXTENSIONS')
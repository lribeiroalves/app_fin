from dynaconf import FlaskDynaconf
import os
import sys
from pathlib import Path


def init_app(app, base_path):
    base_dir = Path(base_path)
    config_path = base_dir / 'config' / 'settings.toml'
    secrets_path = base_dir / 'config' / 'secrets.toml'

    if not config_path.exists() or not secrets_path.exists():
        fallback_dir = Path(sys.executable).resolve().parent
        config_path = fallback_dir / 'config' / 'settings.toml'
        secrets_path = fallback_dir / 'config' / 'secrets.toml'

    if not config_path.exists() or not secrets_path.exists():
        raise FileNotFoundError(f'Config files not found. Expected {config_path} and {secrets_path}')

    app.config.setdefault('ENV', 'production')
    FlaskDynaconf(app=app, settings_files=[str(config_path), str(secrets_path)], extensions_list='EXTENSIONS')
from dynaconf import FlaskDynaconf
import os
import sys
from pathlib import Path


def _resolve_config_paths(base_path):
    candidates = []

    base_dir = Path(base_path)
    candidates.append(base_dir / 'config')

    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).resolve().parent
        candidates.append(exe_dir / 'config')
        candidates.append(exe_dir)
        candidates.append(base_dir)

    for candidate in candidates:
        config_path = candidate / 'settings.toml'
        secrets_path = candidate / 'secrets.toml'
        if config_path.exists() and secrets_path.exists():
            return str(config_path), str(secrets_path)

    return None, None


def init_app(app, base_path):
    config_path, secrets_path = _resolve_config_paths(base_path)

    if not config_path or not secrets_path:
        app.config.setdefault('ENV', 'production')
        return

    app.config.setdefault('ENV', 'production')
    FlaskDynaconf(app=app, settings_files=[config_path, secrets_path], extensions_list='EXTENSIONS')
from .users import seed_users


def init_app(app):
    env_name = app.config.get('ENV', 'production')
    if env_name == 'development':
        for command in [seed_users]:
            app.cli.add_command(command)
from .users import seed_users

def init_app(app):
    if app.config['ENV'] == 'development':
        for command in [seed_users]:
           app.cli.add_command(command)
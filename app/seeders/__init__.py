from .users import seed_users
from .bancos import seed_bancos
from .transacoes import seed_transacoes

def init_app(app):
    if app.config['ENV'] == 'development':
        for command in [seed_users, seed_bancos, seed_transacoes]:
           app.cli.add_command(command)
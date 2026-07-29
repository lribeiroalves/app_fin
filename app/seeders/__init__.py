from .users import seed_users
from .bancos import seed_bancos
from .transacoes import seed_transacoes
from .saldos import seed_saldos

def init_app(app):
    if app.config['ENV'] == 'development':
        for command in [seed_users, seed_bancos, seed_transacoes, seed_saldos]:
           app.cli.add_command(command)
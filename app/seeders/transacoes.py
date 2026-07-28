import click
from app.ext.database import db
from app.ext.database.models import Transacoes, Users

@click.command('seed-transacoes')
def seed_transacoes():
    transacoes = [
        {'tipo': 'ENTRADA', 'ano': 2026, 'mes': 1, 'descricao': 'Salário', 'valor': 3000, 'user_id': 1},
        {'tipo': 'SAIDA', 'ano': 2026, 'mes': 1, 'descricao': 'LUZ', 'valor': 500, 'user_id': 3}
    ]

    add = 0
    n_add = 0

    for t in transacoes:
        if not db.session.query(Transacoes).filter_by(descricao=t['descricao']).first():
            transacao = Transacoes(tipo=t['tipo'], ano=t['ano'], mes=t['mes'], descricao=t['descricao'], valor=t['valor'], user_id=t['user_id'])
            db.session.add(transacao)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    click.echo(f'{add} Transacoes adicionadas. {n_add} Transacoes ja existiam')

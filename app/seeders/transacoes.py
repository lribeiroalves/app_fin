import click
from app.ext.database import db
from app.ext.database.models import Transacoes

@click.command('seed-transacoes')
def seed_transacoes():
    transacoes = [
        {'tipo': 'ENTRADA', 'ano': 2026, 'mes': 1, 'descricao': 'Salário', 'valor': 3000, 'user_id': 1},
        {'tipo': 'SAIDA', 'ano': 2026, 'mes': 1, 'descricao': 'LUZ', 'valor': 500, 'user_id': 3},
        {'tipo': 'SAIDA', 'ano': 2026, 'mes': 1, 'descricao': 'Água', 'valor': 250, 'user_id': 2},
        {'tipo': 'SAIDA', 'ano': 2026, 'mes': 1, 'descricao': 'Conta1', 'valor': 5000, 'user_id': 1},
        {'tipo': 'SAIDA', 'ano': 2026, 'mes': 1, 'descricao': 'Conta2', 'valor': 50, 'user_id': 3},
        {'tipo': 'ENTRADA', 'ano': 2026, 'mes': 1, 'descricao': 'Entrada1', 'valor': 4000, 'user_id': 2},
        {'tipo': 'ENTRADA', 'ano': 2026, 'mes': 1, 'descricao': 'Entrada3', 'valor': 1000, 'user_id': 3},
        {'tipo': 'ENTRADA', 'ano': 2026, 'mes': 1, 'descricao': 'Entrada4', 'valor': 400, 'user_id': 1},
        {'tipo': 'ENTRADA', 'ano': 2026, 'mes': 1, 'descricao': 'Entrada2', 'valor': 8000, 'user_id': 2},
    ]

    add = 0
    n_add = 0

    for t in transacoes:
        if not db.session.query(Transacoes).filter(Transacoes.descricao == t['descricao'], Transacoes.valor == t['valor'], Transacoes.ano == t['ano'], Transacoes.mes == t['mes']).first():
            transacao = Transacoes(tipo=t['tipo'], ano=t['ano'], mes=t['mes'], descricao=t['descricao'], valor=t['valor'], user_id=t['user_id'])
            db.session.add(transacao)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    click.echo(f'{add} Transacoes adicionadas. {n_add} Transacoes ja existiam')

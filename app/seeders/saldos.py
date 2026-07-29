import click
from app.ext.database import db
from app.ext.database.models import Saldos

@click.command('seed-saldos')
def seed_saldos():
    saldos = [
        {'ano': 2026, 'mes': 1, 'saldo': 1500, 'user_id': 1, 'banco_id': 1},
        {'ano': 2026, 'mes': 1, 'saldo': 2300, 'user_id': 1, 'banco_id': 2},
        {'ano': 2026, 'mes': 1, 'saldo': 5000, 'user_id': 2, 'banco_id': 1},
        {'ano': 2026, 'mes': 1, 'saldo': 1500, 'user_id': 3, 'banco_id': 3},
        {'ano': 2026, 'mes': 1, 'saldo': 3611, 'user_id': 3, 'banco_id': 4},
        {'ano': 2026, 'mes': 1, 'saldo': 147, 'user_id': 2, 'banco_id': 4}
    ]

    add = 0
    n_add = 0

    for s in saldos:
        if not db.session.query(Saldos).filter(Saldos.ano == s['ano'], Saldos.mes == s['mes'], Saldos.saldo == s['saldo'], Saldos.user_id == s['user_id'], Saldos.banco_id == s['banco_id']).first():
            saldo = Saldos(ano=s['ano'], mes=s['mes'], saldo=s['saldo'], user_id=s['user_id'], banco_id=s['banco_id'])
            db.session.add(saldo)
            add += 1
        else:
            n_add += 1


    db.session.commit()
    click.echo(f'{add} Transacoes adicionadas. {n_add} Transacoes ja existiam')
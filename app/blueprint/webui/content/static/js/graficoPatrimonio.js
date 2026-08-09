$(document).ready( function () {

});

bancos = sorted(set([saldo.banco.nome for saldo in saldos]))
            saldos_por_banco = {}
            for banco in bancos:
                color = [random.randint(0, 255) for _ in range(3)]
                saldos_por_banco[banco] = {
                    'label': banco,
                    'data': [],
                    'backgroundColor': f"rgba({color[0]}, {color[1]}, {color[2]}, 0.6)",
                    'borderColor': f"rgba({color[0]}, {color[1]}, {color[2]}, 1)"
                }



meses[str(saldo.mes)][2][saldo.banco.nome] = meses[str(saldo.mes)][2].get(saldo.banco.nome, 0) + float(saldo.saldo)


{'1': ['Jan', 3800.0, {'Nubank': 1500.0, 'Mercado Pago': 2300.0}], '2': ['Fev', 8850.54, {'Nubank': 8000.0, 'Banco do Brasil': 850.54}], '3': ['Mar', 900.0, {'Sofisa': 900.0}]}

{'Banco do Brasil': {'label': 'Banco do Brasil', 'data': [None, None, None], 'backgroundColor': 'rgba(130, 171, 79, 0.6)', 'borderColor': 'rgba(130, 171, 79, 1)'}, 'Mercado Pago': {'label': 'Mercado Pago', 'data': [None, None, None], 'backgroundColor': 'rgba(85, 70, 210, 0.6)', 'borderColor': 'rgba(85, 70, 210, 1)'}, 'Nubank': {'label': 'Nubank', 'data': [None, None, None], 'backgroundColor': 'rgba(211, 148, 69, 0.6)', 'borderColor': 'rgba(211, 148, 69, 1)'}, 'Sofisa': {'label': 'Sofisa', 'data': [None, None, None], 'backgroundColor': 'rgba(35, 88, 60, 0.6)', 'borderColor': 'rgba(35, 88, 60, 1)'}}

('Nubank', 1500.0)
('Mercado Pago', 2300.0)
('Nubank', 8000.0)
('Banco do Brasil', 850.54)
('Sofisa', 900.0)
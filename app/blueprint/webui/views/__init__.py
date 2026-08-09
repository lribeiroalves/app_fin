from flask import render_template, abort, redirect, url_for, jsonify, flash, request
from app.ext.database import db
from app.ext.database.models import *
from .forms import FiltrosForm, NovaTransacaoForm, NovoSaldoForm, FormBanco, FormEditBanco, FormEditTransacao, FormEditSaldo
from collections import defaultdict
import random


def consulta_banco(user=1, ano=1, mes=1) -> dict:
    try:
        entradas = db.session.scalars(db.select(Transacoes).where(Transacoes.ano == int(ano), Transacoes.mes == int(mes), Transacoes.user_id == int(user), Transacoes.tipo == 'ENTRADA')).all()
        saidas = db.session.scalars(db.select(Transacoes).where(Transacoes.ano == int(ano), Transacoes.mes == int(mes), Transacoes.user_id == int(user), Transacoes.tipo == 'SAIDA')).all()
        saldos = db.session.scalars(db.select(Saldos).where(Saldos.ano == int(ano), Saldos.mes == int(mes), Saldos.user_id == int(user))).all()

        ano_ant = int(ano)
        mes_ant = int(mes) - 1
        if not mes_ant:
            mes_ant = 12
            ano_ant -= 1

        saldos_ant = db.session.scalars(db.select(Saldos).where(Saldos.ano == ano_ant, Saldos.mes == mes_ant, Saldos.user_id == int(user))).all()

        total_entradas = 0
        total_saidas = 0
        total_saldos = 0
        total_saldos_ant = 0 

        if entradas:
            total_entradas = sum(entrada.valor for entrada in entradas)
        if saidas:
            total_saidas = sum(saida.valor for saida in saidas)
        if saldos:
            total_saldos = sum(saldo.saldo for saldo in saldos)
        if saldos_ant:
            total_saldos_ant = sum(saldo.saldo for saldo in saldos_ant)

        # graficos
        labels_resultado = ['Entradas', 'Saidas']
        values_resultado = [total_entradas, total_saidas]
        labels_saldos = ['Mês Passado', 'Mês Atual']
        values_saldos = [total_saldos_ant, total_saldos]
    except:
        return None

    return {
        'entrada': entradas,
        'saida': saidas,
        'saldo': saldos,
        'total_entrada': total_entradas,
        'total_saida': total_saidas,
        'total_saldo': total_saldos,
        'total_saldo_ant': total_saldos_ant,
        'labels_resultado': labels_resultado,
        'values_resultado': values_resultado,
        'labels_saldo': labels_saldos,
        'values_saldo': values_saldos
    }


def index():
    form = FiltrosForm()
    form_transacao = NovaTransacaoForm()
    form_saldo = NovoSaldoForm()
    form_edit_transacao = FormEditTransacao()
    form_edit_saldo = FormEditSaldo()

    user_arg = request.args.get('user', type=int)
    ano_arg = request.args.get('ano', type=int)
    mes_arg = request.args.get('mes', type=int)
    aba_ativa = request.args.get('aba_ativa')

    if user_arg and ano_arg and mes_arg:
        dados = consulta_banco(user_arg, ano_arg, mes_arg)
        if request.method == 'GET':
            form.user.data = str(user_arg)
            form.ano.data = str(ano_arg)
            form.mes.data = str(mes_arg)
    else:
        dados = consulta_banco()

    if not dados:
        flash('Nenhum dado foi encontrado', 'error')

    return render_template('index.html', form=form, form_transacao=form_transacao, form_saldo=form_saldo, form_edit_transacao=form_edit_transacao, form_edit_saldo=form_edit_saldo, entradas=dados['entrada'], saidas=dados['saida'], saldos=dados['saldo'], total_entradas=dados['total_entrada'], total_saidas=dados['total_saida'], total_saldos=dados['total_saldo'], total_saldos_ant=dados['total_saldo_ant'], labels_resultado = dados['labels_resultado'], values_resultado=dados['values_resultado'], labels_saldos=dados['labels_saldo'], values_saldos=dados['values_saldo'], aba_ativa=aba_ativa)


def form_filtro():
    form = FiltrosForm()

    if request.method == 'POST' and request.form['form_name'] == 'filtros':
        if form.validate_on_submit():
            return redirect(url_for('webui.index',
                                    user = form.user.data,
                                    ano = form.ano.data,
                                    mes = form.mes.data,
                                    aba_ativa = 'entrada'))
        else:
            if form.errors:
                flash('Houve um erro com o formulário de filtros', 'error')
                return redirect(url_for('webui.index'))
    else:
        abort(400)


def form_transaction():
    form = NovaTransacaoForm()

    if request.method == 'POST' and request.form['form_name'] == 'transacao':
        if form.validate_on_submit():
            nova_entrada = Transacoes()
            nova_entrada.tipo = form.tipo.data.upper()
            nova_entrada.user_id = int(form.user.data)
            nova_entrada.ano = int(form.ano.data)
            nova_entrada.mes = int(form.mes.data)
            nova_entrada.descricao = form.desc.data
            nova_entrada.valor = float(form.valor.data.replace(',', '.'))

            db.session.add(nova_entrada)
            db.session.commit()
            flash(f'Nova {form.tipo.data.capitalize()} inserida com sucesso!')

            return redirect(url_for('webui.index',
                                                user = nova_entrada.user_id,
                                                ano = nova_entrada.ano,
                                                mes = nova_entrada.mes,
                                                aba_ativa = form.tipo.data))
        else:
            if form.errors:
                flash('Houve um erro com o formulário de nova transação.', 'error')
                return redirect(url_for('webui.index'))
    else:
        abort(400)


def form_saldo():
    form = NovoSaldoForm()

    if request.method == 'POST' and request.form['form_name'] == 'saldo':
        if form.validate_on_submit():

            saldo_existente = db.session.scalars(db.select(Saldos)
                                                    .where(Saldos.ano == int(form.ano.data))
                                                    .where(Saldos.mes == int(form.mes.data))
                                                    .where(Saldos.banco_id == int(form.banco.data))
                                                    .where(Saldos.user_id == int(form.user.data))
                                                ).first()
            if saldo_existente:
                saldo_existente.saldo = float(form.saldo.data.replace(',', '.'))
                flash('Saldo Alterado.')
            else:
                novo_saldo = Saldos()
                novo_saldo.ano = int(form.ano.data)
                novo_saldo.mes = int(form.mes.data)
                novo_saldo.saldo = float(form.saldo.data.replace(',', '.'))
                novo_saldo.user_id = int(form.user.data)
                novo_saldo.banco_id = int(form.banco.data)
                db.session.add(novo_saldo)
                flash('Novo Saldo Adicionado.')

            db.session.commit()

            return redirect(url_for('webui.index',
                                                user = int(form.user.data),
                                                ano = int(form.ano.data),
                                                mes = int(form.mes.data),
                                                aba_ativa = 'saldo'))
        else:
            if form.errors:
                flash('Houve um erro com o formulário de novo saldo.', 'error')
                return redirect(url_for('webui.index'))
    else:
        abort(400)


def users():
    users = db.session.scalars(db.select(Users)).all()
    users_dict = [user.to_dict() for user in users]
    
    return jsonify(users_dict)


def bancos():
    bancos = db.session.scalars(db.select(Bancos)).all()
    bancos_dict = [banco.to_dict() for banco in bancos]

    return jsonify(bancos_dict)


def config():
    form = FormBanco()
    form_edit = FormEditBanco()
    bancos = db.session.scalars(db.select(Bancos)).all()

    return render_template('config.html', form_banco=form, bancos=bancos, form_edit=form_edit)


def form_banco():
    form = FormBanco()

    if request.method == 'POST' and request.form['form_name'] == 'banco':
        if form.validate_on_submit():
            novo_banco = Bancos()
            novo_banco.nome = form.nome.data.title()

            db.session.add(novo_banco)
            db.session.commit()
            flash('Novo Banco criado com Sucesso!')
        else:
            flash('Houve um erro com o Formulário.')

        return redirect(url_for('webui.config'))
    else:
        abort(400)



def apagar_banco():
    banco_id = int(request.form['id'])
    banco = db.session.scalar(db.select(Bancos).where(Bancos.id == int(banco_id)))

    if not banco:
        flash('Houve um erro: Banco não encontrado.')
        return redirect(url_for('webui.config'))

    saldos = db.session.scalars(db.select(Saldos).where(Saldos.banco_id == banco_id)).first()

    if saldos:
        flash('Não é possível apagar um banco que tem saldos associados.')
        return redirect(url_for('webui.config'))

    db.session.delete(banco)
    db.session.commit()
    flash('Banco removido com Sucesso.')

    return redirect(url_for('webui.config'))


def edit_banco():
    form = FormEditBanco()

    if request.method == 'POST' and request.form['form_name'] == 'banco':
        if form.validate_on_submit():
            banco_id = int(form.id.data)
            banco = db.session.scalars(db.select(Bancos).where(Bancos.id == banco_id)).first()
            if banco:
                banco.nome = form.nome.data.title()

                db.session.commit()
                flash('Banco alterado com Sucesso!')
            else:
                flash('Houve um erro: O banco não foi encontrado.')
        else:
            flash('Houve um erro com o Formulário.')

        return redirect(url_for('webui.config'))
    else:
        abort(400)


def edit_transacao():
    form = FormEditTransacao()

    if request.method == 'POST' and request.form['form_name'] == 'transacao':
        if form.validate_on_submit():
            transacao = db.session.scalars(db.select(Transacoes).where(Transacoes.id == int(form.id.data))).first()

            if transacao:
                try:
                    transacao.descricao = form.desc.data
                    transacao.valor = float(form.valor.data.replace(',','.'))

                    db.session.commit()
                    flash(f'{form.tipo.data.capitalize()} atualizada com sucesso')
                except:
                    flash('Houve um erro durante a atualizacao. Tente novamente.')

                return redirect(url_for('webui.index',
                                                user = transacao.user_id,
                                                ano = transacao.ano,
                                                mes = transacao.mes,
                                                aba_ativa = transacao.tipo.lower()))
            else:
                abort(400)


def edit_saldo():
    form = FormEditSaldo()

    if request.method == 'POST' and request.form['form_name'] == 'saldo':
            if form.validate_on_submit():
                saldo = db.session.scalars(db.select(Saldos).where(Saldos.id == int(form.id.data))).first()

                if saldo:
                    try:
                        saldo.saldo = float(form.saldo.data.replace(',','.'))
                        db.session.commit()
                        flash('Saldo atualizado com sucesso.')
                    except:
                        flash('Houve um erro durante a atualizacao. Tente novamente.')

                    return redirect(url_for('webui.index',
                                                    user = saldo.user_id,
                                                    ano = saldo.ano,
                                                    mes = saldo.mes,
                                                    aba_ativa = 'saldo'))
                else:
                    abort(400)



def apaga_transacao_saldo():
    if request.method == 'POST' and request.form['tipo'] in ['saldo', 'transacao']:
        if request.form['tipo'] == 'transacao':
            transacao = db.session.scalars(db.select(Transacoes).where(Transacoes.id == int(request.form['id']))).first()
            if transacao:
                db.session.delete(transacao)
                db.session.commit()

                flash(f'{transacao.tipo.capitalize()} apagada com sucesso.')
                return redirect(url_for('webui.index',
                                                                user = transacao.user_id,
                                                                ano = transacao.ano,
                                                                mes = transacao.mes,
                                                                aba_ativa = transacao.tipo.lower()))
            else:
                abort(400)
        elif request.form['tipo'] == 'saldo':
            saldo = db.session.scalars(db.select(Saldos).where(Saldos.id == int(request.form['id']))).first()
            if saldo:
                db.session.delete(saldo)
                db.session.commit()

                flash('Saldo apagado com sucesso.')
                return redirect(url_for('webui.index',
                                                                                user = saldo.user_id,
                                                                                ano = saldo.ano,
                                                                                mes = saldo.mes,
                                                                                aba_ativa = 'saldo'))
            else:
                abort(400)
    else:
        abort(400)


def graficos_view():
    anos_transacoes = db.session.scalars(db.select(Transacoes.ano)).all()
    anos_saldos = db.session.scalars(db.select(Saldos.ano)).all()
    anos = list(set(anos_transacoes) | set(anos_saldos))
    return render_template('graficos.html', anos=anos)


def atualiza_graficos():
    dados = request.get_json()

    if not dados:
        abort(400)

    request_grafico = dados['grafico'][-1]
    request_ano = int(dados['ano'])
    request_user = int(dados['user'])
    request_meses = [int(k.split('-')[1]) for i, (k, v) in enumerate(dados['meses'].items()) if v == True]

    meses_fluxo = {str(mes): [['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1], 0, 0, 0] for mes in request_meses}
    meses_patrimonio = {str(mes): [['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1], 0, {}] for mes in request_meses}


    if request_grafico == '1':
        transacoes = db.session.scalars(db.select(Transacoes).where(Transacoes.ano == request_ano, Transacoes.mes.in_(request_meses), Transacoes.user_id == request_user)).all()

        if transacoes:
            for transacao in transacoes:
                if transacao.tipo == 'ENTRADA':
                    meses_fluxo[str(transacao.mes)][1] += float(transacao.valor)
                elif transacao.tipo == 'SAIDA':
                    meses_fluxo[str(transacao.mes)][2] += float(transacao.valor)

            dados_meses = []
            dados_entradas = []
            dados_saidas = []
            dados_saldos = []

            for k, v in meses_fluxo.items():
                v[3] = v[1] - v[2]
                dados_meses.append(v[0])
                dados_entradas.append(v[1])
                dados_saidas.append(v[2])
                dados_saldos.append(v[3])

            return jsonify({
                'meses': dados_meses,
                'entradas': dados_entradas,
                'saidas': dados_saidas,
                'saldos': dados_saldos
            })


        else:
            abort(400)

    elif request_grafico == '2':
        saldos = db.session.scalars(db.select(Saldos).where(Saldos.ano == request_ano, Saldos.mes.in_(request_meses), Saldos.user_id == request_user).order_by(Saldos.mes)).all()

        if saldos:
            bancos = sorted(set([saldo.banco.nome for saldo in saldos]))
            saldos_por_banco = {}
            for banco in bancos:
                color = [random.randint(0, 255) for _ in range(3)]
                saldos_por_banco[banco] = {
                    'label': banco,
                    'data': [None] * len(request_meses),
                    'backgroundColor': f"rgba({color[0]}, {color[1]}, {color[2]}, 0.6)",
                    'borderColor': f"rgba({color[0]}, {color[1]}, {color[2]}, 1)"
                }

            for saldo in saldos:
                meses_patrimonio[str(saldo.mes)][1] += float(saldo.saldo)
                meses_patrimonio[str(saldo.mes)][2][saldo.banco.nome] = meses_patrimonio[str(saldo.mes)][2].get(saldo.banco.nome, 0) + float(saldo.saldo)

            for i, m in enumerate(meses_patrimonio.values()):
                for b in m[2].items():
                    saldos_por_banco[b[0]]['data'][i] = b[1]

            data_meses = [v[0] for _, v in meses_patrimonio.items()]
            data_linha = [v[1] for _, v in meses_patrimonio.items()]
            data_barras = [saldo for _, saldo in saldos_por_banco.items()]

            return jsonify({
                'meses': data_meses,
                'linha': data_linha,
                'barras': data_barras
            })
                
        else:
            abort(400)
    else:
        abort(400)

    return ''
from flask import render_template, abort, redirect, url_for, jsonify, flash, request
from app.ext.database import db
from app.ext.database.models import *
from .forms import FiltrosForm, NovaTransacaoForm, NovoSaldoForm


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

    user_arg = request.args.get('user', type=int)
    ano_arg = request.args.get('ano', type=int)
    mes_arg = request.args.get('mes', type=int)
    aba_ativa = request.args.get('aba_ativa')

    # if request.method == 'POST' and request.form['form_name'] == 'filtros':
    #     if form.validate_on_submit():
    #         return redirect(url_for('webui.index',
    #                                 user = form.user.data,
    #                                 ano = form.ano.data,
    #                                 mes = form.mes.data,
    #                                 aba_ativa = 'entrada'))
    #     else:
    #         if form.errors:
    #             flash('Houve um erro com o formulário de filtros', 'error')
    #             return redirect(url_for('webui.index'))

    # if request.method == 'POST' and request.form['form_name'] == 'transacao':
    #     if form_transacao.validate_on_submit():
    #         nova_entrada = Transacoes()
    #         nova_entrada.tipo = form_transacao.tipo.data.upper()
    #         nova_entrada.user_id = int(form_transacao.user.data)
    #         nova_entrada.ano = int(form_transacao.ano.data)
    #         nova_entrada.mes = int(form_transacao.mes.data)
    #         nova_entrada.descricao = form_transacao.desc.data
    #         nova_entrada.valor = float(form_transacao.valor.data.replace(',', '.'))

    #         db.session.add(nova_entrada)
    #         db.session.commit()
    #         flash(f'Nova {form_transacao.tipo.data.capitalize()} inserida com sucesso!')

    #         return redirect(url_for('webui.index',
    #                                             user = nova_entrada.user_id,
    #                                             ano = nova_entrada.ano,
    #                                             mes = nova_entrada.mes,
    #                                             aba_ativa = form_transacao.tipo.data))
    #     else:
    #         if form_transacao.errors:
    #             flash('Houve um erro com o formulário de nova transação.', 'error')
    #             return redirect(url_for('webui.index'))

    # if request.method == 'POST' and request.form['form_name'] == 'saldo':
    #     if form_saldo.validate_on_submit():

    #         saldo_existente = db.session.scalars(db.select(Saldos)
    #                                                 .where(Saldos.ano == int(form_saldo.ano.data))
    #                                                 .where(Saldos.mes == int(form_saldo.mes.data))
    #                                                 .where(Saldos.banco_id == int(form_saldo.banco.data))
    #                                                 .where(Saldos.user_id == int(form_saldo.user.data))
    #                                             ).first()
    #         if saldo_existente:
    #             saldo_existente.saldo = float(form_saldo.saldo.data.replace(',', '.'))
    #             flash('Saldo Alterado.')
    #         else:
    #             novo_saldo = Saldos()
    #             novo_saldo.ano = int(form_saldo.ano.data)
    #             novo_saldo.mes = int(form_saldo.mes.data)
    #             novo_saldo.saldo = float(form_saldo.saldo.data.replace(',', '.'))
    #             novo_saldo.user_id = int(form_saldo.user.data)
    #             novo_saldo.banco_id = int(form_saldo.banco.data)
    #             db.session.add(novo_saldo)
    #             flash('Novo Saldo Adicionado.')

    #         db.session.commit()

    #         return redirect(url_for('webui.index',
    #                                             user = int(form_saldo.user.data),
    #                                             ano = int(form_saldo.ano.data),
    #                                             mes = int(form_saldo.mes.data),
    #                                             aba_ativa = 'saldo'))
    #     else:
    #         if form_saldo.errors:
    #             flash('Houve um erro com o formulário de novo saldo.', 'error')
    #             return redirect(url_for('webui.index'))

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

    return render_template('index.html', form=form, form_transacao=form_transacao, form_saldo=form_saldo, entradas=dados['entrada'], saidas=dados['saida'], saldos=dados['saldo'], total_entradas=dados['total_entrada'], total_saidas=dados['total_saida'], total_saldos=dados['total_saldo'], total_saldos_ant=dados['total_saldo_ant'], labels_resultado = dados['labels_resultado'], values_resultado=dados['values_resultado'], labels_saldos=dados['labels_saldo'], values_saldos=dados['values_saldo'], aba_ativa=aba_ativa)


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


def form_banco():
    return ''


def users():
    users = db.session.scalars(db.select(Users)).all()
    users_dict = [user.to_dict() for user in users]
    
    return jsonify(users_dict)


def bancos():
    bancos = db.session.scalars(db.select(Bancos)).all()
    bancos_dict = [banco.to_dict() for banco in bancos]

    return jsonify(bancos_dict)

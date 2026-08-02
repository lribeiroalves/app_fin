from flask import render_template, abort, redirect, url_for, jsonify, flash
from app.ext.database import db
from app.ext.database.models import *
from .forms import FiltrosForm, NovaEntradaForm
from sqlalchemy import select


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
    form_entrada = NovaEntradaForm()
    return render_template('index.html', form=form, form_entrada=form_entrada)


def form_index():
    form = FiltrosForm()
    form_entrada = NovaEntradaForm()

    if form.validate_on_submit():
        dados = consulta_banco(user=form.user.data, ano=form.ano.data, mes=form.mes.data)
        if not dados:
            flash('Nenhum dado foi encontrado', 'error')
            return redirect(url_for('webui.index'))
    else:
        print(form.errors)
        flash('Houve um erro com o formulário', 'error')
        return redirect(url_for('webui.index'))

    return render_template('index.html', form=form, form_entrada=form_entrada, entradas=dados['entrada'], saidas=dados['saida'], saldos=dados['saldo'], total_entradas=dados['total_entrada'], total_saidas=dados['total_saida'], total_saldos=dados['total_saldo'], total_saldos_ant=dados['total_saldo_ant'], labels_resultado = dados['labels_resultado'], values_resultado=dados['values_resultado'], labels_saldos=dados['labels_saldo'], values_saldos=dados['values_saldo'], aba_ativa='entrada')


def form_entrada():
    form = FiltrosForm()
    form_entrada = NovaEntradaForm()
    aba_ativa = 'entrada'

    if form_entrada.validate_on_submit():
        pass
    else:
        print(form_entrada.errors)
        flash('Houve um erro com o formulário.', 'error')
        return redirect(url_for('webui.index'))

    return render_template('index.html', form=form, form_entrada=form_entrada, entradas=dados['entrada'], saidas=dados['saida'], saldos=dados['saldo'], total_entradas=dados['total_entrada'], total_saidas=dados['total_saida'], total_saldos=dados['total_saldo'], total_saldos_ant=dados['total_saldo_ant'], labels_resultado = dados['labels_resultado'], values_resultado=dados['values_resultado'], labels_saldos=dados['labels_saldo'], values_saldos=dados['values_saldo'], aba_ativa='entrada')



def users():
    users = db.session.scalars(db.select(Users)).all()
    users_dict = [user.to_dict() for user in users]
    
    return jsonify(users_dict)


def bancos():
    bancos = db.session.scalars(db.select(Bancos)).all()
    bancos_dict = [banco.to_dict() for banco in bancos]

    return jsonify(bancos_dict)

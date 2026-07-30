from flask import render_template, abort, redirect, url_for, jsonify
from app.ext.database import db
from app.ext.database.models import *
from .forms import FiltrosForm
from sqlalchemy import select

def index():
    form = FiltrosForm()
    return render_template('index.html', form=form)


def form_index():
    form = FiltrosForm()
    dados_encontrados = False

    if form.validate_on_submit():
        entradas = db.session.scalars(db.select(Transacoes).where(Transacoes.ano == int(form.ano.data), Transacoes.mes == int(form.mes.data), Transacoes.user_id == int(form.user.data), Transacoes.tipo == 'ENTRADA')).all()
        saidas = db.session.scalars(db.select(Transacoes).where(Transacoes.ano == int(form.ano.data), Transacoes.mes == int(form.mes.data), Transacoes.user_id == int(form.user.data), Transacoes.tipo == 'SAIDA')).all()
        saldos = db.session.scalars(db.select(Saldos).where(Saldos.ano == int(form.ano.data), Saldos.mes == int(form.mes.data), Saldos.user_id == int(form.user.data))).all()

        ano_ant = int(form.ano.data)
        mes_ant = int(form.mes.data) - 1
        if not mes_ant:
            mes_ant = 12
            ano_ant -= 1

        saldos_ant = db.session.scalars(db.select(Saldos).where(Saldos.ano == ano_ant, Saldos.mes == mes_ant, Saldos.user_id == int(form.user.data))).all()

        total_entradas = 0
        total_saidas = 0
        total_saldos = 0
        total_saldos_ant = 0 

        if entradas:
            total_entradas = sum(entrada.valor for entrada in entradas)
            dados_encontrados = True
        if saidas:
            total_saidas = sum(saida.valor for saida in saidas)
            dados_encontrados = True
        if saldos:
            total_saldos = sum(saldo.saldo for saldo in saldos)
            dados_encontrados = True
        if saldos_ant:
            total_saldos_ant = sum(saldo.saldo for saldo in saldos_ant)

    # graficos
    labels_resultado = ['Entradas', 'Saidas']
    values_resultado = [total_entradas, total_saidas]

    return render_template('index.html', form=form, form_validated=dados_encontrados, entradas=entradas, saidas=saidas, saldos=saldos, total_entradas=total_entradas, total_saidas=total_saidas, total_saldos=total_saldos, total_saldos_ant=total_saldos_ant, labels_resultado = labels_resultado, values_resultado=values_resultado)


def users():
    users = db.session.scalars(db.select(Users)).all()
    users_dict = [user.to_dict() for user in users]
    
    return jsonify(users_dict)


def bancos():
    bancos = db.session.scalars(db.select(Bancos)).all()
    bancos_dict = [banco.to_dict() for banco in bancos]

    return jsonify(bancos_dict)

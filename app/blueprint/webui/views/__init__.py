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

    if form.validate_on_submit():
        entradas = db.session.scalars(db.select(Transacoes).where(Transacoes.ano == int(form.ano.data), Transacoes.mes == int(form.mes.data), Transacoes.user_id == int(form.user.data), Transacoes.tipo == 'ENTRADA')).all()
        saidas = db.session.scalars(db.select(Transacoes).where(Transacoes.ano == int(form.ano.data), Transacoes.mes == int(form.mes.data), Transacoes.user_id == int(form.user.data), Transacoes.tipo == 'SAIDA')).all()
        saldos = db.session.scalars(db.select(Saldos).where(Saldos.ano == int(form.ano.data), Saldos.mes == int(form.mes.data), Saldos.user_id == int(form.user.data))).all()

    return render_template('index.html', form=form, entradas=entradas, saidas=saidas, saldos=saldos)


def users():
    users = db.session.scalars(db.select(Users)).all()
    users_dict = [user.to_dict() for user in users]
    
    return jsonify(users_dict)


def bancos():
    bancos = db.session.scalars(db.select(Bancos)).all()
    bancos_dict = [banco.to_dict() for banco in bancos]

    return jsonify(bancos_dict)

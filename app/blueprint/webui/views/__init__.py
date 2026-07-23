from flask import render_template, abort, redirect, url_for, jsonify
from app.ext.database import db
from app.ext.database.models import *

def index():
    return render_template('index.html')


def users():
    users = db.session.scalars(db.select(Users)).all()
    users_dict = [user.to_dict() for user in users]
    
    return jsonify(users_dict)


def bancos():
    bancos = db.session.scalars(db.select(Bancos)).all()
    bancos_dict = [banco.to_dict() for banco in bancos]

    return jsonify(bancos_dict)
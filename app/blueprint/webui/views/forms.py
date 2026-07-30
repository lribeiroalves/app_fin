from flask_wtf.form import _Auto

from app.ext.database import db
from app.ext.database.models import *
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


class FiltrosForm(FlaskForm):
    user = SelectField('Usuário', choices=[], validators=[DataRequired()])
    ano = SelectField('Ano', choices=[], validators=[DataRequired()], default=datetime.now().year)
    mes = SelectField('Mês', choices=[('', 'Selecione...'), ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'), ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'), ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')], validators=[DataRequired()], default=datetime.now().month)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = db.session.scalars(db.select(Users)).all()
        self.user.choices = [(str(u.id), str(u.nome).title()) for u in users]
        self.user.choices.insert(0, ('', 'Selecione...'))

        anos_transacoes = db.session.scalars(db.select(Transacoes.ano)).all()
        anos_saldos = db.session.scalars(db.select(Saldos.ano)).all()
        anos = list(set(anos_transacoes) | set(anos_saldos))
        self.ano.choices = [(str(ano), str(ano)) for ano in anos]
        self.ano.choices.insert(0, ('', 'Selecione...'))

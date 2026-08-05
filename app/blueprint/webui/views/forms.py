from flask_wtf.form import _Auto

from app.ext.database import db
from app.ext.database.models import *
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DecimalField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

msg_req = 'Campo obrigatório.'

class FiltrosForm(FlaskForm):
    user = SelectField('Usuário', choices=[], validators=[DataRequired(message=msg_req)])
    ano = SelectField('Ano', choices=[], validators=[DataRequired(message=msg_req)], default=datetime.now().year)
    mes = SelectField('Mês', choices=[('', 'Selecione...'), ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'), ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'), ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')], validators=[DataRequired(message=msg_req)], default=datetime.now().month)
    form_name = HiddenField('form_name')

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


class NovaTransacaoForm(FlaskForm):
    user = SelectField('Usuário', choices=[], validators=[DataRequired(message=msg_req)])
    ano = StringField('Ano', validators=[DataRequired(message=msg_req)])
    mes = SelectField('Mês', choices=[('', 'Selecione...'), ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'), ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'), ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')], validators=[DataRequired(message=msg_req)])
    desc = TextAreaField('Descrição', validators=[DataRequired(message=msg_req)], render_kw={'rows': 5, 'style': 'height: 100%;'})
    valor = StringField('Valor', validators=[DataRequired(message="O valor é obrigatório.")])
    form_name = HiddenField('form_name')
    tipo = HiddenField('tipo')

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


class NovoSaldoForm(FlaskForm):
    user = SelectField('Usuário', choices=[], validators=[DataRequired(message=msg_req)])
    ano = StringField('Ano', validators=[DataRequired(message=msg_req)])
    mes = SelectField('Mês', choices=[('', 'Selecione...'), ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'), ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'), ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')], validators=[DataRequired(message=msg_req)])
    saldo = StringField('Valor', validators=[DataRequired(message="O valor é obrigatório.")])
    banco = SelectField('Banco', choices=[], validators=[DataRequired(message=msg_req)])
    form_name = HiddenField('form_name')

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

            bancos = db.session.scalars(db.select(Bancos)).all()
            self.banco.choices = [(str(b.id), str(b.nome)) for b in bancos]
            self.banco.choices.insert(0, ('', 'Selecione...'))


class FormBanco(FlaskForm):
    nome = StringField('Banco', validators=[DataRequired(message=msg_req)])
    form_name = HiddenField('form_name')


class FormEditBanco(FlaskForm):
    nome = StringField('Banco', validators=[DataRequired(message=msg_req)])
    id = HiddenField('Id', validators=[DataRequired()])
    form_name = HiddenField('form_name', validators=[DataRequired()])
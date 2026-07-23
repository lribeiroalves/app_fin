from . import db

from sqlalchemy import String, Numeric, ForeignKey, CheckConstraint, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import Optional
from datetime import datetime


class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'Usuario(id: {self.id}, nome: {self.nome})'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }


class Bancos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'Banco(id: {self.id}, nome: {self.nome})'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }


class TipoTransacao(str, Enum):
    ENTRADA = 'ENTRADA'
    SAIDA = 'SAIDA'


class Transacoes(db.Model):
    __table_args__ = (
        CheckConstraint("ano >= 2026", name="check_ano_valido"),
        CheckConstraint("mes >= 1 AND mes <= 12", name="check_mes_valido"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoTransacao] = mapped_column(SQLEnum(TipoTransacao, native_enum=False), nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)
    mes: Mapped[int] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    # Relacoes
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship('Users')

    def __repr__(self):
        return f'Transacao(id: {self.id}, tipo: {self.tipo}, ano: {self.ano}, mes: {self.mes}, descricao: {self.descricao}, valor: {self.valor}, user_id: {self.user_id}, user: {self.user})'

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'ano': self.ano,
            'mes': self.mes,
            'descricao': self.descricao,
            'valor': self.valor,
            'user_id': self.user_id
        }


class Saldos(db.Model):
    __table_args__ = (
            CheckConstraint("ano >= 2026", name="check_ano_valido"),
            CheckConstraint("mes >= 1 AND mes <= 12", name="check_mes_valido"),
            UniqueConstraint('ano', 'mes', 'banco_id', 'user_id', name='unique_ano_mes_banco_user')
        )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    ano: Mapped[int] = mapped_column(nullable=False)
    mes: Mapped[int] = mapped_column(nullable=False)
    saldo: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    # relacoes
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship('Users')
    banco_id: Mapped[int] = mapped_column(ForeignKey('bancos.id'))
    banco: Mapped['Bancos'] = relationship('Bancos')

    def __repr__(self):
        return f'Saldo(id: {self.id}, ano: {self.ano}, mes: {self.mes}, saldo: {self.saldo}, user_id: {self.user_id}, user: {self.user}, banco_id: {self.banco_id}, banco: {self.banco})'

    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'mes': self.mes,
            'saldo': self.saldo,
            'user_id': self.user_id,
            'banco_id': self.banco_id
        }

from . import db

from sqlalchemy import String, Numeric, ForeignKey, Integer, CheckConstraint, Enum as SQLEnum
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
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    # Relacoes
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship('Users')
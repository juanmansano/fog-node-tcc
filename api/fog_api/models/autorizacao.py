from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey, PrimaryKeyConstraint
from flask_marshmallow import Marshmallow

from sqlalchemy.ext.declarative import declarative_base

ma = Marshmallow()

Base = declarative_base()

class Autorizacao(Base):
    __tablename__ = 'autorizacao'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    id_usuario = Column(Integer())
    id_dispositivo = Column(Integer(), nullable = False)
    ativo = Column(Integer(), nullable=False)

class AutorizacaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Autorizacao

autorizacao_schema = AutorizacaoSchema()
autorizacao_schema = AutorizacaoSchema(many=True)

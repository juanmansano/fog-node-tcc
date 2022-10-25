from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey
from flask_marshmallow import Marshmallow

from sqlalchemy.ext.declarative import declarative_base

ma = Marshmallow()

Base = declarative_base()

class Atividades(Base):
    __tablename__ = 'atividades'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)
    iluminancia = Column(Integer(), nullable=False)

class AtividadesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Atividades

atividades_schema = AtividadesSchema()
atividades_schema = AtividadesSchema(many=True)
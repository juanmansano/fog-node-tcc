from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey
from flask_marshmallow import Marshmallow

from sqlalchemy.ext.declarative import declarative_base

ma = Marshmallow()

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)
    senha = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)

class UsuariosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuarios

usuarios_schema = UsuariosSchema()
usuarios_schema = UsuariosSchema(many=True)
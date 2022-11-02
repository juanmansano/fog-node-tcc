from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow

from sqlalchemy.ext.declarative import declarative_base

ma = Marshmallow()

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer(), ForeignKey("autorizacao.id_usuario"), primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)

class Dispositivos(Base):
    __tablename__ = 'dispositivos'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)
    id_ultima_atividade = Column(Integer(), nullable=False)
    ligado = Column(Integer(), nullable=False)
    ativo = Column(Integer(), nullable=False)
    owner = Column(Integer(), nullable=False)
    id_usuario_ultima_atualizacao = Column(Integer(), nullable=False)
    data_criacao = Column(DateTime(), nullable=True)
    atividade = relationship("Atividades")
    usuarios_autorizados = relationship("Autorizacao")

class Atividades(Base):
    __tablename__ = 'atividades'

    id = Column(Integer(), ForeignKey("dispositivos.id_ultima_atividade"), primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)

class Autorizacao(Base):
    __tablename__ = 'autorizacao'
    __table_args__ = (
        PrimaryKeyConstraint('id_usuario', 'id_dispositivo'),
    )

    id_usuario = Column(Integer())
    id_dispositivo = Column(Integer(), ForeignKey('dispositivos.id'))
    ativo = Column(Integer(), nullable=False)
    dados_autorizados = relationship("Usuarios")


class AtividadesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Atividades
        include_fk = True

class UsuariosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuarios
        include_fk = True

class AutorizacaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Autorizacao
        include_fk = True

    dados_autorizados = ma.Nested(UsuariosSchema, many=True)


class DispositivosSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Dispositivos

    atividade = ma.Nested(AtividadesSchema, many=True)
    usuarios_autorizados = ma.Nested(AutorizacaoSchema, many=True)
        

autorizacao_schema = AutorizacaoSchema()
autorizacao_schema = AutorizacaoSchema(many=True)

atividades_schema = AtividadesSchema()
atividades_schema = AtividadesSchema(many=True)

usuarios_schema = UsuariosSchema()
usuarios_schema = UsuariosSchema(many=True)


dispositivo_schema = DispositivosSchema()
dispositivo_schema = DispositivosSchema(many=True)


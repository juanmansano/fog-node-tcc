from flask import Blueprint, jsonify, request

from fog_api import db_core
from fog_api.api.middleware import middleware

from fog_api.models.autorizacao import Autorizacao, autorizacao_schema
from fog_api.models.usuarios import Usuarios, usuarios_schema

app = Blueprint('autorizacao', __name__, url_prefix='/novaAutorizacao')

@app.route('', methods=['POST'])
@middleware
def post():
    payload = request.json
    print(payload)

    usuario = db_core.query(Usuarios).filter(Usuarios.email==payload['email']).first()

    print(usuario.id)

    autorizacao = db_core.query(Autorizacao).filter(Autorizacao.id_usuario == usuario.id).filter(Autorizacao.id_dispositivo == payload['id_dispositivo']).first()

    if(autorizacao):
        return {'autorizacao_existente': 1}, 400

    id_usuario = usuario.id

    autorizacao = Autorizacao(id_usuario=id_usuario, id_dispositivo=payload['id_dispositivo'], ativo=payload['ativo'])
    db_core.add(autorizacao)
    db_core.commit()

    return {'usuario_adicionado': 1}
    
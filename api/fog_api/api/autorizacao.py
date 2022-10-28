from crypt import methods
from flask import Blueprint, jsonify, request

from fog_api import db_core
from fog_api.api.middleware import middleware

from fog_api.models.autorizacao import Autorizacao, autorizacao_schema
from fog_api.models.usuarios import Usuarios, usuarios_schema

app = Blueprint('autorizacao', __name__, url_prefix='')

@app.route('/autorizacao/dispositivo=<dispositivo_id>', methods=['GET'])
@middleware
def get(dispositivo_id):
    autorizacao = db_core.query(Usuarios.email, Usuarios.nome, Usuarios.id).\
                            join(Autorizacao, Usuarios.id == Autorizacao.id_usuario).\
                                filter(Autorizacao.id_dispositivo==dispositivo_id).\
                                    filter(Autorizacao.ativo==True).all()

    return jsonify(usuarios_schema.dump(autorizacao))

@app.route('/changeAutorizacao', methods=['POST'])
@middleware
def post():
    payload = request.json
    print(payload)

    usuario = db_core.query(Usuarios).filter(Usuarios.email==payload['email']).first()

    print(usuario.id)

    autorizacao = db_core.query(Autorizacao).\
                            filter(Autorizacao.id_usuario == usuario.id).\
                                filter(Autorizacao.id_dispositivo == payload['id_dispositivo']).\
                                        first()

    id_usuario = usuario.id

    if(autorizacao):
        autorizacao.ativo = payload['ativo']

    else:
        autorizacao = Autorizacao(id_usuario=id_usuario, id_dispositivo=payload['id_dispositivo'], ativo=payload['ativo'])
    
    db_core.add(autorizacao)
    db_core.commit()

    return {'autorizacao_atualizada': 1}
    
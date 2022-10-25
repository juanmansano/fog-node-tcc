from flask import Blueprint, jsonify, request

from fog_api import db_core
from fog_api.api.middleware import middleware

from fog_api.models.dispositivos import Autorizacao, Dispositivos, dispositivo_schema

app = Blueprint('dispositivos', __name__)

@app.route('/dispositivos/usuario=<user_id>', methods=['GET'])
@middleware
def get(user_id):
    dispositivos = db_core.query(Dispositivos)\
        .join(Autorizacao)\
            .filter(Autorizacao.id_usuario == user_id)\
                .filter(Autorizacao.ativo==1).all()

    print(dispositivos)
    print(jsonify(dispositivo_schema.dump(dispositivos)))
    
    return jsonify(dispositivo_schema.dump(dispositivos))

@app.route('/statusDispositivo/id=<dispositivo_id>', endpoint='status', methods=['POST'])
@middleware
def post(dispositivo_id):
    payload = request.json
    dispositivo = db_core.query(Dispositivos).filter(Dispositivos.id==dispositivo_id).first()

    dispositivo.id = dispositivo_id
    dispositivo.ligado = payload['ligado']
    dispositivo.id_usuario_ultima_atualizacao = payload['usuario_ultima_atualizacao']

    db_core.add(dispositivo)
    db_core.commit()

    return {'status_atualizado': True}

@app.route('/configuracaoDispositivo/id=<dispositivo_id>', endpoint='configuracao', methods=['POST'])
@middleware
def post(dispositivo_id):
    payload = request.json
    dispositivo = db_core.query(Dispositivos).filter(Dispositivos.id==dispositivo_id).first()

    dispositivo.id = dispositivo_id
    dispositivo.id_usuario_ultima_atualizacao = payload['usuario_ultima_atualizacao']
    dispositivo.ligado = payload['ligado']
    dispositivo.id_ultima_atividade = payload['id_ultima_atividade']
    if(payload.get('nome')):
        dispositivo.nome = payload['nome']

    db_core.add(dispositivo)
    db_core.commit()

    return {'configuracao_atualizada': True}


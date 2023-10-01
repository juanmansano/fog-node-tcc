import datetime
import json

from fog_api import config, broker_conn, db_core
from fog_api.models.dispositivos import Dispositivos
from fog_api.models.autorizacao import Autorizacao


def adicionar_dispositivo(mensagem):
    id_usuario = mensagem.get('ativar_owner')
    nome = mensagem.get('nome')
    data_criacao = datetime.datetime.strptime(mensagem.get('data_criacao'), '%d/%m/%Y %H:%M:%S')

    dispositivo = Dispositivos(nome=nome,
                               id_ultima_atividade=1,
                               owner=id_usuario, 
                               data_criacao=data_criacao,
                               ligado=0,
                               ativo=1, 
                               id_usuario_ultima_atualizacao=id_usuario)
    db_core.add(dispositivo)
    db_core.commit()

    dispositivo = db_core.query(Dispositivos).filter(Dispositivos.nome==nome, 
                                                     Dispositivos.data_criacao==data_criacao, 
                                                     Dispositivos.owner==id_usuario).first()
    

    autorizacao = Autorizacao(id_usuario=id_usuario, id_dispositivo=dispositivo.id, ativo=1)
    db_core.add(autorizacao)
    db_core.commit()

    message = '{"ativado": ' + str(dispositivo.id) + '}'
    message = json.dumps(message)
    
    if config.PROTOCOL == 'stomp':
        broker_conn.send(body=str(message), destination=config.STOMP_PUB_TOPIC)
    else:
        broker_conn.publish(config.PUB_TOPIC, message, config.QOS)
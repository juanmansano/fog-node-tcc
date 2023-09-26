from fog_api import config, broker_conn, db_core

from fog_api.models.atividades import Atividades

import json

def send_message(dispostivo_id, atividade_id):
    atividade = db_core.query(Atividades).filter(Atividades.id == atividade_id).first()
    message = {"atividade": atividade.nome, "iluminancia": atividade.iluminancia}
    message = json.dumps(message)
    print(message)

    if config.PROTOCOL == 'stomp':
        broker_conn.send(body=str(message), destination=config.STOMP_PUB_TOPIC)
    else:
        broker_conn.publish(config.PUB_TOPIC, message, config.QOS)

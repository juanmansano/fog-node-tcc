from fog_api import config, broker_conn, db_core

from fog_api.models.atividades import Atividades

import json
import time

answer = None
match_awnser = False

def send_message(dispostivo_id, atividade_id):
    global answer, match_awnser
    answer = None
    atividade = db_core.query(Atividades).filter(Atividades.id == atividade_id).first()
    message = {"atividade": atividade.nome, "iluminancia": atividade.iluminancia}
    message = json.dumps(message)

    if config.PROTOCOL == 'stomp':
        broker_conn.send(body=str(message), destination=config.STOMP_PUB_TOPIC)
    else:
        broker_conn.publish(config.PUB_TOPIC, message, config.QOS)

    while not answer:
        time.sleep(0.1)

    match_awnser = message_recived(dispostivo_id, atividade_id, answer)

    while not match_awnser:
        send_message(dispostivo_id, atividade_id)


def message_recived(dispositivo_id, atividade_id, message):
    if int(message["dispositivo_id"]) == int(dispositivo_id)\
        and message["atividade_id"] == atividade_id:
            return True
    else:
        return False

from fog_api import config, broker_conn, db_core
from fog_api.models.atividades import Atividades

import json
import time

answer = None
dispositivo = 0
atividade = 0

def send_message(dispositivo_id, atividade_id):
    global answer, dispositivo, atividade
    answer = None
    match_answer = False
    dispositivo = dispositivo_id
    atividade = atividade_id
    atividade_db = db_core.query(Atividades).filter(Atividades.id == atividade_id).first()
    message = {"atualizar_dispositivo_id": dispositivo_id, "atividade_id": atividade_id, "iluminancia": atividade_db.iluminancia}
    message = json.dumps(message)

    if config.PROTOCOL == 'stomp':
        broker_conn.send(body=str(message), destination=config.STOMP_PUB_TOPIC)
    else:
        broker_conn.publish(config.PUB_TOPIC, message, config.QOS)

    while not answer:
        time.sleep(0.01)

    match_answer = check_return(answer)

    while not match_answer:
        send_message(dispositivo_id, atividade_id)


def check_return(answer):

    global dispositivo, atividade, match_answer

    if int(answer.get("atualizado_dispositivo_id")) == int(dispositivo)\
    and int(answer.get("atividade_id")) == int(atividade):
        return True
    else:
        return False
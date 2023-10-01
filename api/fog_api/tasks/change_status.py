from fog_api import config, broker_conn, db_core
from fog_api.models.atividades import Atividades

import json
import time

answer = None
match_answer = False
dispositivo = 0
atividade = 0

def send_message(dispositivo_id, atividade_id):
    global answer, match_answer, dispositivo, atividade
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

    match_answer = check_return(message)

    while not match_answer:
        send_message(dispositivo_id, atividade_id)


def check_return(message):

    print(message)
    global dispositivo, atividade, match_answer
    print(dispositivo)
    print(atividade)
    print(message.get("atualizado_dispositivo_id"))
    print(message.get("atividade_id"))

    if int(message.get("atualizado_dispositivo_id")) == int(dispositivo)\
    and int(message.get("atividade_id")) == int(atividade):
        match_answer = True
    else:
        match_answer = False
from fog_api import config, broker_conn, db_core

from fog_api.models.atividades import Atividades


def send_message(dispostivo_id, atividade_id):
    atividade = db_core.query(Atividades).filter(Atividades.id == atividade_id).first()
    message = f'{"iluminancia": {atividade.iluminancia}}'
    print(message)

    broker_conn.publish(config.PUB_TOPIC, message, config.QOS)

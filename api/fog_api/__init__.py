import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .helpers import Singleton
from fog_api import config

import paho.mqtt.client as mqtt
import json

class Database(metaclass=Singleton):
    engine = SQLAlchemy()

db = Database()

db_core = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(
            "mysql+pymysql://juan:juan@localhost:3306/tcc",
            pool_size=15,
            max_overflow=10,
            pool_recycle=60 * 60 * 1,
            pool_timeout=30,
        )
    )
)

log = logging.getLogger(__name__)

def create_app():
    """ Retorna o aplicativo pronto para execução """
    from fog_api.api import dispositivos, atividades, usuarios, autorizacao

    app = Flask(__name__)
   
    # app.config.from_object(config)
    log.info('Configurado Flask')
    
    db.engine = SQLAlchemy()
    db.engine.init_app(app)
    log.info('Configurado Flask SQLAlchemy')

    log.info("Registrando blueprints")    
    app.register_blueprint(dispositivos.app)
    app.register_blueprint(atividades.app)
    app.register_blueprint(usuarios.app)
    app.register_blueprint(autorizacao.app)
    log.info('Configurado Blueprint')

    log.info("App criado")
    
    return app


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config.SUB_TOPIC, config.QOS)


def on_message(client, userdata, msg):
    if(msg.retain == 1):
        pass
    else:
        message = str(msg.payload)
        print(message)
        list = message.split("'")
        if(not message.startswith("b'test")):
            mensagem_json = json.loads(list[1])
            print(mensagem_json)


def create_mqtt_connection():
    
    Broker = "tccmansano.ddns.net"
    client = mqtt.Client("fog_")
    client.username_pw_set("juan", "juan1234")
    client.connect(Broker, 1883)
    client.loop_start()

    client.on_connect = on_connect
    client.on_message = on_message

    return client

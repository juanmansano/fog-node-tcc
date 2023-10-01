import logging
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import stomp
import paho.mqtt.client as mqtt

from .helpers import Singleton
from fog_api import config

mqtt_conn = None

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

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
   
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

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('received an error "%s"' % frame.body)
         
    def on_message(self, frame):
        from fog_api.tasks.recived_message import message_recived

        message = str(frame.body)
        mensagem_json = json.loads(message)
        message_recived(mensagem_json)
        

def init_stomp():
    stomp_conn = stomp.Connection(host_and_ports=[(config.BROKER, config.STOMP_PORT)])
    stomp_conn.set_listener('', MyListener())
    stomp_conn.connect(config.USER, config.PASS, wait=True)

    stomp_conn.subscribe(destination=config.STOMP_SUB_TOPIC, id=1, ack='auto')

    return stomp_conn


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexão MQTT estabelecida com sucesso")
        client.subscribe(config.SUB_TOPIC, config.QOS)
    else:
        print(f"Falha na conexão MQTT, código de retorno: {rc}")

# Função de callback para mensagens recebidas
def on_message(client, userdata, msg):
    from fog_api.tasks.recived_message import message_recived
    print(msg.payload.decode())
    message_recived(json.loads(msg.payload.decode()))

# Função para ouvir a fila MQTT
def init_mqtt():
    global mqtt_conn
    mqtt_conn = mqtt.Client('fog_')
    mqtt_conn.on_connect = on_connect
    mqtt_conn.on_message = on_message
    mqtt_conn.username_pw_set("juan", "juan1234")
    mqtt_conn.connect(config.BROKER, config.MQTT_PORT, keepalive=60)
    mqtt_conn.loop_start()

    return mqtt_conn

if config.PROTOCOL == 'stomp':
    broker_conn = init_stomp()
else:
    broker_conn = init_mqtt()
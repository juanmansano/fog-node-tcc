import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .helpers import Singleton

class Database(metaclass=Singleton):
    engine = SQLAlchemy()

db = Database()

db_core = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(
            "mysql+pymysql://remoto:juan1234@dvrmansano.ddns.net:3306/tcc",
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
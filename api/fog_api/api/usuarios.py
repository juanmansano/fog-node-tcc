from flask import Blueprint, request
import bcrypt
import jwt
import datetime

from fog_api import db_core

from fog_api.models.usuarios import Usuarios

app = Blueprint('usuarios', __name__)

@app.route('/createUser', methods=['POST'], endpoint='criar_usuario')
def post():
    payload = request.json
    email = payload['email']
    usuario = db_core.query(Usuarios).filter(Usuarios.email == email).first()

    if(usuario):
        return {'usuario_existente': 1}, 400

    salt = bcrypt.gensalt(8)

    nome = payload['nome']
    senha = bcrypt.hashpw(payload['senha'].encode('utf8'), salt)

    usuario = Usuarios(nome=nome, email=email, senha=senha)
    db_core.add(usuario)
    db_core.commit()

    return {'usuario_adicionado': 1}

@app.route('/authUser', methods=['POST'], endpoint='authUser')
def get():
    payload = request.json
    email = payload['email']

    usuario = db_core.query(Usuarios).filter(Usuarios.email == email).first()

    if(not usuario):
        return {'usuario_inexistente': 1}, 400

    senha_correta = bcrypt.checkpw(payload['senha'].encode('utf8'), usuario.senha.encode('utf-8'))


    if(not senha_correta):
        return {'senha_incorreta': 1}, 400

    encode_jwt = jwt.encode(payload={"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "exp": datetime.datetime.now() + datetime.timedelta(days=30) }, key='22b01d54f5921f51adb4d9c7a8fc2b1a', algorithm="HS256")

    return {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email, 'token': encode_jwt}


from functools import wraps
from flask import Response, request
import jwt
import datetime

from fog_api import db_core
from fog_api.models.usuarios import Usuarios

def middleware(func):
    @wraps(func)
    def middleware_function(*args, **kargs):
        token = request.headers['authorization'].split(" ")[1]
            
        try:
            data = jwt.decode(token, '22b01d54f5921f51adb4d9c7a8fc2b1a', 'HS256')
        except jwt.InvalidTokenError as e:
            return Response('Authorization failed', mimetype='text/plain', status=401)
        
        email = data['email']
        usuario = db_core.query(Usuarios).filter(Usuarios.email == email).first()

        if(datetime.datetime.utcfromtimestamp(data['exp'])  <= datetime.datetime.now()):
            return Respons('Authorization expired', mimetype='text/plain', status=401)

        if(data['nome']==usuario.nome):
            return func(*args, **kargs)

    return middleware_function

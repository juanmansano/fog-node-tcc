from flask import Blueprint, jsonify

from fog_api import db_core
from fog_api.api.middleware import middleware

from fog_api.models.atividades import Atividades, atividades_schema

app = Blueprint('atividades', __name__, url_prefix='/atividades')

@app.route('', methods=['GET'])
@middleware
def get():
    atividades = db_core.query(Atividades).order_by(Atividades.iluminancia.asc()).all()
    
    
    return jsonify(atividades_schema.dump(atividades))
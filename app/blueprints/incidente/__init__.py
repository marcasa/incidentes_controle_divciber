# app/blueprints/incidente/__init__.py

from flask import Blueprint

# Cria uma instância do Blueprint para as funcionalidades de 'analise'
# 'template_folder' e 'static_folder' direcionam para subpastas dentro do blueprint
incidente_bp = Blueprint('incidente', __name__, template_folder='templates', static_folder='static')

# Importa as rotas para que sejam registradas no blueprint
from app.blueprints.incidente import routes
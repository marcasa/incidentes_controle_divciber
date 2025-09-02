# app/blueprints/main/__init__.py
from flask import Blueprint

# Cria uma instância do Blueprint para as funcionalidades gerais (página inicial, etc.)
main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

# Importa as rotas para que sejam registradas no blueprint
from app.blueprints.main import routes
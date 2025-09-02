# app/blueprints/users/__init__.py

from flask import Blueprint
# Cria uma instância do Blueprint para as funções de cadastro de 'users'

users_bp = Blueprint('users', __name__, template_folder='templates', static_folder='static')

from app.blueprints.users import routes

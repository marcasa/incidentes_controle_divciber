# database.py

from app import create_app, db
from flask import current_app
import os

from app.models import User, Analise

app = create_app()

with app.app_context():
    
    if os.path.exists('instance/divciber.db'):
        os.remove('instance/divciber.db') # Remove o banco de dados existente para recriá-lo do zero (apenas para desenvolvimento)
        current_app.logger.info("Banco de dados existente removido.")
        
    db.create_all() # Cria todas as tabelas definidas nos modelos
    current_app.logger.info("Banco de dados e tabelas criados com sucesso.")
    
current_app.logger.info("Script de criação do banco de dados concluído.")
# database.py

from app import create_app, db
import os

from app.models import User, Analise

app = create_app()

with app.app_context():
    
    if os.path.exists('divciber.db'):
        os.remove('divciber.db') # Remove o banco de dados existente para recriá-lo do zero (apenas para desenvolvimento)
        print("Banco de dados existente removido.")
        
    db.create_all() # Cria todas as tabelas definidas nos modelos
    print("Banco de dados e tabelas criados com sucesso.")
    
print("Script de criação do banco de dados concluído.")
# run.py

import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

from app import create_app, db

app = create_app()
with app.app_context():
    
    #if os.path.exists('./instance/divciber.db'):
    #    os.remove('./instance/divciber.db') # Remove o banco de dados existente para recriá-lo do zero (apenas para desenvolvimento)
    #   print("Banco de dados existente removido.")
        
    db.create_all() # Cria todas as tabelas definidas nos modelos
    print("Banco de dados e tabelas criados com sucesso.")
    
print("Script de criação do banco de dados concluído.")

if __name__ == "__main__":
    app.run(port=5005)
    

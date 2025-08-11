# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig # Importando as classes de configuração do arquivo config.py

db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    
    app = Flask(__name__) # Criando uma instância do Flask
    app.config.from_object(config_class) # Carregando a configuração da classe fornecida > Desenvolvimento ou Produção
    
    db.init_app(app) # Inicializando o SQLAlchemy com a aplicação Flask
    
    #from app.blueprints import analise_bp
    #app.register_blueprint(analise_bp) # Registrando o blueprint análise
    
    #Implementar postertiormente manipuladores de erro personalizados
    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render_template('404.html'), 404
    
    return app # Retornando a instância da aplicação Flask
# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig # Importando as classes de configuração do arquivo config.py
from flask_login import LoginManager, set_login_view # Importando o gerenciador de login
import hashlib

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()
    
from flask_login import LoginManager, set_login_view # Importando o gerenciador de login
import hashlib

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()
    
db = SQLAlchemy()
lm = LoginManager()


def create_app(config_class=DevelopmentConfig):
    
    app = Flask(__name__) # Criando uma instância do Flask
    app.config.from_object(config_class) # Carregando a configuração da classe fornecida > Desenvolvimento ou Produção
    
    db.init_app(app) # Inicializando o SQLAlchemy com a aplicação Flask
    lm.init_app(app) # Inicializando o LoginManager com a aplicação Flask  
    # Carregando os blueprints
    from app.blueprints.main import main_bp # Importando o blueprint principal
    app.register_blueprint(main_bp) # Registrando o blueprint principal
    
    from app.blueprints.incidente import incidente_bp # Importando o blueprint análise
    app.register_blueprint(incidente_bp) # Registrando o blueprint análise com prefixo de URL
    
    from app.blueprints.users import users_bp # Importando o blueprint usuários
    app.register_blueprint(users_bp) # Registrando o blueprint usuários com prefixo de URL
    
    lm.login_view = 'users.login' # Definindo a rota de login
    lm.login_message = "Por favor, faça login para acessar o sistema." # Mensagem exibida quando o usuário não está autenticado
    
        
    #Implementar postertiormente manipuladores de erro personalizados
    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render_template('404.html'), 404
    
    return app # Retornando a instância da aplicação Flask




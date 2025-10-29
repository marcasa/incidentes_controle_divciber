# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig # Importando as classes de configuração do arquivo config.py
from flask_login import LoginManager, set_login_view # Importando o gerenciador de login
import hashlib
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_login import LoginManager, set_login_view # Importando o gerenciador de login
import hashlib

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()
    
db = SQLAlchemy()
lm = LoginManager()

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')
def create_app(config_class=ProductionConfig):
    
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
    
    
    # ====================================================================
    # CONFIGURAÇÃO DO LOGGING
    # ====================================================================

    if not app.debug and not app.testing:
        # Define o nível mínimo de log para o manipulador de arquivo
        log_level = logging.INFO
        
        # 1. Cria o manipulador de arquivo (Handler)
        # Rotaciona o arquivo quando ele atinge 10 MB e mantém 10 arquivos de backup
        file_handler = RotatingFileHandler(
            'logs/app.log', 
            maxBytes=1024 * 1024 * 10, # 10 MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        
        # 2. Define o formato da mensagem de log
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(module)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        
        # 3. Adiciona o manipulador ao logger da aplicação
        app.logger.addHandler(file_handler)
        app.logger.setLevel(log_level)
        
        # Opcional: Configurar o log para o console (útil em ambientes de produção)
        # if app.config['ENV'] == 'production':
        #     # Configuração do console para DEBUG/INFO
        #     stream_handler = logging.StreamHandler()
        #     stream_handler.setFormatter(formatter)
        #     stream_handler.setLevel(logging.INFO)
        #     app.logger.addHandler(stream_handler)

    # Cria a pasta de logs se ela não existir
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    # ====================================================================
    
    
    return app # Retornando a instância da aplicação Flask




import os


class Config:
    from dotenv import load_dotenv
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Desativa o rastreamento de modificações do SQLAlchemy para economizar memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class DevelopmentConfig(Config):
    DEBUG = True # Ativa o modo debug (recarregamento automático, mensagens de erro detalhadas)
    
class ProductionConfig(Config):
    DEBUG = False # Desativa o modo debug



























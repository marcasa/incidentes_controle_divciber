# config.py
import os


class Config:
    from dotenv import load_dotenv
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Desativa o rastreamento de modificações do SQLAlchemy para economizar memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    


  



























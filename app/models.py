# app/models.py

from datetime import datetime
from app import db # Importando a instância do SQLAlchemy de app/__init__.py
from werkzeug.security import generate_password_hash, check_password_hash # Importando funções para hash de senha


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID do usuário
    username = db.Column(db.String(100), unique=True, nullable=False) # Nome de usuário único
    email = db.Column(db.String(100), unique=True, nullable=False) # Email do usuário único
    password_hash = db.Column(db.String(256), nullable=False) # Hash da senha do usuário
    
    # Relacionamento: um usuário pode ter várias análises
    # 'backref' permite acessar o usuário a partir da análise (ex: analise.autor)
    analises = db.relationship('Analise', backref='autor', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # Gera o hash da senha
    
    def chack_password(self, password):
        return check_password_hash(self.password_hash, password) # Verifica a senha fornecida com o hash armazenado
    
    def __repr__(self):
        return f'<User {self.username}>'
    
class Analise(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID da análise
    incident_type = db.Column(db.String(100), nullable=False) # Tipo de incidente >>> posteriormente criar uma tabela de tipos de incidentes
    report_number = db.Column(db.String(50), nullable=False) # Número do relatório semanal ou relatorio técnico em que a análise foi feita
    msg_number = db.Column(db.String(50), nullable= True) # Número da mensagem enviada ou chamado aberto
    cpa = db.Column(db.String(100), nullable=False) # grande comando ou diretoria
    btl = db.Column(db.String(100), nullable=False) # Batalhão ou unidade envolvida no incidente
    cia = db.Column(db.String(100), nullable=True) # Companhia envolvida no incidente
    description = db.Column(db.Text, nullable=False) # Descrição do incidente
    start_date = db.Column(db.DateTime) # Data de abertura da análise/incidente
    end_date = db.Column(db.DateTime, nullable=True) # Data de encerramento da análise/incidente
    status = db.Column(db.String(50), default='Em andamento') # Status da análise
    
    def __repr__(self):
        return f'<Analise {self.incident_type} - {self.report_number}>'
# app/models.py

from datetime import datetime
from app import db # Importando a instância do SQLAlchemy de app/__init__.py
from werkzeug.security import generate_password_hash, check_password_hash # Importando funções para hash de senha
from flask_login import UserMixin # Importando UserMixin para integração com Flask-Login


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID do usuário
    username = db.Column(db.String(100), unique=True, nullable=False) # Nome de usuário único
    name = db.Column(db.String(100), unique=True, nullable=False) # Nome de usuário único
    email = db.Column(db.String(100), unique=True, nullable=False) # Email do usuário único
    profile = db.Column(db.String(50), nullable=False) # Perfil do usuário (admin, user ou viewer)
    is_temp_password = db.Column(db.Boolean, default=True, nullable=False)
    password = db.Column(db.String(256), nullable=False) # Hash da senha do usuário
    
    
    # Relacionamento: um usuário pode ter várias análises e várias observações
    # 'backref' permite acessar o usuário a partir da análise (ex: analise.autor)
    incidente = db.relationship('Incidente', backref='autor', lazy=True)
    observacoes = db.relationship('IncidenteObs', backref='autor_obs', lazy=True)
    
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password) # Gera o hash da senha
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password) # Gera o hash da senha
    
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password) # Verifica a senha fornecida com o hash armazenado
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password) # Verifica a senha fornecida com o hash armazenado
    
    def __repr__(self):
        return f'<User {self.username}>'
    
class Incidente(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID do incidente
    incident_type = db.Column(db.String(100), nullable=False) # Tipo de incidente >>> posteriormente criar uma tabela de tipos de incidentes
    report_number = db.Column(db.String(50), nullable=False) # Número do relatório semanal ou relatorio técnico em que a análise foi feita
    ticket_number = db.Column(db.String(50), nullable= True) # Número da mensagem enviada ou chamado aberto
    cpa = db.Column(db.String(100), nullable=False) # grande comando ou diretoria
    btl = db.Column(db.String(100), nullable=False) # Batalhão ou unidade envolvida no incidente
    cia = db.Column(db.String(100), nullable=True) # Companhia envolvida no incidente
    description = db.Column(db.Text, nullable=False) # Descrição do incidente. Como? Quando? Onde? Quem? Por quê? Ações tomadas?
    start_date = db.Column(db.DateTime, nullable=False) # Data de abertura da análise/incidente
    end_date = db.Column(db.DateTime, nullable=True) # Data de encerramento da análise/incidente
    status_incident = db.Column(db.String(50), default='Em andamento', nullable=False) # Status da análise
    
    # Chave estrangeira para o usuário que realizou a análise
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamento: uma análise pode ter várias observações
    # 'lazy=True' significa que as observações serão carregadas sob demanda
    obs_incidente = db.relationship('IncidenteObs', backref='incidente', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Incidente {self.incident_type} - {self.report_number}>'
    
    
class IncidenteObs(db.Model):
    
    # Modelo para a tabela de observações de análise
    id = db.Column(db.Integer, primary_key=True)
    texto_observacao = db.Column(db.Text, nullable=False)
    data_observacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # Chave estrangeira para o usuário que inseriu a observação
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Chave estrangeira para a análise à qual a observação pertence
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidente.id'), nullable=False)

    def __repr__(self):
        return f'<Observação {self.id}>'
        
class Unidades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpa = db.Column(db.String(100), nullable=False)
    btl = db.Column(db.String(100), nullable=False)
    

    def __repr__(self):
        return f'<Unidade {self.cpa} - {self.btl}>'
class TipoIncidente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_incidente = db.Column(db.String(100), nullable=False)
    desc_incidente = db.Column(db.Text, nullable=True)
    

    def __repr__(self):
        return f'<TipoIncidente {self.tipo_incidente} - {self.desc_incidente}>'

class StatusIncidente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    desc_status = db.Column(db.Text, nullable=True)
    

    def __repr__(self):
        return f'<StatusIncidente {self.status} - {self.desc_status}>'
    
    

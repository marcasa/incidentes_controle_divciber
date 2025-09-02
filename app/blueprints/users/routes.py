# app/blueprints/users/routes.py

from flask import render_template, url_for, flash, redirect, request
from app.blueprints.users import users_bp
from app.models import User
from app import db, lm, hash
from flask_login import login_user

@lm.user_loader # Função para carregar o usuário a partir do ID armazenado na sessão
def user_loader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user



@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    # Rota para cadastrar um novo usuário
    if request.method == 'GET':
        return render_template('users/register_user.html', title="Registro de usuário")
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        profile = request.form['profile']
        password = request.form['password']
        
        new_user = User(username=username, email=email, profile=profile, password= hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user) # Loga o usuário imediatamente após o registro
        
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('users.login'))
        
@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    # Rota para fazer login de um usuário
    if request.method == 'GET':
        return render_template('users/login.html', title="Login de usuário")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.session.query(User).filter_by(username=username, password= hash(password)).first()
        if not user:
            flash('Nome de usuário ou senha incorretos.', 'danger')
            return redirect(url_for('users.login'))
        
        login_user(user) # Loga o usuário se as credenciais estiverem corretas
        
        return redirect(url_for('main.home'))
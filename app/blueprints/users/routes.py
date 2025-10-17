# app/blueprints/users/routes.py

from flask import render_template, url_for, flash, redirect, request
from app.blueprints.users import users_bp
from app.models import User
from app import db, lm, hash
from flask_login import login_user, current_user, login_required


@lm.user_loader # Função para carregar o usuário a partir do ID armazenado na sessão
def user_loader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user



#Função para verificar se o perfil do usuário atual permite acesso a determinada rota
def allowed_edit_profile(profile):
    if profile.profile == 'Admin' or profile.profile == 'User':
        return True
    else:
        return False
    

@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.profile == 'Admin':
        # Rota para cadastrar um novo usuário
        if request.method == 'GET':
            return render_template('users/register_user.html', title="Registro de usuário")
        elif request.method == 'POST':
            username = request.form['username']
            name = request.form['name']
            email = request.form['email']
            profile = request.form['profile']
            password = request.form['password']
            
            new_user = User(username=username, name=name, email=email, profile=profile, password= hash(password))
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user) # Loga o usuário imediatamente após o registro
            
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('users.login'))
    else:
        flash('Acesso negado: Apenas administradores podem cadastrar novos usuários.', 'danger')
        return redirect(url_for('main.home'))
        
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
        
        # Verifica se o usuário possui uma senha temporaria
        if user.is_temp_password:
            return redirect(url_for('users.change_password'))
        
        return redirect(url_for('incidente.dashboard_incidentes_status'))
    
@users_bp.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method =='POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not new_password or new_password != confirm_password:
            flash('As senhas devem ser iguais.', 'danger')
            return redirect(url_for('users.change_password'))

        current_user.password = hash(new_password)
        current_user.is_temp_password = False
        db.session.commit()
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('users/change_psw.html', title="Alteração de senha")
    
        
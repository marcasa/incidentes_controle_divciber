# app/blueprints/main/routes.py

from flask import render_template, redirect, url_for
from app.blueprints.main import main_bp #importando a instância do blueprint main
from flask_login import login_required, logout_user, current_user

@main_bp.route('/')
@main_bp.route('/home')
@login_required
def home():
    #Rota página inicial
    return render_template('main/home.html', title='Página Inicial')
                           
@main_bp.route('/about')
def about():
    #Rota página sobre
    return render_template('main/about.html', title='Sobre')

@main_bp.route('/logout')
@login_required
def logout():
    # Rota para logout do usuário
    logout_user()
    return redirect(url_for('main.home'))
    
    
    
    
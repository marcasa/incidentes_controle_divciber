# app/blueprints/analise/routes.py

from flask import render_template, url_for, flash, redirect, request
from app.blueprints.analise import analise_bp
from app.models import Analise, User
from app import db
from flask_login import login_required, current_user


@analise_bp.before_request
@login_required


@analise_bp.route("/analises")
# @login_required
def listar_analises():
    # Rota para listar todas as análises
    analises = "Hello world"
    return render_template('analise/analises.html', title="Analises", analises = analises)

@analise_bp.route("/analises/nova", methods=['GET', 'POST'])
# @login_required
def nova_analise():
    # Rota para criar uma nova análise
    return render_template('analise/nova_analise.html', title="Nova Analise")


        
        
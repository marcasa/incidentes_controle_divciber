# app/blueprints/analise/routes.py

from flask import render_template, url_for, flash, redirect, request
from app.blueprints.incidente import incidente_bp
from app.models import Incidente, User
from app import db
from flask_login import login_required, current_user



@incidente_bp.route("/incidentes")
@login_required
def incidents_list():
    # Rota para listar todas as análises
    analises = "Hello world"
    return render_template('incidente/incidentes.html', title="Incidentes", analises = analises)

@incidente_bp.route("/incidente/new", methods=['GET', 'POST'])
@login_required
def new_incident():
    # Rota para criar uma nova análise
    return render_template('incidente/new_incident.html', title="Registro de Incidente")


        
        
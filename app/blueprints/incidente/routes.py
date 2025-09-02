# app/blueprints/analise/routes.py

from flask import render_template, url_for, flash, redirect, request
from app.blueprints.incidente import incidente_bp
from app.models import Incidente, User, IncidenteObs
from app import db
from flask_login import login_required, current_user
from datetime import datetime

#=================================LISTAR INCIDENTES=================================
@incidente_bp.route("/incidentes")
@login_required
def incidents_list():
    # Rota para listar todas as análises
    analises = "Hello world"
    return render_template('incidente/incidentes.html', title="Incidentes", analises = analises)

#=================================REGISTRAR NOVO INCIDENTE=================================
@incidente_bp.route("/incidente/new", methods=['GET', 'POST'])
@login_required
def new_incident():
    # Rota para registro de novo incidente
    if request.method == 'POST':
        # recebendo dados do formulário
        status_incident = request.form['status_incidente'] #notnull
        start_date = request.form['start_data_hora'] #notnull
        incident_type = request.form['incident_type'] #notnull
        report_number = request.form['report_number'] #notnull
        ticket_number = request.form['ticket_number']
        btl = request.form['btl'] #notnull
        cpa = request.form['cpa'] #notnull
        cia = request.form['cia']
        description = request.form['description'] #notnull
        
        # Usuário logado
        user_id = current_user.id
        
        # Verifica os campos obrigatórios
        if not all([status_incident, start_date, incident_type, report_number,btl, cpa, description]):
            flash('Erro: Os campos obrigatórios devem ser preenchidos.', 'danger')
            return redirect(url_for('incidente.new_incident'))
        
        # Convertendo campos de data para datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        # if end_date:
        #     end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
        # else:
        #     end_date = None
        
        # Criando nova instância de Incidente    
        new_incident = Incidente(
            status_incident=status_incident,
            start_date=start_date,
            incident_type=incident_type,
            report_number=report_number,
            ticket_number=ticket_number,
            btl=btl,
            cpa=cpa,
            cia=cia,
            description=description,
            user_id=user_id,
            # end_date=end_date
        )
        
        # Adicionando e comitando no banco de dados
        db.session.add(new_incident)
        db.session.commit()
        flash('Incidente registrado com sucesso!', 'success')
        return redirect(url_for('main.home')) #alterar para lista de incidentes
        
        
    return render_template('incidente/new_incident.html', title="Registro de Incidente")

#=================================ADD OBSERVAÇÃO=================================
@incidente_bp.route("/incidente/<int:incident_id>/add_obs", methods=['POST'])
@login_required
def add_obs(incident_id):
    # Rota para adicionar observação ao incidente
    texto_observacao = request.form['texto_observacao']
    user_id = current_user.id # Usuário logado
    data_observacao = datetime.now() # Data e hora atual
    
    # Adicionando e comitando no banco de dados
    new_obs = IncidenteObs(incidente_id=incident_id, usuario_id=user_id, texto_observacao=texto_observacao, data_observacao=data_observacao)
    db.session.add(new_obs)
    db.session.commit()
    flash('Observação adicionada com sucesso!', 'success')
    return redirect(url_for('incidente.incident_view', incident_id=incident_id))
                    
                    
#=================================VIEW DO INCIDENTE=================================
@incidente_bp.route("/incidente/<int:incident_id>", methods=['GET'])
@login_required
def incident_view(incident_id):
    # Rota para visualizar detalhes de um incidente específico
    incidente = Incidente.query.get_or_404(incident_id)
    return render_template('incidente/incidente_view.html', title="Detalhes do Incidente", incidente=incidente)



        
        
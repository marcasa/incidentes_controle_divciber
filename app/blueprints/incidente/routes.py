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
    incidentes = Incidente.query.all()
    return render_template('incidente/incidentes.html', title="Incidentes Registrados", incidentes = incidentes)

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

#=================================EDITAR INCIDENTE=================================
@incidente_bp.route("/incidente/<int:incident_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_incident(incident_id):
    # Rota para editar um incidente
    
    #carregando dados do incidente registrado pelo id
    incident = Incidente.query.get_or_404(incident_id)
    
    # Veririfica o metodo da requisição, se for POST, atualiza os dados
    if request.method == 'POST':
        # recebendo dados do formulário
        incident.status_incident = request.form['status_incidente'] #notnull
        incident.start_date = request.form['start_data_hora'] #notnull
        incident.incident_type = request.form['incident_type'] #notnull
        incident.report_number = request.form['report_number'] #notnull
        incident.ticket_number = request.form['ticket_number']
        incident.btl = request.form['btl'] #notnull
        incident.cpa = request.form['cpa'] #notnull
        incident.cia = request.form['cia']
        incident.description = request.form['description'] #notnull
        
        # Verifica os campos obrigatórios
        if not all([incident.status_incident, incident.start_date, incident.incident_type, incident.report_number, incident.btl, incident.cpa, incident.description]):
            flash('Erro: Os campos obrigatórios devem ser preenchidos.', 'danger')
            return redirect(url_for('incidente.edit_incident', incident_id=incident_id))
        
        # Convertendo campos de data para datetime
        incident.start_date = datetime.strptime(incident.start_date, '%Y-%m-%dT%H:%M')
        # if incident.end_date:
        #     incident.end_date = datetime.strptime(incident.end_date, '%Y-%m-%dT%H:%M')
        # else:
        #     incident.end_date = None
        
        # Adicionando e comitando no banco de dados
        db.session.commit()
        flash('Incidente editado com sucesso!', 'success')
        return redirect(url_for('incidente.incident_view', incident_id=incident_id))
    
    edit_mode = True  # Indicador de modo de edição para o template
    # Se for GET, renderiza o formulário com os dados atuais
    return render_template('incidente/new_incident.html', title="Editar Incidente", incident = incident, edit_mode=edit_mode)
    
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


#=================================EXCLUIR OBSERVAÇÃO=================================
@incidente_bp.route("/incidente/<int:incident_id>/delete_obs/<int:obs_id>", methods=['POST'])
@login_required
def delete_obs(incident_id, obs_id):
    # Rota para excluir observação
    obs = IncidenteObs.query.get_or_404(obs_id)

    db.session.delete(obs)
    db.session.commit()
    flash('Observação excluida com sucesso!', 'success')
    return redirect(url_for('incidente.incident_view', incident_id=incident_id))
                    
                    
#=================================VIEW DO INCIDENTE=================================
@incidente_bp.route("/incidente/<int:incident_id>", methods=['GET'])
@login_required
def incident_view(incident_id):
    # Rota para visualizar detalhes de um incidente específico
    incidente = Incidente.query.get_or_404(incident_id)
    return render_template('incidente/incidente_view.html', title="Detalhes do Incidente", incidente=incidente)



        
        
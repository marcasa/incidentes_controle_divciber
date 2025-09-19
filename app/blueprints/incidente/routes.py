# app/blueprints/analise/routes.py

from flask import render_template, url_for, flash, redirect, request
from app.blueprints.incidente import incidente_bp
from app.models import Incidente, User, IncidenteObs, Unidades, StatusIncidente, TipoIncidente
from app import db
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import or_



################################################################################
#=================================ROTAS INCIDENTE========================
################################################################################


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
        
        print(f"Status Incidente: {status_incident}\nStart Date: {start_date}\nIncident Type: {incident_type}\nreport_number: {report_number}\nTicket Number: {ticket_number}\nBTL: {btl}\nCPA: {cpa}\nCIA: {cia}\nDescription: {description}\nUser ID: {user_id}")
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
        return redirect(url_for('incidente.incidents_list')) #alterar para lista de incidentes
        
    unidades = Unidades.query.all() # Carrega os dados da tabela unidades para o formulário
    incidents_types = TipoIncidente.query.all()# Carrega os dados da tabela TipoIncidente para o formulário
    status_incident_list = StatusIncidente.query.all() # Carrega os dados da tabela status para o formulário    
    return render_template('incidente/new_incident.html', title="Registro de Incidente", unidades= unidades , status_incident_list=status_incident_list, incidents_types=incidents_types)

#=================================EDITAR INCIDENTE=================================
@incidente_bp.route("/incidente/<int:incident_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_incident(incident_id):
    # Rota para editar um incidente
    
    #carregando dados do incidente registrado pelo id
    incident = Incidente.query.get_or_404(incident_id)
    
    # Veririfica o metodo da requisição, se for POST, atualiza os dados
    if request.method == 'POST':
        
        #Armazenando os dados oriinais antes da edição
        original_data = {
            'status_incident': incident.status_incident,
            'start_date': incident.start_date,
            'incident_type': incident.incident_type,
            'report_number': incident.report_number,
            'ticket_number': incident.ticket_number,
            'btl': incident.btl,
            'cpa': incident.cpa,
            'cia': incident.cia,
            'description': incident.description
        }
        
                  
        # Atualiza o objeto incidente com os novos dados do formulário
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
        
        #VERIFICANDO QUAIS CAMPOS FORAM MODIFICADOS
        changes = []
        campos = ['status_incident', 'start_date', 'incident_type', 'report_number', 'ticket_number', 'btl', 'cpa', 'cia', 'description']
        
        for key, new_value in incident.__dict__.items():
            original_value = original_data.get(key)
            if new_value != str(original_value):
                if key in campos:
                    changes.append(f"{key} alterado de '{original_value}' para '{new_value}' \n")  
        
        if changes:
            txt_obs = "Alterações realizadas:\n" + "\n".join(changes)
            new_obs = IncidenteObs(incidente_id=incident.id, usuario_id=4, texto_observacao=txt_obs, data_observacao=datetime.now()) #Usuário ID 1 -Sistema        
        
        # Adicionando a observação de alterações no incidente
        db.session.add(new_obs)
        
        # Adicionando e comitando no banco de dados
        db.session.commit()
        flash('Incidente editado com sucesso!', 'success')
        return redirect(url_for('incidente.incident_view', incident_id=incident_id))
    
    edit_mode = True  # Indicador de modo de edição para o template
    unidades = Unidades.query.all() # Carrega os dados da tabela unidades para o formulário
    incidents_types = TipoIncidente.query.all()# Carrega os dados da tabela TipoIncidente para o formulário
    status_incident_list = StatusIncidente.query.all() # Carrega os dados da tabela status para o formulário
    # Se for GET, renderiza o formulário com os dados atuais
    return render_template('incidente/new_incident.html', title="Editar Incidente", incident = incident, edit_mode=edit_mode, unidades=unidades, status_incident_list=status_incident_list, incidents_types=incidents_types)

#================================EXCLUIR INCIDENTE=================================
@incidente_bp.route("/incidente/delete/<int:incident_id>", methods=['POST'])
@login_required 
def delete_incident(incident_id):
    # Rota para excluir um incidente
    incident = Incidente.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    flash('Incidente excluído com sucesso!', 'success')
    return redirect(url_for('incidente.incidents_list'))   





#=================================PESQUISAR INCIDENTE=================================
@incidente_bp.route("/incidente/pesquisar", methods=['GET'])
@login_required
def search_incident():
    # Rota para pesquisar incidentes
    
    termo = request.args.get('termo', '') # Pega o termo de pesquisa do formulário
    
    # Se não houver termo de pesquisa, redireciona para a lista de incidentes
    if not termo:
        return redirect(url_for('incidente.incidents_list'))
    
    query = Incidente.query
    search_terms = f"%{termo}%"
    
    filters = [
        Incidente.incident_type.ilike(search_terms),
        Incidente.report_number.ilike(search_terms),
        Incidente.ticket_number.ilike(search_terms),
        Incidente.btl.ilike(search_terms),
        Incidente.cpa.ilike(search_terms),
        Incidente.cia.ilike(search_terms),
        Incidente.description.ilike(search_terms),
    ]
    
    resultados = query.filter(or_(*filters)).all()
    
    return render_template('incidente/incidentes.html', title=f"Resultados da pesquisa para: {termo}", incidentes=resultados)

    
################################################################################
#===============================OBSERVAÇÕES DO INCIDENTE========================
################################################################################


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



#####################################################################################################
#=================================DASHBOARD=================================
#####################################################################################################

# app/blueprints/incidente/routes.py
# ... (seus imports existentes) ...
import pandas as pd
import plotly.express as px
from sqlalchemy.sql import func
import json


@incidente_bp.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    # Rota para visualizar o dashboard de incidentes
    
    if request.args.get('start_date'):
        start_date = request.args.get('start_date')
    else:
        start_date = '2024-06-03'
    
    if request.args.get('end_date'):
        end_date = request.args.get('end_date')
    else:
        end_date = datetime.now().strftime('%Y-%m-%d')
        
    incident_type = request.args.get('incident_type')
    status_str = request.args.get('status')
    
    
    incidents_types = TipoIncidente.query.all()
    status = StatusIncidente.query.all()
    
    incidentes = Incidente.query.all()
    nomes_colunas = []
    
    for incidente in incidentes:
        nomes_colunas.append({
            'id': incidente.id,
            'incident_type': incidente.incident_type,
            'report_number': incidente.report_number,
            'ticket_number': incidente.ticket_number,
            'cpa': incidente.cpa,
            'btl': incidente.btl,
            'cia': incidente.cia,
            'start_date': incidente.start_date,
            'end_date': incidente.end_date,
            'status_incident': incidente.status_incident
        })
    
    df= pd.DataFrame(nomes_colunas)
    
      
    filtro_periodo = (df['start_date'] >= pd.to_datetime(start_date)) & (df['start_date'] <= pd.to_datetime(end_date))
    filtro_status = df['status_incident'] == status_str
    filtro_tipo_incidente = df['incident_type'] == incident_type
    
    filtros_aplicados = f"Periodo: {start_date} - {end_date}, Status: {status_str}, Tipo Incidente: {incident_type}"
    
    df_filtred = df[filtro_periodo]
    
    print(df_filtred)
    
    # if incident_type :
    #     df_bar = df[df['incident_type'] == incident_type]
    # else:
    #     df_bar = df
    
    df_bar = df_filtred
        
    bar_counts = df_bar.groupby(['cpa', 'btl']).size().reset_index(name='total')
    
    ##################################################################
    # Gráfico de barras empilhadas com Plotly ======================
    fig_bar = px.bar(
        bar_counts,
        x='cpa',
        y='total',
        color='btl',
        title='',
        labels={'cpa': 'Grande Comando', 'total': 'Incidentes'}
    )
    fig_bar.update_layout(barmode='stack')
    bar_chart_html = fig_bar.to_html(full_html=False)
    
    
    
    
    
    
    ###########################################
    #GRAFICO ROSCA
    
    # if status_str:
    #     df_donut = df[df['status_incident'] == status_str]
    # else:
    #     df_donut = df
    
    df_donut = df_filtred
        
    status_counts = df_donut.groupby('status_incident').size().reset_index(name='total')
    
    # Cria o gráfico de rosca com Plotly
    fig_donut = px.pie(
        status_counts,
        values='total',
        names='status_incident',
        hole=0.6,
        title='Incidentes por Status'
    )
    fig_donut.update_traces(textposition='outside', textinfo='percent+label')
    donut_chart_html = fig_donut.to_html(full_html=False)
    
    
    
    
    
    return render_template(
        'dashboard/dashboard.html',
        title="Dashboard de Incidentes",
        incidents_types=incidents_types,
        status=status,
        bar_chart_html=bar_chart_html,
        donut_chart_html=donut_chart_html,
        filtros_aplicados=filtros_aplicados
        )
        
    
        
    
    

        
        
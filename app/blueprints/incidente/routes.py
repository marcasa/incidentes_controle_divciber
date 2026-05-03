# app/blueprints/incidente/routes.py

from flask import render_template, url_for, flash, redirect, request, current_app, jsonify
from app.blueprints.incidente import incidente_bp
from app.models import Incidente, User, IncidenteObs, Unidades, StatusIncidente, TipoIncidente
from app import db
from flask_login import login_required, current_user
from datetime import datetime, timedelta, timezone
from sqlalchemy import or_
from app.utils.data_processing import get_filtered_incidents_df
from app.blueprints.users.routes import allowed_edit_profile
import os
import uuid
import shutil
import re
from werkzeug.utils import secure_filename

# Configurações de upload
UPLOAD_TEMP_FOLDER = 'app/static/uploads/incidentes/temp'
UPLOAD_FINAL_FOLDER = 'app/static/uploads/incidentes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função auxiliar para formatar timedelta em uma string legível
def format_timedelta(td):
    if not td: return "N/A"
    total_segundos = int(td.total_seconds())
    dias, resto = divmod(total_segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, _ = divmod(resto, 60)
    tempo_formatado = []
    if dias > 0: tempo_formatado.append(f"{dias}d")
    if horas > 0: tempo_formatado.append(f"{horas}h")
    if minutos > 0: tempo_formatado.append(f"{minutos}m")
    return " ".join(tempo_formatado) if tempo_formatado else "1m"

# Rota de Upload de Imagem
@incidente_bp.route("/incidente/upload", methods=['POST'])
@login_required
def upload_image():
    if 'upload' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['upload']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    os.makedirs(UPLOAD_TEMP_FOLDER, exist_ok=True)
    file.save(os.path.join(UPLOAD_TEMP_FOLDER, unique_filename))
    url = url_for('static', filename=f'uploads/incidentes/temp/{unique_filename}')
    return jsonify({'url': url})

################################################################################
#=================================ROTAS INCIDENTE========================
################################################################################

#=================================LISTAR INCIDENTES=================================
@incidente_bp.route("/incidentes", methods=['GET'])
@login_required
def incidents_list():
    status_filter = request.args.get('status_filter')
    direction_filter = request.args.get('direction', 'desc')
    sort_by = request.args.get('sort_by', 'start_date')
    query = Incidente.query
    if status_filter and status_filter != 'todos':
        query = query.filter(Incidente.status_incident == status_filter)
    if sort_by:
        if direction_filter == 'desc': query = query.order_by(db.desc(getattr(Incidente, sort_by)))
        else: query = query.order_by(db.asc(getattr(Incidente, sort_by)))
    incidentes = query.all()
    now = datetime.now(timezone.utc)
    incidentes_com_tempo = []
    for inc in incidentes:
        start_date_aware = inc.start_date.replace(tzinfo=timezone.utc)
        if inc.end_date:
            end_date_aware = inc.end_date.replace(tzinfo=timezone.utc)
            duracao = end_date_aware - start_date_aware
        else:
            duracao = now - start_date_aware
        inc.tempo_aberto_formatado = format_timedelta(duracao)
        incidentes_com_tempo.append(inc)
    status_options = db.session.query(Incidente.status_incident).distinct().all()
    return render_template('incidente/incidentes.html', title="Incidentes Registrados", incidentes = incidentes_com_tempo, status_options=status_options, direction_filter=direction_filter, sort_by=sort_by, status_filter=status_filter)

#=================================REGISTRAR NOVO INCIDENTE=================================
@incidente_bp.route("/incidente/new", methods=['GET', 'POST'])
@login_required
def new_incident():
    if allowed_edit_profile(current_user):
        if request.method == 'POST':
            status_incident = request.form['status_incidente']
            start_date = request.form['start_data_hora']
            incident_type = request.form['incident_type']
            report_number = request.form['report_number']
            ticket_number = request.form['ticket_number']
            btl = request.form['btl']
            cpa = request.form['cpa']
            cia = request.form['cia']
            description = request.form['description']
            
            if not all([status_incident, start_date, incident_type, report_number,btl, cpa, description]):
                flash('Erro: Os campos obrigatórios devem ser preenchidos.', 'danger')
                return redirect(url_for('incidente.new_incident'))
            
            start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            
            new_incident = Incidente(status_incident=status_incident, start_date=start_date, incident_type=incident_type, report_number=report_number, ticket_number=ticket_number, btl=btl, cpa=cpa, cia=cia, description=description, user_id=current_user.id)
            
            db.session.add(new_incident)
            db.session.commit()
            
            # Movimentação e Renomeação de imagens
            incident_dir = os.path.join(UPLOAD_FINAL_FOLDER, str(new_incident.id))
            os.makedirs(incident_dir, exist_ok=True)
            
            if os.path.exists(UPLOAD_TEMP_FOLDER):
                files = os.listdir(UPLOAD_TEMP_FOLDER)
                seq = 1
                for filename in files:
                    if filename in new_incident.description:
                        # Extrair extensão
                        ext = filename.rsplit('.', 1)[1]
                        new_name = f"evidencia_incidente_{new_incident.id}_{seq}.{ext}"
                        shutil.move(os.path.join(UPLOAD_TEMP_FOLDER, filename), os.path.join(incident_dir, new_name))
                        new_incident.description = new_incident.description.replace(f'/static/uploads/incidentes/temp/{filename}', f'/static/uploads/incidentes/{new_incident.id}/{new_name}')
                        seq += 1
                db.session.commit()
            
            flash('Incidente registrado com sucesso!', 'success')
            return redirect(url_for('incidente.incidents_list'))
            
        unidades = Unidades.query.all()
        incidents_types = TipoIncidente.query.all()
        status_incident_list = StatusIncidente.query.all()
        return render_template('incidente/new_incident.html', title="Registro de Incidente", unidades= unidades , status_incident_list=status_incident_list, incidents_types=incidents_types)
    else:
        flash('Acesso negado: Você não tem permissão para registrar um novo incidente.', 'danger')
        return redirect(url_for('incidente.incidents_list'))

#=================================EDITAR INCIDENTE=================================
@incidente_bp.route("/incidente/<int:incident_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_incident(incident_id):
    def format_key_name(key_name):
        if not isinstance(key_name, str): return str(key_name)
        return key_name.replace('_', ' ').title()
    if allowed_edit_profile(current_user):
        incident = Incidente.query.get_or_404(incident_id)
        if request.method == 'POST':
            DATE_FORMAT = '%Y-%m-%dT%H:%M'
            original_data = {'status_incident': incident.status_incident, 'start_date': incident.start_date.strftime(DATE_FORMAT) if incident.start_date else '', 'incident_type': incident.incident_type, 'report_number': incident.report_number, 'ticket_number': incident.ticket_number, 'btl': incident.btl, 'cpa': incident.cpa, 'cia': incident.cia, 'description': incident.description}
            form_to_model = {'status_incidente': 'status_incident', 'start_data_hora': 'start_date', 'incident_type': 'incident_type', 'report_number': 'report_number', 'ticket_number': 'ticket_number', 'btl': 'btl', 'cpa': 'cpa', 'cia': 'cia', 'description': 'description'}
            changes = []
            new_values_map = {}
            for form_key, model_key in form_to_model.items():
                new_value = request.form.get(form_key, '').strip()
                new_values_map[model_key] = new_value
                original_value = original_data.get(model_key, '')
                original_str = str(original_value or '')
                new_str = str(new_value or '')
                if model_key in ['ticket_number', 'cia'] and original_str in ('None', '') and (new_str == '' or new_str == 'None' or new_str is None): continue
                if new_str != original_str:
                    friendly_name = format_key_name(model_key)
                    if new_str == 'Encerrado': incident.end_date = datetime.now()
                    changes.append(f"{friendly_name} alterado de '{original_str}' para '{new_str}'")
            incident.status_incident = new_values_map['status_incident']
            incident.start_date = new_values_map['start_date']
            incident.incident_type = new_values_map['incident_type']
            incident.report_number = new_values_map['report_number']
            incident.ticket_number = new_values_map['ticket_number']
            incident.btl = new_values_map['btl']
            incident.cpa = new_values_map['cpa']
            incident.cia = new_values_map['cia']
            incident.description = new_values_map['description']
            if not all([incident.status_incident, incident.start_date, incident.incident_type, incident.report_number, incident.btl, incident.cpa, incident.description]):
                flash('Erro: Os campos obrigatórios devem ser preenchidos.', 'danger')
                return redirect(url_for('incidente.edit_incident', incident_id=incident_id))
            try:
                incident.start_date = datetime.strptime(incident.start_date, DATE_FORMAT)
            except ValueError:
                flash('Erro: Formato de data/hora inválido.', 'danger')
                return redirect(url_for('incidente.edit_incident', incident_id=incident_id))
            if changes:
                txt_obs = "Alterações:\n" + "\n".join(changes)
                txt_obs += f"Usuário: {current_user.name}"
                new_obs = IncidenteObs(incidente_id=incident.id, usuario_id=1, texto_observacao=txt_obs, data_observacao=datetime.now()) 
                db.session.add(new_obs)
            db.session.commit()
            current_app.logger.info(f"Usuario {current_user.id} editou o incidente {incident_id}")
            flash('Incidente editado com sucesso!', 'success')
            return redirect(url_for('incidente.incident_view', incident_id=incident_id))
        edit_mode = True
        unidades = Unidades.query.all()
        incidents_types = TipoIncidente.query.all()
        status_incident_list = StatusIncidente.query.all()
        return render_template('incidente/new_incident.html', title="Editar Incidente", incident = incident, edit_mode=edit_mode, unidades=unidades, status_incident_list=status_incident_list, incidents_types=incidents_types)
    else:
        current_app.logger.info(f"Usuario {current_user.id} tentou editar o incidente {incident_id}. Sem permissão. {current_user.profile}")
        flash('Acesso negado: Você não tem permissão para editar este incidente.', 'danger')
        return redirect(url_for('incidente.incident_view', incident_id=incident_id))

#================================EXCLUIR INCIDENTE=================================
@incidente_bp.route("/incidente/delete/<int:incident_id>", methods=['POST'])
@login_required 
def delete_incident(incident_id):
    if allowed_edit_profile(current_user):
        incident = Incidente.query.get_or_404(incident_id)
        db.session.delete(incident)
        db.session.commit()
        flash('Incidente excluído com sucesso!', 'success')
        return redirect(url_for('incidente.incidents_list'))   
    else:
        flash('Acesso negado: Você não tem permissão para excluir este incidente.', 'danger')
        return redirect(url_for('incidente.incident_view', incident_id=incident_id))

#=================================PESQUISAR INCIDENTE=================================
@incidente_bp.route("/incidente/pesquisar", methods=['GET'])
@login_required
def search_incident():
    termo = request.args.get('termo', '')
    if not termo: return redirect(url_for('incidente.incidents_list'))
    query = Incidente.query
    search_terms = f"%{termo}%"
    filters = [Incidente.incident_type.ilike(search_terms), Incidente.report_number.ilike(search_terms), Incidente.ticket_number.ilike(search_terms), Incidente.btl.ilike(search_terms), Incidente.cpa.ilike(search_terms), Incidente.cia.ilike(search_terms), Incidente.description.ilike(search_terms)]
    resultados = query.filter(or_(*filters)).all()
    return render_template('incidente/incidentes.html', title=f"Resultados da pesquisa para: {termo}", incidentes=resultados)

################################################################################
#===============================OBSERVAÇÕES DO INCIDENTE========================
################################################################################

#=================================ADD OBSERVAÇÃO=================================
@incidente_bp.route("/incidente/<int:incident_id>/add_obs", methods=['POST'])
@login_required
def add_obs(incident_id):
    if allowed_edit_profile(current_user):
        texto_observacao = request.form['texto_observacao']
        user_id = current_user.id
        data_observacao = datetime.now()
        new_obs = IncidenteObs(incidente_id=incident_id, usuario_id=user_id, texto_observacao=texto_observacao, data_observacao=data_observacao)
        db.session.add(new_obs)
        db.session.commit()
        flash('Observação adicionada com sucesso!', 'success')
        return redirect(url_for('incidente.incident_view', incident_id=incident_id))
    else:
        flash('Acesso negado: Você não tem permissão para inserir uma observação.', 'danger')
        return redirect(url_for('incidente.incident_view', incident_id=incident_id))

#=================================EXCLUIR OBSERVAÇÃO=================================
@incidente_bp.route("/incidente/<int:incident_id>/delete_obs/<int:obs_id>", methods=['POST'])
@login_required
def delete_obs(incident_id, obs_id):
    obs = IncidenteObs.query.get_or_404(obs_id)
    db.session.delete(obs)
    db.session.commit()
    flash('Observação excluida com sucesso!', 'success')
    return redirect(url_for('incidente.incident_view', incident_id=incident_id))
                    
#=================================VIEW DO INCIDENTE=================================
@incidente_bp.route("/incidente/<int:incident_id>", methods=['GET'])
@login_required
def incident_view(incident_id):
    incidente = Incidente.query.get_or_404(incident_id)
    return render_template('incidente/incidente_view.html', title="Detalhes do Incidente", incidente=incidente)

#####################################################################################################
#=================================DASHBOARD=================================
#####################################################################################################
import pandas as pd
import plotly.express as px
from sqlalchemy.sql import func

@incidente_bp.route("/dashboard/incidentes_cpa_btl", methods=['GET'])
@login_required
def dashboard_incidentes_cpa_btl():
    incidents_types = TipoIncidente.query.all()
    status = StatusIncidente.query.all()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    incident_type = request.args.get('incident_type')
    status_str = request.args.get('status')
    df_filtred_incidentes_opm, filters = get_filtered_incidents_df(start_date, end_date, incident_type, status_str)
    df_bar = df_filtred_incidentes_opm
    bar_counts = df_bar.groupby(['cpa', 'btl']).size().reset_index(name='total')
    fig_bar = px.bar(bar_counts, x='cpa', y='total', color='btl', title='', labels={'cpa': 'Grande Comando', 'total': 'Incidentes'})
    fig_bar.update_layout(barmode='stack')
    bar_chart_html = fig_bar.to_html(full_html=False)
    return render_template('dashboard/incidentes_cpa_btl.html', title="Dashboard de Incidentes", start_date= filters['start_date'], end_date= filters['end_date'], incidents_types=incidents_types, status=status, bar_chart_html=bar_chart_html, filtros_aplicados=filters)
        
@incidente_bp.route("/dashboard/incidentes_status", methods=['GET'])
@login_required
def dashboard_incidentes_status():
    incidents_types = TipoIncidente.query.all()
    status = StatusIncidente.query.all()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    incident_type = request.args.get('incident_type')
    status_str = request.args.get('status')
    df_filtred, filtros_aplicados = get_filtered_incidents_df(start_date, end_date, incident_type, status_str)
    df_donut = df_filtred
    status_counts = df_donut.groupby('status_incident').size().reset_index(name='total')
    fig_donut = px.pie(status_counts, values='total', names='status_incident', hole=0.6, title='Incidentes por Status')
    fig_donut.update_traces(textposition='outside', textinfo='percent+label')
    donut_chart_html = fig_donut.to_html(full_html=False)
    total_incidents = len(df_filtred)
    total_incidentes_encerrados = len(df_filtred[df_filtred['status_incident'] == 'Encerrado'])
    total_incidentes_em_analise = len(df_filtred[df_filtred['status_incident'] == 'Em Análise'])
    total_incidentes_em_mitigacao = len(df_filtred[df_filtred['status_incident'] == 'Em Mitigação'])
    total_incidentes_falso_positivo = len(df_filtred[df_filtred['status_incident'] == 'Falso positivo'])
    totais = ({"Total" : total_incidents, "Resolvido": total_incidentes_encerrados, "Em Análise": total_incidentes_em_analise, "Aguardando": total_incidentes_em_mitigacao, "Falso Positivo": total_incidentes_falso_positivo})
    return render_template('dashboard/incidentes_status.html', title="Dashboard de Incidentes", donut_chart_html=donut_chart_html, filtros_aplicados=filtros_aplicados, incidents_types=incidents_types, status=status, totais=totais)

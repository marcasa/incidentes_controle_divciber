from app import create_app, db
from app.models import User, Incidente, IncidenteObs, Unidades, StatusIncidente, TipoIncidente
from datetime import datetime, timezone
import pytz


app = create_app()

fuso_sao_paulo = pytz.timezone('America/Sao_Paulo')

now_utc = datetime.now(timezone.utc)
now_sao_paulo = now_utc.astimezone(fuso_sao_paulo)

# print(f'Data e hora atual em São Paulo: {now_sao_paulo}')
# print(f'Data e hora atual em UTC: {now_utc}')


with app.app_context():
    print("Inserindo dados de teste no banco de dados...")
    Incidente_obs = IncidenteObs(texto_observacao='Observação 4 teste4', data_observacao= now_sao_paulo, usuario_id=2, incidente_id=1)
    db.session.add(Incidente_obs)
    db.session.commit()
    print("Dados de teste inseridos com sucesso.")
    

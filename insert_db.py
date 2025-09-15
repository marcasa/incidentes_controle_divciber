import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

from app import create_app, db
from app.models import Unidades, StatusIncidente, TipoIncidente, Incidente


load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

def import_from_csv(file_path, tb_name):
    
    app = create_app()
    
    with app.app_context():
        
        
        
            
        
        ############### IMPORTAÇÃO DE DADOS PARA A TABELA UNIDADES ####################
                
        #Iterando as linhas do DataFrame
        match tb_name:
            case 'tb_unidades':
                try:
                    df = pd.read_csv(file_path)
            
                except FileNotFoundError:
                    print(f"Erro: O arquivo {file_path} não foi encontrado.")
                    return
                except Exception as e:
                    print(f"Erro ao ler o arquivo .xlsx: {e}")
                    return
                
                for index, row in df.iterrows():
                    try:
                        new_unidade = Unidades(
                            cpa=row['cpa'],
                            btl=row['btl']
                        )
                        
                        print(f"Adicionando unidade: id={index}, CPA={row['cpa']}, BTL={row['btl']}")
                        db.session.add(new_unidade)
                    except KeyError as e:
                        print(f"Erro de importação na linha {index + 1}: Coluna {e.args[0]} não encontrada. Pulando linha")
                        continue
                    except Exception as e:
                        print(f"Erro inesperado na linha {index + 1}: {e}. Pulando linha")
                        continue
                # Comitando todas as adições de uma vez
                db.session.commit()
                print("Importação concluída com sucesso.")
                
            case 'tb_status':
                pass
                
            case 'tb_tipos':
                pass                
            
            case 'tb_incidentes':
                for index, row in df.iterrows():
                    try:
                        new_incidente = Incidente(
                            id = row['Id'],
                            incident_type = row['incident_type'],
                            report_number = row['report_number'],
                            ticket_number = row['ticket_number'],
                            cpa = row['cpa'],
                            btl = row['btl'],
                            cia = row['cia'],
                            description = row['description'],
                            start_date = row['start_date'],
                            end_date = row['end_date'],
                            status_incident = row['status_incident'],
                            user_id = row['user_id']
                        )
                        db.session.add(new_incidente)
                        print(f"Adicionando incidente: id={Incidente.id}")
                    except KeyError as e:
                        print(f"Erro de importação na linha {index + 1}: Coluna {e.args[0]} não encontrada. Pulando linha")
                        continue
                    except Exception as e:
                        print(f"Erro inesperado na linha {index + 1}: {e}. Pulando linha")
                        continue
                #Comitando todas as adições de uma vez
                db.session.commit()
                print("Importação concluída com sucesso.")                
            
            case _:
                print("Tabela inválida.")            
        
        ##############################################################################
        ############### IMPORTAÇÃO DE DADOS PARA A TABELA STATUS ####################
        ############################################################################## 
        # for index, row in df.iterrows():
        #     try:
        #         new_status = StatusIncidente(
        #             status = row['status'],
        #             desc_status = row['descricao']
        #         )
        #         db.session.add(new_status)
        #         print(f"Adicionando status: id={index}, Status={row['status']}, Descrição={row['descricao']}")
        #     except KeyError as e:
        #         print(f"Erro de importação na linha {index + 1}: Coluna {e.args[0]} não encontrada. Pulando linha")
        #         continue
        #     except Exception as e:
        #         print(f"Erro inesperado na linha {index + 1}: {e}. Pulando linha")
        #         continue
        # # Comitando todas as adições de uma vez
        # db.session.commit()
        # print("Importação concluída com sucesso.")
        
        ##############################################################################
        ############### IMPORTAÇÃO DE DADOS PARA A TABELA TIPOS DE INCIDENTE ####################
        ############################################################################## 
        # for index, row in df.iterrows():
        #     try:
        #         new_tp_incidente = TipoIncidente(
        #             tipo_incidente = row['tipo_incidente'],
        #             desc_incidente = row['descricao']
        #         )
        #         db.session.add(new_tp_incidente)
        #         print(f"Adicionando Tipo de incidente: id={index}, Tipo Incidente={row['tipo_incidente']}, Descrição={row['descricao']}")
        #     except KeyError as e:
        #         print(f"Erro de importação na linha {index + 1}: Coluna {e.args[0]} não encontrada. Pulando linha")
        #         continue
        #     except Exception as e:
        #         print(f"Erro inesperado na linha {index + 1}: {e}. Pulando linha")
        #         continue
        # # Comitando todas as adições de uma vez
        # db.session.commit()
        # print("Importação concluída com sucesso.")
        
        
        
        ##############################################################################
        ############### IMPORTAÇÃO DE DADOS PARA A TABELA INCIDENTE ####################
        ############################################################################## 
        
        

if __name__ == '__main__':
    csv_file_path = 'tb_unidades.csv' 
    import_from_csv(csv_file_path, "tb_unidades")        
            

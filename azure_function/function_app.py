import logging
import azure.functions as func
import pyodbc
import struct
import os
import smtplib
from email.message import EmailMessage
from azure.identity import DefaultAzureCredential
from etl.etl_projetos import executar_etl  

app = func.FunctionApp()

def enviar_email(assunto, corpo):
    msg = EmailMessage()
    msg.set_content(corpo)
    msg['Subject'] = assunto
    msg['From'] = "joao.modesto12373@gmail.com"  # Configure um e-mail de remetente
    msg['To'] = "joao.modesto12373@gmail.com"

    try:
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("joao.modesto12373@gmail.com", "ncyc qyah weqj liru")
            smtp.send_message(msg)
        logging.info("E-mail de status enviado com sucesso.")
    except Exception as e:
        logging.error(f"Falha ao enviar e-mail: {e}")

def atualizar_kpis():
    # Obtém credenciais automáticas da Azure Function
    credential = DefaultAzureCredential()
    token = credential.get_token("https://database.windows.net/.default")
    token_bytes = token.token.encode("utf-16-le")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

    conn_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:db-projetos.database.windows.net,1433;"
        "Database=db_gestao_projetos;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

    try:
        with pyodbc.connect(conn_str, attrs_before={1256: token_struct}) as conn:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            sql_path = os.path.join(BASE_DIR, "database", "KPIs.sql")
            with open(sql_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
            conn.execute(sql_script)
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Erro ao atualizar KPIs no SQL: {e}")
        return False

@app.timer_trigger(schedule="0 0 12,20 * * *", arg_name="myTimer", run_on_startup=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    hora_atual = "12h" if myTimer.schedule_status and "12:00" in str(myTimer.schedule_status) else "20h"
    status_report = []

    logging.info(f"Iniciando processamento das {hora_atual}...")

    # Passo 1: Rodar ETL
    try:
        executar_etl()
        status_report.append("ETL de Projetos: SUCESSO")
    except Exception as e:
        status_report.append(f"ETL de Projetos: FALHA ({e})")

    # Passo 2: Rodar SQL de KPIs
    if atualizar_kpis():
        status_report.append("Atualização de KPIs SQL: SUCESSO")
    else:
        status_report.append("Atualização de KPIs SQL: FALHA")

    # Passo 3: Enviar E-mail
    corpo_email = f"Relatório de Atualização - {hora_atual}\n\n" + "\n".join(status_report)
    assunto = f"Status ETL/KPI - {hora_atual}"
    enviar_email(assunto, corpo_email)

#versão 2.0
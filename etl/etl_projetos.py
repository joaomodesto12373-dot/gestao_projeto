import pandas as pd
import pyodbc
from datetime import datetime


df = pd.read_csv("../../data/projetos.csv")
hoje = pd.to_datetime(datetime.today().date())

df["data_inicio"] = pd.to_datetime(df["data_inicio"])
df["data_fim_prevista"] = pd.to_datetime(df["data_fim_prevista"])

df["desvio_custo"] = df["custo_real"] - df["custo_orcado"]

df["status_atraso"] = df["data_fim_prevista"].apply(
    lambda data: "Atrasado" if data < hoje else "No Prazo"
)


connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:db-projetos.database.windows.net,1433;"
    "Database=db_gestao_projetos;"
    "Authentication=ActiveDirectoryInteractive;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


insert_query = """
INSERT INTO Projetos (
    id_projeto,
    nome_projeto,
    gerente,
    data_inicio,
    data_fim_prevista,
    custo_orcado,
    custo_real,
    percentual_conclusao,
    desvio_custo,
    status_atraso
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        int(row["id_projeto"]),
        row["nome_projeto"],
        row["gerente"],
        row["data_inicio"],
        row["data_fim_prevista"],
        float(row["custo_orcado"]),
        float(row["custo_real"]),
        int(row["percentual_conclusao"]),
        float(row["desvio_custo"]),
        row["status_atraso"]
    )

conn.commit()
conn.close()

print("ETL executado com sucesso via Azure AD.")

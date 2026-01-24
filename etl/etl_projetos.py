import pandas as pd
import pyodbc
import struct
from datetime import datetime
from azure.identity import InteractiveBrowserCredential

# ==============================
# 1. EXTRAÇÃO
# ==============================
df = pd.read_csv("data/projetos.csv")

# ==============================
# 2. TRANSFORMAÇÃO
# ==============================
hoje = pd.to_datetime(datetime.today().date())

df["data_inicio"] = pd.to_datetime(df["data_inicio"])
df["data_fim_prevista"] = pd.to_datetime(df["data_fim_prevista"])

# Cálculos de transformação
df["desvio_custo"] = df["custo_real"] - df["custo_orcado"]

df["status_atraso"] = df["data_fim_prevista"].apply(
    lambda data: "Atrasado" if data < hoje else "No Prazo"
)

# ==============================
# 3. CONEXÃO AZURE SQL (Via Token/MFA)
# ==============================
print("Solicitando autenticação via Browser...")
credential = InteractiveBrowserCredential()
token = credential.get_token("https://database.windows.net/.default")

# Preparação do token binário para o Driver ODBC
token_bytes = token.token.encode("utf-16-le")
token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

# String de conexão limpa (sem Uid ou Authentication para não conflitar com o Token)
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:db-projetos.database.windows.net,1433;"
    "Database=db_gestao_projetos;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Conectar e injetar o Token no atributo 1256 (SQL_COPT_AS_ACCESS_TOKEN)
conn = pyodbc.connect(connection_string, attrs_before={1256: token_struct})
cursor = conn.cursor()

# ==============================
# 4. CARGA
# ==============================
# Verifique se as colunas 'desvio_custo' e 'status_atraso' existem na sua tabela SQL
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

print(f"Iniciando a carga de {len(df)} linhas...")

try:
    for _, row in df.iterrows():
        cursor.execute(
            insert_query,
            int(row["id_projeto"]),
            row["nome_projeto"],
            row["gerente"],
            row["data_inicio"].strftime('%Y-%m-%d'), # Formata data para o SQL
            row["data_fim_prevista"].strftime('%Y-%m-%d'),
            float(row["custo_orcado"]),
            float(row["custo_real"]),
            int(row["percentual_conclusao"]),
            float(row["desvio_custo"]),
            row["status_atraso"]
        )

    conn.commit()
    print("ETL executado com sucesso via Azure AD Token.")
except Exception as e:
    print(f"Erro durante a carga: {e}")
    conn.rollback()
finally:
    conn.close()
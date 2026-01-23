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

print(df)

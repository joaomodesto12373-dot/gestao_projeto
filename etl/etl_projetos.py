import pandas as pd
from datetime import datetime

df = pd.read_csv("../../data/projetos.csv")

# Datas
hoje = pd.to_datetime(datetime.today().date())
df["data_fim_prevista"] = pd.to_datetime(df["data_fim_prevista"])

# Regras de negócio
df["desvio_custo"] = df["custo_real"] - df["custo_orcado"]
df["status_atraso"] = df["data_fim_prevista"].apply(
    lambda x: "Atrasado" if x < hoje else "No Prazo"
)

print(df)

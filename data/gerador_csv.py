import csv
import random
from datetime import datetime, timedelta

# Configurações iniciais
gerentes = ['Carlos', 'Ana', 'João', 'Marina', 'Ricardo']
projetos_nomes = ['Obra', 'Reforma', 'Expansão', 'Manutenção', 'Instalação']
status_nomes = ['Alpha', 'Beta', 'Gama', 'Delta']

def gerar_data(base_date, dias_range):
    return (base_date + timedelta(days=random.randint(0, dias_range))).strftime('%Y-%m-%d')

with open('projetos.csv', mode='w', newline='', encoding='utf-8') as arquivo:
    escritor = csv.writer(arquivo)
    # Cabeçalho
    escritor.writerow(['id_projeto', 'nome_projeto', 'gerente', 'data_inicio', 'data_fim_prevista', 'custo_orcado', 'custo_real', 'percentual_conclusao'])
    
    data_base = datetime(2024, 1, 1)

    for i in range(1, 201):
        # Lógica 
        inicio = data_base + timedelta(days=random.randint(0, 300))
        fim_prevista = inicio + timedelta(days=random.randint(30, 180))
        
        orcado = random.randrange(50000, 500000, 5000)
        # Custo real flutua em torno do orçado (entre 80% e 120%)
        real = int(orcado * random.uniform(0.8, 1.2))
        conclusao = random.randint(0, 100)
        
        nome = f"{random.choice(projetos_nomes)} {random.choice(status_nomes)} {i}"
        
        escritor.writerow([
            i, 
            nome, 
            random.choice(gerentes), 
            inicio.strftime('%Y-%m-%d'), 
            fim_prevista.strftime('%Y-%m-%d'), 
            orcado, 
            real, 
            conclusao
        ])

print("Arquivo 'projetos.csv' gerado com sucesso com 200 linhas!")
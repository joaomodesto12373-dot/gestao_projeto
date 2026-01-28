# gestao_projeto

Este repositório apresenta uma solução end-to-end para análise e otimização da gestão de projetos, desenvolvida com foco em automação, qualidade de dados e suporte à tomada de decisão gerencial. O projeto implementa um pipeline de Business Intelligence (BI) automatizado, utilizando uma arquitetura baseada em nuvem para processar dados de projetos e calcular Key Performance Indicators (KPIs) em tempo real.

## 🚀 Visão Geral e Arquitetura

O projeto utiliza uma arquitetura de engenharia de dados que orquestra a extração, transformação e carga (ETL) de dados de projetos para um banco de dados analítico.

O fluxo de trabalho é o seguinte:

1. **Extração e Transformação (ETL):** Um script Python (`etl/etl_projetos.py`) processa dados de projetos (atualmente de um CSV) e calcula métricas financeiras e de prazo.

1. **Carga (Load):** Os dados transformados são carregados em um banco de dados Azure SQL, utilizando autenticação segura via Azure AD Token.

1. **Cálculo de KPIs:** Scripts SQL (`database/KPIs.sql`) são executados para calcular métricas avançadas (como Valor Agregado Líquido e Farol de Criticidade).

1. **Automação:** Uma Azure Function orquestra a execução agendada do ETL e do cálculo de KPIs, enviando um e-mail de status ao final.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia | Finalidade |
| --- | --- | --- |
| **Linguagem** | Python | Scripts ETL e Automação |
| **Processamento** | Pandas | Manipulação e Transformação de Dados |
| **Banco de Dados** | Azure SQL Database | Armazenamento e Cálculo de KPIs |
| **Automação** | Azure Functions | Orquestração e Agendamento do Pipeline |
| **Conectividade** | pyodbc, azure-identity | Conexão segura via Azure AD Token |
| **Notificação** | smtplib | Envio de Alertas de Status |

## Funcionalidades Principais

- **ETL Robusto:** Cálculo de desvio de custo e status de atraso (`etl/etl_projetos.py`).

- **KPIs Gerenciais:** Definição de métricas de negócio avançadas, incluindo **Valor Agregado Líquido** e um **Farol de Criticidade** automatizado (`database/KPIs.sql`).

- **Automação Agendada:** Execução diária (12h e 20h) do pipeline completo via Timer Trigger da Azure Function.

- **Segurança em Nuvem:** Uso de `DefaultAzureCredential` para autenticação no Azure SQL, seguindo as melhores práticas de segurança em ambientes Azure.

## 📂 Estrutura do Projeto

```
.
├── README.md
├── azure_function/
│   ├── etl/
│   ├── function_app.py  # Orquestração e Timer Trigger
│   ├── host.json
│   └── requirements.txt
├── data/
│   ├── gerador_csv.py   # Script para gerar dados de exemplo
│   └── projetos.csv     # Fonte de dados de entrada
├── database/
│   ├── KPIs.sql         # Script SQL para cálculo de KPIs
│   └── criar_tabelas.sql # Script SQL para criação das tabelas
├── etl/
│   └── etl_projetos.py  # Lógica principal de Extração e Transformação
└── requirements.txt     # Dependências do projeto principal
```

## Configuração e Instalação

### Pré-requisitos

- Python 3.x

- Acesso a um **Azure SQL Database** e permissões para usar a autenticação **Azure AD**.

- Configuração de um **ODBC Driver 18 for SQL Server** no ambiente de execução.

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/joaomodesto12373-dot/gestao_projeto.git
   cd gestao_projeto
   ```

1. Instale as dependências Python:

   ```bash
   pip install -r requirements.txt
   ```

### Configuração do Azure SQL

1. Execute o script `database/criar_tabelas.sql` no seu Azure SQL Database para criar a tabela `Projetos`.

1. **Ajuste a Conexão:** No arquivo `etl/etl_projetos.py`, atualize a `connection_string` (linhas 39-46 ) com o nome do seu servidor e banco de dados.

### Configuração da Azure Function

1. Ajuste o agendamento do Timer Trigger em `azure_function/function_app.py` (linha 54) se necessário.

1. **Segurança de E-mail:** **Recomendação:** Armazene as credenciais de e-mail (linha 22) em um serviço seguro como o Azure Key Vault e acesse-as via variáveis de ambiente, em vez de deixá-las *hardcoded*.

## Execução

O pipeline é projetado para ser executado automaticamente pela Azure Function.

Para testes locais do ETL:

```bash
python etl/etl_projetos.py
```

**Nota:** A execução local do `etl_projetos.py` exigirá autenticação interativa via navegador para obter o Azure AD Token.

---

**

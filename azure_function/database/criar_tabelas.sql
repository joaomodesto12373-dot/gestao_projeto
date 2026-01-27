CREATE TABLE Projetos (
    id_projeto INT PRIMARY KEY,
    nome_projeto VARCHAR(100),
    gerente VARCHAR(50),
    data_inicio DATE,
    data_fim_prevista DATE,
    custo_orcado DECIMAL(12,2),
    custo_real DECIMAL(12,2),
    percentual_conclusao INT,
    desvio_custo DECIMAL(12,2),
    status_atraso VARCHAR(20)
);
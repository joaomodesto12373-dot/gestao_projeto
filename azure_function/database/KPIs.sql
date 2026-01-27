CREATE OR ALTER VIEW dbo.vw_KPIs_Projetos AS
SELECT 
    id_projeto,
    nome_projeto,
    gerente,
    custo_orcado,
    custo_real,
    percentual_conclusao,
    -- Variância de Custo (Valores negativos = prejuízo)
    (custo_orcado * (percentual_conclusao / 100.0)) - custo_real AS valor_agregado_liquido,
    
    -- Status Financeiro
    CASE 
        WHEN custo_real > custo_orcado THEN 'Acima do Orçamento'
        WHEN custo_real = custo_orcado THEN 'No Orçamento'
        ELSE 'Abaixo do Orçamento'
    END AS status_financeiro,

    -- Farol de Criticidade (Lógica Automática)
    CASE 
        WHEN percentual_conclusao < 100 AND data_fim_prevista < GETDATE() THEN 'Crítico (Atrasado)'
        WHEN percentual_conclusao < 40 AND DATEDIFF(day, data_inicio, data_fim_prevista) > 30 THEN 'Atenção'
        ELSE 'Saudável'
    END AS farol_projeto
FROM dbo.Projetos;
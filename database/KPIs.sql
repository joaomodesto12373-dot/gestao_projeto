SELECT 
    nome_projeto,
    gerente,
    custo_orcado,
    custo_real,
    (custo_real - custo_orcado) AS variancia_custo,
    ((custo_real - custo_orcado) / NULLIF(custo_orcado, 0)) * 100 AS percentual_desvio
FROM Projetos;

SELECT *,
    CASE 
        WHEN percentual_conclusao < 100 AND data_fim_prevista < GETDATE() THEN 'Atrasado'
        WHEN percentual_conclusao < 50 AND DATEDIFF(day, data_inicio, GETDATE()) > DATEDIFF(day, GETDATE(), data_fim_prevista) THEN 'Risco de Atraso'
        WHEN percentual_conclusao = 100 THEN 'Concluído'
        ELSE 'Em Dia'
    END AS status_cronograma
FROM Projetos;
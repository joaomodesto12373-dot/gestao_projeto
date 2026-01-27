-- Cria um usuário no banco vinculado à sua Function
CREATE USER [name_app] FROM EXTERNAL PROVIDER;

-- Dá permissão de leitura, escrita e execução (necessário para atualizar KPIs)
ALTER ROLE db_datareader ADD MEMBER [name_app];
ALTER ROLE db_datawriter ADD MEMBER [name_app];
ALTER ROLE db_ddladmin ADD MEMBER [name_app]; -- Se o seu script criar tabelas

-- Concede as permissões necessárias para ler e gravar dados
ALTER ROLE db_datareader ADD MEMBER [name_app];
ALTER ROLE db_datawriter ADD MEMBER [name_app];

-- Para executar scripts DDL 
ALTER ROLE db_ddladmin ADD MEMBER [name_app];
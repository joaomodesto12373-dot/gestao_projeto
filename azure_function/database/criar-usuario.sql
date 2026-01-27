-- Cria um usuário no banco vinculado à sua Function
CREATE USER [app-function] FROM EXTERNAL PROVIDER;

-- Dá permissão de leitura, escrita e execução (necessário para atualizar KPIs)
ALTER ROLE db_datareader ADD MEMBER [app-function];
ALTER ROLE db_datawriter ADD MEMBER [app-function];
ALTER ROLE db_ddladmin ADD MEMBER [app-function]; -- Se o seu script criar tabelas
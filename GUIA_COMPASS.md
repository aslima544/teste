# GUIA: MIGRAÇÃO VIA MONGODB COMPASS

## PASSO A PASSO:

### 1. INSTALAR MONGODB COMPASS
- Download: https://www.mongodb.com/try/download/compass

### 2. CONECTAR AO BANCO LOCAL
- Abra o Compass
- Conecte em: mongodb://localhost:27017
- Selecione database: consultorio_db

### 3. EXPORTAR DADOS
Para cada coleção (users, patients, doctors, appointments, consultorios):
- Clique na coleção
- Clique em "Export Data"
- Escolha formato JSON
- Salve o arquivo

### 4. CONECTAR AO ATLAS
- Pegue a connection string do Atlas
- Conecte no Compass usando a URL do Atlas

### 5. IMPORTAR DADOS
Para cada coleção:
- Vá na coleção correspondente no Atlas
- Clique em "Import Data"
- Selecione o arquivo JSON exportado
- Confirme a importação

### 6. VERIFICAR
- Confirme se todos os dados foram importados
- Teste o login no Railway
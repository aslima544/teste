# Contratos de API - Sistema de Gestão de Consultórios

## 1. DADOS MOCKADOS A SUBSTITUIR

### Frontend Mock Data (`/src/mock/mockData.js`):
- `consultoriosFixos`: Array com consultórios C1-C5 (ESF)
- `cronogramaSemanal`: Objeto com cronograma dos consultórios C6-C8
- `especialidades`: Lista de especialidades disponíveis
- `agendamentosHoje`: Agendamentos do dia atual
- `dadosHistoricos`: Dados históricos para relatórios
- `visitasDomiciliares`: Cronograma de visitas domiciliares
- `gerarAgendamentosMock()`: Função que gera dados dinâmicos

## 2. API ENDPOINTS A IMPLEMENTAR

### 2.1 Consultórios
```
GET /api/consultorios
- Retorna todos os consultórios (fixos + variáveis)
- Response: { fixos: [], variaveis: [] }

PUT /api/consultorios/{id}/cronograma
- Atualiza cronograma de consultório variável
- Body: { dia, especialidade, periodo, horario }
```

### 2.2 Cronograma Semanal
```
GET /api/cronograma/semanal
- Retorna cronograma completo da semana
- Response: { segunda: {}, terca: {}, ... }

PUT /api/cronograma/semanal
- Atualiza cronograma semanal
- Body: { dia, consultorio, dados }
```

### 2.3 Agendamentos
```
GET /api/agendamentos
- Lista agendamentos por data
- Query: ?data=YYYY-MM-DD
- Response: [{ id, consultorio, paciente, horario, status, especialidade }]

POST /api/agendamentos
- Cria novo agendamento
- Body: { consultorio, paciente, horario, especialidade }

PUT /api/agendamentos/{id}
- Atualiza status do agendamento
- Body: { status }

DELETE /api/agendamentos/{id}
- Remove agendamento
```

### 2.4 Especialidades
```
GET /api/especialidades
- Lista todas as especialidades disponíveis
- Response: [{ id, nome, tipo }]
```

### 2.5 Relatórios
```
GET /api/relatorios/ocupacao
- Taxa de ocupação por consultório
- Query: ?periodo=semana|mes|personalizado&inicio=DATE&fim=DATE
- Response: [{ consultorio, ocupacao, atendimentos }]

GET /api/relatorios/especialidades
- Performance por especialidade
- Response: [{ nome, atendimentos, satisfacao }]

GET /api/relatorios/tempo-espera
- Tempo de espera por período
- Response: [{ periodo, tempoMedio }]

GET /api/relatorios/historico
- Dados históricos para análises
- Response: [{ data, consultorio, especialidade, atendimentos, ocupacao }]
```

### 2.6 Dashboard Stats
```
GET /api/stats/dashboard
- Estatísticas principais do dashboard
- Response: { 
    consultoriosAtivos, 
    atendimentosHoje, 
    taxaOcupacao, 
    horarioAtual 
  }
```

## 3. MODELOS DE DADOS (MongoDB)

### 3.1 Consultorio
```javascript
{
  _id: ObjectId,
  codigo: String, // C1, C2, etc.
  nome: String,
  tipo: String, // 'fixo' | 'variavel'
  ocupacaoFixa: String, // para fixos: ESF 1, ESF 2, etc.
  horarioPadrao: String, // 07h-16h, etc.
  cor: String, // para UI
  ativo: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

### 3.2 CronogramaSemanal
```javascript
{
  _id: ObjectId,
  consultorio: String, // C6, C7, C8
  dia: String, // segunda, terca, etc.
  especialidade: String,
  periodo: String, // Manhã, Tarde, Integral, etc.
  horario: String, // 08h-17h
  ativo: Boolean,
  semanaReferencia: String, // YYYY-WW
  createdAt: Date,
  updatedAt: Date
}
```

### 3.3 Agendamento
```javascript
{
  _id: ObjectId,
  consultorio: String,
  paciente: String,
  especialidade: String,
  data: Date,
  horario: String,
  status: String, // confirmado, em_atendimento, aguardando, concluido, cancelado
  tipo: String, // consulta, exame, etc.
  observacoes: String,
  createdAt: Date,
  updatedAt: Date
}
```

### 3.4 Especialidade
```javascript
{
  _id: ObjectId,
  nome: String,
  tipo: String, // esf, especialista, apoio
  cor: String,
  ativo: Boolean,
  createdAt: Date
}
```

### 3.5 RelatorioHistorico
```javascript
{
  _id: ObjectId,
  data: Date,
  consultorio: String,
  especialidade: String,
  totalAgendamentos: Number,
  atendimentosRealizados: Number,
  taxaOcupacao: Number,
  tempoMedioEspera: Number,
  satisfacaoMedia: Number,
  createdAt: Date
}
```

## 4. INTEGRAÇÃO FRONTEND/BACKEND

### 4.1 Substituições no Frontend:
1. **Dashboard.js**: Substituir dados mockados por chamadas API
   - `consultoriosFixos` → `GET /api/consultorios`
   - `cronogramaSemanal` → `GET /api/cronograma/semanal`
   - `agendamentosHoje` → `GET /api/agendamentos?data=hoje`

2. **WeeklyView.js**: Integrar edição de cronograma
   - Carregar dados: `GET /api/cronograma/semanal`
   - Salvar mudanças: `PUT /api/cronograma/semanal`

3. **DailyView.js**: Agendamentos em tempo real
   - Listar: `GET /api/agendamentos?data=YYYY-MM-DD`
   - Criar: `POST /api/agendamentos`
   - Atualizar status: `PUT /api/agendamentos/{id}`

4. **ReportsView.js**: Relatórios dinâmicos
   - Ocupação: `GET /api/relatorios/ocupacao`
   - Especialidades: `GET /api/relatorios/especialidades`
   - Histórico: `GET /api/relatorios/historico`

### 4.2 Utilitário API (criar `/src/services/api.js`):
```javascript
// Centralizará todas as chamadas API
// Configurará axios com baseURL
// Gerenciará erros e loading states
```

### 4.3 Context/State Management:
- Criar context para dados globais (consultórios, especialidades)
- Implementar cache local para reduzir requisições
- Adicionar states de loading e error

## 5. FUNCIONALIDADES DE NEGÓCIO

### 5.1 Validações:
- Não permitir sobreposição de agendamentos
- Validar horários dentro do funcionamento do consultório
- Verificar disponibilidade antes de agendar

### 5.2 Regras de Negócio:
- Consultórios C1-C5 são fixos (não editáveis)
- Consultórios C6-C8 podem ter cronograma alterado
- C8 é consultório coringa (backup)
- Visitas domiciliares liberam consultórios (segunda e quarta)

### 5.3 Relatórios Automáticos:
- Gerar dados históricos diários automaticamente
- Calcular métricas de ocupação
- Compilar estatísticas de satisfação

## 6. PRIORIDADE DE IMPLEMENTAÇÃO

1. **Fase 1**: Modelos básicos + endpoints de consultórios e cronograma
2. **Fase 2**: Sistema de agendamentos completo
3. **Fase 3**: Relatórios e dados históricos
4. **Fase 4**: Otimizações e funcionalidades avançadas

## 7. TESTES NECESSÁRIOS

- Validação de sobreposição de horários
- Testes de carga para múltiplos agendamentos simultâneos
- Validação de integridade dos dados de relatório
- Testes de performance para consultas de histórico
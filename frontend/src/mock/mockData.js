// Mock data para sistema de gestão de consultórios

export const consultoriosFixos = [
  {
    id: 'C1',
    nome: 'Consultório 1',
    ocupacao: 'ESF 1',
    horario: '07h - 16h',
    tipo: 'fixo',
    cor: '#4F46E5'
  },
  {
    id: 'C2', 
    nome: 'Consultório 2',
    ocupacao: 'ESF 2',
    horario: '07h - 16h',
    tipo: 'fixo',
    cor: '#059669'
  },
  {
    id: 'C3',
    nome: 'Consultório 3', 
    ocupacao: 'ESF 3',
    horario: '08h - 17h',
    tipo: 'fixo',
    cor: '#DC2626'
  },
  {
    id: 'C4',
    nome: 'Consultório 4',
    ocupacao: 'ESF 4', 
    horario: '10h - 19h',
    tipo: 'fixo',
    cor: '#7C2D12'
  },
  {
    id: 'C5',
    nome: 'Consultório 5',
    ocupacao: 'ESF 5',
    horario: '12h - 21h',
    tipo: 'fixo',
    cor: '#581C87'
  }
];

export const cronogramaSemanal = {
  segunda: {
    C6: { especialidade: 'Cardiologia', periodo: 'Manhã/Tarde', horario: '08h-17h' },
    C7: { especialidade: 'Médico Apoio', periodo: 'Integral', horario: '07h-16h' },
    C8: { especialidade: 'E-MULTI', periodo: 'Manhã/Tarde', horario: '08h-17h' }
  },
  terca: {
    C6: { especialidade: 'Acupuntura', periodo: 'Manhã/Tarde', horario: '08h-17h' },
    C7: { especialidade: 'Cardiologia', periodo: 'Tarde', horario: '13h-17h' },
    C8: { especialidade: 'Médico Apoio', periodo: 'Integral', horario: '07h-16h' }
  },
  quarta: {
    C6: { especialidade: 'Cardiologia', periodo: 'Manhã/Tarde', horario: '08h-17h' },
    C7: { especialidade: 'Pediatria (manhã) / Acupuntura (tarde)', periodo: 'Integral', horario: '08h-17h' },
    C8: { especialidade: 'E-MULTI', periodo: 'Manhã/Tarde', horario: '08h-17h' }
  },
  quinta: {
    C6: { especialidade: 'Ginecologista (tarde) / Cardiologia (manhã)', periodo: 'Integral', horario: '08h-17h' },
    C7: { especialidade: 'Pediatria (manhã) / Acupuntura (tarde)', periodo: 'Integral', horario: '08h-17h' },
    C8: { especialidade: 'Médico Apoio', periodo: 'Integral', horario: '07h-16h' }
  },
  sexta: {
    C6: { especialidade: 'Acupuntura', periodo: 'Manhã/Tarde', horario: '08h-17h' },
    C7: { especialidade: 'Médico Apoio', periodo: 'Integral', horario: '07h-16h' },
    C8: { especialidade: 'Apoio/Reserva', periodo: 'Disponível', horario: 'Conforme demanda' }
  }
};

export const especialidades = [
  'Cardiologia',
  'Acupuntura', 
  'Pediatria',
  'Ginecologista',
  'E-MULTI',
  'Médico Apoio',
  'Apoio/Reserva',
  'ESF 1',
  'ESF 2', 
  'ESF 3',
  'ESF 4',
  'ESF 5'
];

export const agendamentosHoje = [
  {
    id: 1,
    consultorio: 'C1',
    paciente: 'Maria Silva Santos',
    especialidade: 'ESF 1',
    horario: '08:00',
    status: 'confirmado',
    tipo: 'consulta'
  },
  {
    id: 2,
    consultorio: 'C6', 
    paciente: 'João Carlos Oliveira',
    especialidade: 'Cardiologia',
    horario: '09:30',
    status: 'em_atendimento',
    tipo: 'consulta'
  },
  {
    id: 3,
    consultorio: 'C8',
    paciente: 'Ana Paula Costa',
    especialidade: 'E-MULTI', 
    horario: '10:00',
    status: 'aguardando',
    tipo: 'consulta'
  },
  {
    id: 4,
    consultorio: 'C2',
    paciente: 'Pedro Henrique',
    especialidade: 'ESF 2',
    horario: '11:00', 
    status: 'confirmado',
    tipo: 'consulta'
  }
];

export const dadosHistoricos = [
  {
    data: '2024-01-15',
    consultorio: 'C6',
    especialidade: 'Cardiologia',
    atendimentos: 12,
    ocupacao: '85%'
  },
  {
    data: '2024-01-15',
    consultorio: 'C7', 
    especialidade: 'Médico Apoio',
    atendimentos: 15,
    ocupacao: '92%'
  },
  {
    data: '2024-01-15',
    consultorio: 'C8',
    especialidade: 'E-MULTI',
    atendimentos: 8,
    ocupacao: '65%'
  }
];

export const visitasDomiciliares = [
  {
    dia: 'segunda',
    equipes: ['ESF 1', 'ESF 3'],
    horario: '08h-12h',
    status: 'ativo'
  },
  {
    dia: 'quarta',
    equipes: ['ESF 2', 'ESF 4'],
    horario: '09h-15h', 
    status: 'ativo'
  }
];

// Função para gerar dados mockados dinâmicos
export const gerarAgendamentosMock = (data) => {
  const horarios = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00'];
  const pacientes = [
    'Maria Silva', 'João Santos', 'Ana Costa', 'Pedro Oliveira',
    'Julia Lima', 'Carlos Ferreira', 'Lucia Mendes', 'Roberto Dias'
  ];
  
  return horarios.map((horario, index) => ({
    id: index + 1,
    consultorio: ['C1', 'C2', 'C6', 'C7'][index % 4],
    paciente: pacientes[index % pacientes.length],
    horario: horario,
    status: ['confirmado', 'em_atendimento', 'aguardando'][index % 3],
    data: data
  }));
};
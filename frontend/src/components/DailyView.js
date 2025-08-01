import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Calendar, ChevronLeft, ChevronRight, Clock, Users, Plus } from 'lucide-react';
import { consultoriosFixos, cronogramaSemanal, gerarAgendamentosMock } from '../mock/mockData';

const DailyView = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [agendamentos, setAgendamentos] = useState([]);
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    // Gerar agendamentos mock para a data selecionada
    const mockData = gerarAgendamentosMock(selectedDate.toISOString().split('T')[0]);
    setAgendamentos(mockData);

    // Timer para atualizar horário atual
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 30000); // Atualiza a cada 30 segundos

    return () => clearInterval(timer);
  }, [selectedDate]);

  const getDiaSemanaNome = (date) => {
    const dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
    return dias[date.getDay()];
  };

  const getAllConsultoriosDisponíveis = () => {
    const diaAtual = getDiaSemanaNome(selectedDate);
    const consultoriosHoje = [...consultoriosFixos];
    
    // Adicionar consultórios variáveis conforme cronograma
    if (cronogramaSemanal[diaAtual]) {
      Object.entries(cronogramaSemanal[diaAtual]).forEach(([consultorio, info]) => {
        consultoriosHoje.push({
          id: consultorio,
          nome: consultorio,
          ocupacao: info.especialidade,
          horario: info.horario,
          tipo: 'variavel',
          periodo: info.periodo
        });
      });
    }

    return consultoriosHoje;
  };

  const getStatusConsultorio = (consultorioId) => {
    const agendamentosConsultorio = agendamentos.filter(a => a.consultorio === consultorioId);
    const horaAtual = currentTime.getHours() * 100 + currentTime.getMinutes();
    
    for (const agendamento of agendamentosConsultorio) {
      const [hora, minuto] = agendamento.horario.split(':').map(Number);
      const horarioAgendamento = hora * 100 + minuto;
      
      if (Math.abs(horarioAgendamento - horaAtual) <= 50) { // 50 minutos de tolerância
        return agendamento.status;
      }
    }
    
    return 'livre';
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'em_atendimento': return 'bg-green-100 text-green-800 border-green-200';
      case 'confirmado': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'aguardando': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'livre': return 'bg-gray-100 text-gray-600 border-gray-200';
      default: return 'bg-gray-100 text-gray-600 border-gray-200';
    }
  };

  const navigateDate = (direction) => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + direction);
    setSelectedDate(newDate);
  };

  const horarios = [
    '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'
  ];

  const AddAppointmentDialog = () => {
    const [formData, setFormData] = useState({
      consultorio: '',
      paciente: '',
      horario: '',
      tipo: 'consulta'
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      const novoAgendamento = {
        id: Date.now(),
        ...formData,
        status: 'confirmado',
        data: selectedDate.toISOString().split('T')[0]
      };
      
      setAgendamentos(prev => [...prev, novoAgendamento]);
      setIsAddDialogOpen(false);
      setFormData({ consultorio: '', paciente: '', horario: '', tipo: 'consulta' });
    };

    return (
      <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Novo Agendamento</DialogTitle>
            <DialogDescription>
              {selectedDate.toLocaleDateString('pt-BR', { 
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>Consultório</Label>
              <Select value={formData.consultorio} onValueChange={(value) => setFormData(prev => ({ ...prev, consultorio: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um consultório" />
                </SelectTrigger>
                <SelectContent>
                  {getAllConsultoriosDisponíveis().map((cons) => (
                    <SelectItem key={cons.id} value={cons.id}>
                      {cons.id} - {cons.ocupacao}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label>Paciente</Label>
              <Input 
                value={formData.paciente} 
                onChange={(e) => setFormData(prev => ({ ...prev, paciente: e.target.value }))}
                placeholder="Nome do paciente"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label>Horário</Label>
              <Select value={formData.horario} onValueChange={(value) => setFormData(prev => ({ ...prev, horario: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o horário" />
                </SelectTrigger>
                <SelectContent>
                  {horarios.map((hora) => (
                    <SelectItem key={hora} value={hora}>{hora}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={() => setIsAddDialogOpen(false)}>
                Cancelar
              </Button>
              <Button type="submit">Agendar</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header com navegação de data */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Visão Diária</h2>
          <p className="text-gray-600 mt-2">Status dos consultórios em tempo real</p>
        </div>
        
        <div className="flex items-center space-x-4">
          <Button 
            variant="outline" 
            onClick={() => setIsAddDialogOpen(true)}
            className="flex items-center space-x-2"
          >
            <Plus className="h-4 w-4" />
            <span>Novo Agendamento</span>
          </Button>
          
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="icon" onClick={() => navigateDate(-1)}>
              <ChevronLeft className="h-4 w-4" />
            </Button>
            
            <div className="text-center px-4">
              <div className="font-semibold text-lg">
                {selectedDate.toLocaleDateString('pt-BR', { 
                  weekday: 'long',
                  day: 'numeric',
                  month: 'long'
                })}
              </div>
              <div className="text-sm text-gray-500">
                {currentTime.toLocaleTimeString('pt-BR', { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </div>
            </div>
            
            <Button variant="outline" size="icon" onClick={() => navigateDate(1)}>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Grid de consultórios */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {getAllConsultoriosDisponíveis().map((consultorio) => {
          const status = getStatusConsultorio(consultorio.id);
          const agendamentosHoje = agendamentos.filter(a => a.consultorio === consultorio.id);
          
          return (
            <Card key={consultorio.id} className={`hover:shadow-lg transition-shadow ${getStatusColor(status)}`}>
              <CardHeader className="pb-3">
                <div className="flex justify-between items-center">
                  <CardTitle className="text-lg">{consultorio.id}</CardTitle>
                  <Badge 
                    variant="secondary" 
                    className={`capitalize ${getStatusColor(status)}`}
                  >
                    {status.replace('_', ' ')}
                  </Badge>
                </div>
                <CardDescription>
                  <div className="space-y-1">
                    <p className="font-medium">{consultorio.ocupacao}</p>
                    <div className="flex items-center space-x-1 text-xs">
                      <Clock className="h-3 w-3" />
                      <span>{consultorio.horario}</span>
                    </div>
                  </div>
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Agendamentos</span>
                    <Badge variant="outline">{agendamentosHoje.length}</Badge>
                  </div>
                  
                  <div className="space-y-1 max-h-32 overflow-y-auto">
                    {agendamentosHoje.length > 0 ? (
                      agendamentosHoje.map((agendamento) => (
                        <div key={agendamento.id} className="text-xs p-2 bg-white/50 rounded">
                          <div className="flex justify-between items-center">
                            <span className="font-medium">{agendamento.horario}</span>
                            <Badge className={`text-xs ${getStatusColor(agendamento.status)}`}>
                              {agendamento.status.replace('_', ' ')}
                            </Badge>
                          </div>
                          <p className="text-gray-600 mt-1">{agendamento.paciente}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-xs text-gray-500 text-center py-2">
                        Nenhum agendamento
                      </p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Timeline do dia */}
      <Card>
        <CardHeader>
          <CardTitle>Timeline do Dia</CardTitle>
          <CardDescription>Cronograma detalhado dos agendamentos</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {horarios.map((horario) => {
              const agendamentosHorario = agendamentos.filter(a => a.horario === horario);
              const isHorarioAtual = currentTime.getHours() === parseInt(horario.split(':')[0]);
              
              return (
                <div 
                  key={horario}
                  className={`flex items-center p-3 rounded-lg border ${isHorarioAtual ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200'}`}
                >
                  <div className={`w-16 text-sm font-medium ${isHorarioAtual ? 'text-blue-700' : 'text-gray-700'}`}>
                    {horario}
                  </div>
                  
                  <div className="flex-1 flex flex-wrap gap-2 ml-4">
                    {agendamentosHorario.length > 0 ? (
                      agendamentosHorario.map((agendamento) => (
                        <div 
                          key={agendamento.id}
                          className="flex items-center space-x-2 bg-white px-3 py-1 rounded border"
                        >
                          <Badge variant="outline" className="text-xs">
                            {agendamento.consultorio}
                          </Badge>
                          <span className="text-sm">{agendamento.paciente}</span>
                          <Badge className={`text-xs ${getStatusColor(agendamento.status)}`}>
                            {agendamento.status.replace('_', ' ')}
                          </Badge>
                        </div>
                      ))
                    ) : (
                      <span className="text-gray-400 text-sm">Nenhum agendamento</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      <AddAppointmentDialog />
    </div>
  );
};

export default DailyView;
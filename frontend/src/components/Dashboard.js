import React, { useState, useEffect } from 'react';
import { Calendar, Clock, Users, Building, Activity, FileText } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { consultoriosFixos, cronogramaSemanal, agendamentosHoje } from '../mock/mockData';
import WeeklyView from './WeeklyView';
import DailyView from './DailyView';
import ReportsView from './ReportsView';

const Dashboard = () => {
  const [currentView, setCurrentView] = useState('dashboard');
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const getDiaAtual = () => {
    const dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
    return dias[currentTime.getDay()];
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'confirmado': return 'bg-blue-100 text-blue-800';
      case 'em_atendimento': return 'bg-green-100 text-green-800';
      case 'aguardando': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderContent = () => {
    switch(currentView) {
      case 'semanal':
        return <WeeklyView />;
      case 'diario':
        return <DailyView />;
      case 'relatorios':
        return <ReportsView />;
      default:
        return renderDashboard();
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Consultórios Ativos</CardTitle>
            <Building className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">5 fixos, 3 variáveis</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Atendimentos Hoje</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{agendamentosHoje.length}</div>
            <p className="text-xs text-muted-foreground">4 confirmados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Ocupação</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">87%</div>
            <p className="text-xs text-muted-foreground">Acima da média</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Horário Atual</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {currentTime.toLocaleTimeString('pt-BR', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
            <p className="text-xs text-muted-foreground">
              {currentTime.toLocaleDateString('pt-BR')}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Consultórios Fixos */}
      <Card>
        <CardHeader>
          <CardTitle>Consultórios Fixos (C1 - C5)</CardTitle>
          <CardDescription>Distribuição permanente das Equipes ESF</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {consultoriosFixos.map((consultorio) => (
              <div 
                key={consultorio.id}
                className="p-4 border rounded-lg bg-gradient-to-br from-white to-gray-50 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-lg">{consultorio.id}</h3>
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: consultorio.cor }}
                  ></div>
                </div>
                <p className="text-sm text-gray-600 mb-1">{consultorio.ocupacao}</p>
                <Badge variant="outline" className="text-xs">
                  {consultorio.horario}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Consultórios Variáveis */}
      <Card>
        <CardHeader>
          <CardTitle>Consultórios Variáveis - {getDiaAtual().charAt(0).toUpperCase() + getDiaAtual().slice(1)}</CardTitle>
          <CardDescription>C6, C7 e C8 - Uso rotativo para especialistas</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {cronogramaSemanal[getDiaAtual()] && Object.entries(cronogramaSemanal[getDiaAtual()]).map(([consultorio, info]) => (
              <div key={consultorio} className="p-4 border rounded-lg bg-gradient-to-br from-blue-50 to-indigo-50 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-lg">{consultorio}</h3>
                  <Badge variant="secondary">{info.periodo}</Badge>
                </div>
                <p className="text-sm text-gray-700 mb-2">{info.especialidade}</p>
                <Badge variant="outline" className="text-xs">
                  {info.horario}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Atendimentos de Hoje */}
      <Card>
        <CardHeader>
          <CardTitle>Atendimentos de Hoje</CardTitle>
          <CardDescription>Status em tempo real dos agendamentos</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {agendamentosHoje.map((agendamento) => (
              <div key={agendamento.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Badge variant="outline">{agendamento.consultorio}</Badge>
                  <div>
                    <p className="font-medium">{agendamento.paciente}</p>
                    <p className="text-sm text-gray-500">{agendamento.especialidade}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-medium">{agendamento.horario}</span>
                  <Badge className={getStatusColor(agendamento.status)}>
                    {agendamento.status.replace('_', ' ')}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Building className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                Sistema de Gestão de Consultórios
              </h1>
            </div>
            
            <nav className="flex space-x-4">
              <Button 
                variant={currentView === 'dashboard' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('dashboard')}
                className="flex items-center space-x-2"
              >
                <Activity className="h-4 w-4" />
                <span>Dashboard</span>
              </Button>
              
              <Button 
                variant={currentView === 'semanal' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('semanal')}
                className="flex items-center space-x-2"
              >
                <Calendar className="h-4 w-4" />
                <span>Visão Semanal</span>
              </Button>
              
              <Button 
                variant={currentView === 'diario' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('diario')}
                className="flex items-center space-x-2"
              >
                <Clock className="h-4 w-4" />
                <span>Visão Diária</span>
              </Button>
              
              <Button 
                variant={currentView === 'relatorios' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('relatorios')}
                className="flex items-center space-x-2"
              >
                <FileText className="h-4 w-4" />
                <span>Relatórios</span>
              </Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderContent()}
      </main>
    </div>
  );
};

export default Dashboard;
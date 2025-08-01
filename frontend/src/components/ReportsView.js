import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Calendar } from './ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { 
  BarChart, 
  FileText, 
  Download, 
  Calendar as CalendarIcon,
  TrendingUp,
  Users,
  Clock,
  Activity
} from 'lucide-react';
import { dadosHistoricos, consultoriosFixos } from '../mock/mockData';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

const ReportsView = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('semana');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [selectedConsultorio, setSelectedConsultorio] = useState('todos');
  const [reportType, setReportType] = useState('ocupacao');

  // Dados mock para relatórios
  const dadosOcupacao = [
    { consultorio: 'C1', ocupacao: 92, atendimentos: 45 },
    { consultorio: 'C2', ocupacao: 87, atendimentos: 42 },
    { consultorio: 'C3', ocupacao: 89, atendimentos: 38 },
    { consultorio: 'C4', ocupacao: 94, atendimentos: 48 },
    { consultorio: 'C5', ocupacao: 91, atendimentos: 41 },
    { consultorio: 'C6', ocupacao: 85, atendimentos: 35 },
    { consultorio: 'C7', ocupacao: 78, atendimentos: 32 },
    { consultorio: 'C8', ocupacao: 73, atendimentos: 28 }
  ];

  const especialidadesStats = [
    { nome: 'ESF 1', atendimentos: 156, satisfacao: 4.8 },
    { nome: 'ESF 2', atendimentos: 142, satisfacao: 4.7 },
    { nome: 'Cardiologia', atendimentos: 89, satisfacao: 4.9 },
    { nome: 'Pediatria', atendimentos: 67, satisfacao: 4.8 },
    { nome: 'Acupuntura', atendimentos: 45, satisfacao: 4.9 },
    { nome: 'Ginecologia', atendimentos: 34, satisfacao: 4.7 }
  ];

  const tempoEspera = [
    { periodo: '07h-09h', tempoMedio: 12 },
    { periodo: '09h-11h', tempoMedio: 18 },
    { periodo: '11h-13h', tempoMedio: 25 },
    { periodo: '13h-15h', tempoMedio: 15 },
    { periodo: '15h-17h', tempoMedio: 20 },
    { periodo: '17h-19h', tempoMedio: 22 }
  ];

  const generateReport = () => {
    // Simular geração de relatório
    console.log('Gerando relatório:', {
      periodo: selectedPeriod,
      startDate,
      endDate,
      consultorio: selectedConsultorio,
      tipo: reportType
    });
    
    // Aqui seria a integração com o backend
    alert('Relatório gerado! Em breve será implementada a funcionalidade de download.');
  };

  const exportData = (format) => {
    console.log(`Exportando dados em formato: ${format}`);
    alert(`Exportação em ${format.toUpperCase()} será implementada em breve.`);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Relatórios e Análises</h2>
          <p className="text-gray-600 mt-2">Dados históricos e insights dos consultórios</p>
        </div>
        
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => exportData('pdf')}>
            <Download className="h-4 w-4 mr-2" />
            Exportar PDF
          </Button>
          <Button variant="outline" onClick={() => exportData('excel')}>
            <Download className="h-4 w-4 mr-2" />
            Exportar Excel
          </Button>
        </div>
      </div>

      {/* Filtros */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="h-5 w-5" />
            <span>Filtros de Relatório</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label>Tipo de Relatório</Label>
              <Select value={reportType} onValueChange={setReportType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ocupacao">Taxa de Ocupação</SelectItem>
                  <SelectItem value="atendimentos">Atendimentos</SelectItem>
                  <SelectItem value="especialidades">Por Especialidade</SelectItem>
                  <SelectItem value="tempo_espera">Tempo de Espera</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Período</Label>
              <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="hoje">Hoje</SelectItem>
                  <SelectItem value="semana">Esta Semana</SelectItem>
                  <SelectItem value="mes">Este Mês</SelectItem>
                  <SelectItem value="trimestre">Trimestre</SelectItem>
                  <SelectItem value="personalizado">Personalizado</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Consultório</Label>
              <Select value={selectedConsultorio} onValueChange={setSelectedConsultorio}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="todos">Todos</SelectItem>
                  {['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'].map(c => (
                    <SelectItem key={c} value={c}>{c}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Ações</Label>
              <Button onClick={generateReport} className="w-full">
                <BarChart className="h-4 w-4 mr-2" />
                Gerar Relatório
              </Button>
            </div>
          </div>

          {selectedPeriod === 'personalizado' && (
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="space-y-2">
                <Label>Data Inicial</Label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button variant="outline" className="w-full justify-start text-left font-normal">
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {startDate ? format(startDate, 'PPP', { locale: ptBR }) : 'Selecione a data'}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={startDate}
                      onSelect={setStartDate}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
              </div>

              <div className="space-y-2">
                <Label>Data Final</Label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button variant="outline" className="w-full justify-start text-left font-normal">
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {endDate ? format(endDate, 'PPP', { locale: ptBR }) : 'Selecione a data'}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={endDate}
                      onSelect={setEndDate}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Métricas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Ocupação Média</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">86.2%</div>
            <p className="text-xs text-muted-foreground">+5.2% em relação ao mês anterior</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Atendimentos</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2,847</div>
            <p className="text-xs text-muted-foreground">Este mês</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tempo Médio de Espera</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">18 min</div>
            <p className="text-xs text-muted-foreground">-3 min desde semana passada</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Satisfação Média</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4.8/5.0</div>
            <p className="text-xs text-muted-foreground">Baseado em 542 avaliações</p>
          </CardContent>
        </Card>
      </div>

      {/* Taxa de Ocupação por Consultório */}
      <Card>
        <CardHeader>
          <CardTitle>Taxa de Ocupação por Consultório</CardTitle>
          <CardDescription>Últimos 30 dias</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {dadosOcupacao.map((item) => (
              <div key={item.consultorio} className="flex items-center space-x-4">
                <div className="w-12 text-sm font-medium">{item.consultorio}</div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm">{item.ocupacao}%</span>
                    <span className="text-xs text-gray-500">{item.atendimentos} atendimentos</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ width: `${item.ocupacao}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Performance por Especialidade */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Performance por Especialidade</CardTitle>
            <CardDescription>Atendimentos e satisfação</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {especialidadesStats.map((esp) => (
                <div key={esp.nome} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <h4 className="font-medium">{esp.nome}</h4>
                    <p className="text-sm text-gray-500">{esp.atendimentos} atendimentos</p>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center space-x-1">
                      <span className="text-lg font-bold text-yellow-500">★</span>
                      <span className="font-medium">{esp.satisfacao}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Tempo de Espera por Período</CardTitle>
            <CardDescription>Média em minutos</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {tempoEspera.map((item) => (
                <div key={item.periodo} className="flex items-center space-x-4">
                  <div className="w-16 text-sm font-medium">{item.periodo}</div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm">{item.tempoMedio} min</span>
                      <Badge variant={item.tempoMedio > 20 ? 'destructive' : 'secondary'}>
                        {item.tempoMedio > 20 ? 'Alto' : 'Normal'}
                      </Badge>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full transition-all ${
                          item.tempoMedio > 20 ? 'bg-red-500' : 'bg-green-500'
                        }`}
                        style={{ width: `${Math.min(item.tempoMedio * 2, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Dados Históricos */}
      <Card>
        <CardHeader>
          <CardTitle>Histórico de Dados</CardTitle>
          <CardDescription>Últimos registros do sistema</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Data</th>
                  <th className="text-left p-2">Consultório</th>
                  <th className="text-left p-2">Especialidade</th>
                  <th className="text-left p-2">Atendimentos</th>
                  <th className="text-left p-2">Ocupação</th>
                </tr>
              </thead>
              <tbody>
                {dadosHistoricos.map((item, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="p-2">{new Date(item.data).toLocaleDateString('pt-BR')}</td>
                    <td className="p-2">
                      <Badge variant="outline">{item.consultorio}</Badge>
                    </td>
                    <td className="p-2">{item.especialidade}</td>
                    <td className="p-2">{item.atendimentos}</td>
                    <td className="p-2">
                      <Badge variant={parseInt(item.ocupacao) > 80 ? 'default' : 'secondary'}>
                        {item.ocupacao}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ReportsView;
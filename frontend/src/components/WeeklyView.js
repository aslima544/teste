import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { cronogramaSemanal, consultoriosFixos, especialidades } from '../mock/mockData';
import { Edit, Save, X } from 'lucide-react';

const WeeklyView = () => {
  const [editingCell, setEditingCell] = useState(null);
  const [scheduleData, setScheduleData] = useState(cronogramaSemanal);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [selectedCell, setSelectedCell] = useState(null);

  const diasSemana = [
    { key: 'segunda', label: 'Segunda-feira' },
    { key: 'terca', label: 'Terça-feira' },
    { key: 'quarta', label: 'Quarta-feira' },
    { key: 'quinta', label: 'Quinta-feira' },
    { key: 'sexta', label: 'Sexta-feira' }
  ];

  const consultoriosVariaveis = ['C6', 'C7', 'C8'];

  const handleEditClick = (dia, consultorio) => {
    setSelectedCell({
      dia,
      consultorio,
      data: scheduleData[dia][consultorio]
    });
    setIsEditDialogOpen(true);
  };

  const handleSaveEdit = (newData) => {
    if (selectedCell) {
      setScheduleData(prev => ({
        ...prev,
        [selectedCell.dia]: {
          ...prev[selectedCell.dia],
          [selectedCell.consultorio]: newData
        }
      }));
    }
    setIsEditDialogOpen(false);
    setSelectedCell(null);
  };

  const EditDialog = ({ isOpen, onClose, cellData, onSave }) => {
    const [formData, setFormData] = useState(cellData?.data || {});

    const handleSubmit = (e) => {
      e.preventDefault();
      onSave(formData);
    };

    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Editar Atribuição</DialogTitle>
            <DialogDescription>
              {cellData && `${cellData.consultorio} - ${cellData.dia.charAt(0).toUpperCase() + cellData.dia.slice(1)}`}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="especialidade">Especialidade</Label>
              <Select 
                value={formData.especialidade} 
                onValueChange={(value) => setFormData(prev => ({ ...prev, especialidade: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione uma especialidade" />
                </SelectTrigger>
                <SelectContent>
                  {especialidades.map((esp) => (
                    <SelectItem key={esp} value={esp}>{esp}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="periodo">Período</Label>
              <Select 
                value={formData.periodo} 
                onValueChange={(value) => setFormData(prev => ({ ...prev, periodo: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o período" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Manhã">Manhã</SelectItem>
                  <SelectItem value="Tarde">Tarde</SelectItem>
                  <SelectItem value="Manhã/Tarde">Manhã/Tarde</SelectItem>
                  <SelectItem value="Integral">Integral</SelectItem>
                  <SelectItem value="Disponível">Disponível</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="horario">Horário</Label>
              <Input 
                id="horario"
                value={formData.horario} 
                onChange={(e) => setFormData(prev => ({ ...prev, horario: e.target.value }))}
                placeholder="Ex: 08h-17h"
              />
            </div>
            
            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancelar
              </Button>
              <Button type="submit">
                Salvar
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Visão Semanal</h2>
          <p className="text-gray-600 mt-2">Cronograma completo dos consultórios</p>
        </div>
        <Badge variant="secondary" className="text-sm">
          Semana Atual
        </Badge>
      </div>

      {/* Consultórios Fixos */}
      <Card>
        <CardHeader>
          <CardTitle>Consultórios Fixos (C1 - C5)</CardTitle>
          <CardDescription>Atribuições permanentes - ESF</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {consultoriosFixos.map((consultorio) => (
              <div 
                key={consultorio.id}
                className="p-4 border rounded-lg bg-gradient-to-br from-gray-50 to-gray-100"
              >
                <div className="text-center">
                  <h3 className="font-bold text-lg mb-2">{consultorio.id}</h3>
                  <p className="text-sm text-gray-700 mb-2">{consultorio.ocupacao}</p>
                  <Badge variant="outline" className="text-xs">
                    {consultorio.horario}
                  </Badge>
                  <div className="mt-2 text-xs text-gray-500">
                    Segunda a Sexta
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Cronograma Semanal - Consultórios Variáveis */}
      <Card>
        <CardHeader>
          <CardTitle>Cronograma Semanal - Consultórios Variáveis</CardTitle>
          <CardDescription>C6, C7 e C8 - Clique para editar as atribuições</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-4 font-semibold">Dia</th>
                  {consultoriosVariaveis.map(consultorio => (
                    <th key={consultorio} className="text-center p-4 font-semibold">
                      {consultorio}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {diasSemana.map(({ key, label }) => (
                  <tr key={key} className="border-b hover:bg-gray-50">
                    <td className="p-4 font-medium text-gray-900">
                      {label}
                    </td>
                    {consultoriosVariaveis.map(consultorio => (
                      <td key={`${key}-${consultorio}`} className="p-4">
                        <div 
                          className="border rounded-lg p-3 bg-white hover:shadow-md transition-shadow cursor-pointer relative group"
                          onClick={() => handleEditClick(key, consultorio)}
                        >
                          {scheduleData[key] && scheduleData[key][consultorio] ? (
                            <div className="space-y-2">
                              <div className="flex items-center justify-between">
                                <Badge variant="secondary" className="text-xs">
                                  {scheduleData[key][consultorio].periodo}
                                </Badge>
                                <Edit className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                              </div>
                              <p className="text-sm font-medium text-gray-900">
                                {scheduleData[key][consultorio].especialidade}
                              </p>
                              <p className="text-xs text-gray-500">
                                {scheduleData[key][consultorio].horario}
                              </p>
                            </div>
                          ) : (
                            <div className="text-center text-gray-400 py-2">
                              <p className="text-sm">Disponível</p>
                              <Edit className="h-3 w-3 mx-auto mt-1 opacity-0 group-hover:opacity-100" />
                            </div>
                          )}
                        </div>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Visitas Domiciliares */}
      <Card>
        <CardHeader>
          <CardTitle>Visitas Domiciliares</CardTitle>
          <CardDescription>Equipes ESF que saem para atendimento domiciliar</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 border rounded-lg bg-blue-50">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold">Segunda-feira</h4>
                <Badge variant="outline">08h-12h</Badge>
              </div>
              <p className="text-sm text-gray-600">ESF 1 e ESF 3</p>
              <p className="text-xs text-gray-500 mt-1">Libera fluxo em C1 e C3</p>
            </div>
            
            <div className="p-4 border rounded-lg bg-green-50">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold">Quarta-feira</h4>
                <Badge variant="outline">09h-15h</Badge>
              </div>
              <p className="text-sm text-gray-600">ESF 2 e ESF 4</p>
              <p className="text-xs text-gray-500 mt-1">Libera fluxo em C2 e C4</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <EditDialog 
        isOpen={isEditDialogOpen}
        onClose={() => setIsEditDialogOpen(false)}
        cellData={selectedCell}
        onSave={handleSaveEdit}
      />
    </div>
  );
};

export default WeeklyView;
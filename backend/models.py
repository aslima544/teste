from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Enums
class TipoConsultorio(str, Enum):
    FIXO = "fixo"
    VARIAVEL = "variavel"

class StatusAgendamento(str, Enum):
    CONFIRMADO = "confirmado"
    EM_ATENDIMENTO = "em_atendimento"
    AGUARDANDO = "aguardando"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"

class TipoEspecialidade(str, Enum):
    ESF = "esf"
    ESPECIALISTA = "especialista"
    APOIO = "apoio"

class DiaSemana(str, Enum):
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"

class PeriodoAtendimento(str, Enum):
    MANHA = "Manhã"
    TARDE = "Tarde"
    MANHA_TARDE = "Manhã/Tarde"
    INTEGRAL = "Integral"
    DISPONIVEL = "Disponível"

# Models
class Consultorio(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    codigo: str
    nome: str
    tipo: TipoConsultorio
    ocupacao_fixa: Optional[str] = None
    horario_padrao: str
    cor: Optional[str] = None
    ativo: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class ConsultorioCreate(BaseModel):
    codigo: str
    nome: str
    tipo: TipoConsultorio
    ocupacao_fixa: Optional[str] = None
    horario_padrao: str
    cor: Optional[str] = None

class ConsultorioUpdate(BaseModel):
    ocupacao_fixa: Optional[str] = None
    horario_padrao: Optional[str] = None
    cor: Optional[str] = None
    ativo: Optional[bool] = None

class CronogramaSemanal(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    consultorio: str
    dia: DiaSemana
    especialidade: str
    periodo: PeriodoAtendimento
    horario: str
    ativo: bool = True
    semana_referencia: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class CronogramaSemanalCreate(BaseModel):
    consultorio: str
    dia: DiaSemana
    especialidade: str
    periodo: PeriodoAtendimento
    horario: str
    semana_referencia: str

class CronogramaSemanalUpdate(BaseModel):
    especialidade: Optional[str] = None
    periodo: Optional[PeriodoAtendimento] = None
    horario: Optional[str] = None

class Agendamento(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    consultorio: str
    paciente: str
    especialidade: str
    data: datetime
    horario: str
    status: StatusAgendamento = StatusAgendamento.CONFIRMADO
    tipo: str = "consulta"
    observacoes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class AgendamentoCreate(BaseModel):
    consultorio: str
    paciente: str
    especialidade: str
    data: datetime
    horario: str
    tipo: str = "consulta"
    observacoes: Optional[str] = None

class AgendamentoUpdate(BaseModel):
    status: Optional[StatusAgendamento] = None
    observacoes: Optional[str] = None

class Especialidade(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nome: str
    tipo: TipoEspecialidade
    cor: Optional[str] = None
    ativo: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class EspecialidadeCreate(BaseModel):
    nome: str
    tipo: TipoEspecialidade
    cor: Optional[str] = None

class RelatorioHistorico(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    data: datetime
    consultorio: str
    especialidade: str
    total_agendamentos: int
    atendimentos_realizados: int
    taxa_ocupacao: float
    tempo_medio_espera: int  # em minutos
    satisfacao_media: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}

# Response Models para relatórios
class DashboardStats(BaseModel):
    consultorios_ativos: int
    atendimentos_hoje: int
    taxa_ocupacao: float
    horario_atual: str

class RelatorioOcupacao(BaseModel):
    consultorio: str
    ocupacao: float
    atendimentos: int

class RelatorioEspecialidade(BaseModel):
    nome: str
    atendimentos: int
    satisfacao: Optional[float] = None

class RelatorioTempoEspera(BaseModel):
    periodo: str
    tempo_medio: int

class CronogramaSemanalResponse(BaseModel):
    segunda: Optional[dict] = {}
    terca: Optional[dict] = {}
    quarta: Optional[dict] = {}
    quinta: Optional[dict] = {}
    sexta: Optional[dict] = {}

class ConsultoriosResponse(BaseModel):
    fixos: List[Consultorio]
    variaveis: List[Consultorio]

class AgendamentosResponse(BaseModel):
    agendamentos: List[Agendamento]
    total: int
    data: str
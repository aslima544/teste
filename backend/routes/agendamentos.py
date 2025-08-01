from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from datetime import datetime, timedelta
from models import (
    Agendamento, AgendamentoCreate, AgendamentoUpdate,
    AgendamentosResponse, StatusAgendamento
)
from database import db

router = APIRouter(prefix="/agendamentos", tags=["agendamentos"])

@router.get("/", response_model=AgendamentosResponse)
async def get_agendamentos(
    data: Optional[str] = Query(None, description="Data no formato YYYY-MM-DD (padrão: hoje)"),
    consultorio: Optional[str] = Query(None, description="Código do consultório"),
    status: Optional[StatusAgendamento] = Query(None, description="Status do agendamento"),
    limit: int = Query(100, description="Limite de resultados")
):
    """Lista agendamentos com filtros opcionais"""
    try:
        # Preparar filtros
        filtros = {}
        
        # Filtro por data
        if data:
            if data.lower() == "hoje":
                data_consulta = datetime.utcnow().date()
            else:
                data_consulta = datetime.strptime(data, "%Y-%m-%d").date()
        else:
            data_consulta = datetime.utcnow().date()
        
        inicio_dia = datetime.combine(data_consulta, datetime.min.time())
        fim_dia = datetime.combine(data_consulta, datetime.max.time())
        filtros["data"] = {"$gte": inicio_dia, "$lte": fim_dia}
        
        # Filtro por consultório
        if consultorio:
            filtros["consultorio"] = consultorio
        
        # Filtro por status
        if status:
            filtros["status"] = status.value
        
        # Buscar agendamentos
        agendamentos_data = await db.agendamentos.find(filtros).sort("horario", 1).limit(limit).to_list(limit)
        
        agendamentos = [Agendamento(**ag) for ag in agendamentos_data]
        
        return AgendamentosResponse(
            agendamentos=agendamentos,
            total=len(agendamentos),
            data=data_consulta.isoformat()
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamentos: {str(e)}")

@router.get("/{agendamento_id}", response_model=Agendamento)
async def get_agendamento(agendamento_id: str = Path(..., description="ID do agendamento")):
    """Retorna dados de um agendamento específico"""
    try:
        agendamento_data = await db.agendamentos.find_one({"_id": agendamento_id})
        
        if not agendamento_data:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        return Agendamento(**agendamento_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamento: {str(e)}")

@router.post("/", response_model=Agendamento)
async def create_agendamento(agendamento: AgendamentoCreate):
    """Cria um novo agendamento"""
    try:
        # Verificar se o consultório existe
        consultorio_exists = await db.consultorios.find_one({
            "codigo": agendamento.consultorio,
            "ativo": True
        })
        
        if not consultorio_exists:
            raise HTTPException(status_code=404, detail="Consultório não encontrado")
        
        # Verificar conflito de horários
        data_agendamento = agendamento.data.replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_dia = data_agendamento
        fim_dia = data_agendamento + timedelta(days=1)
        
        conflito = await db.agendamentos.find_one({
            "consultorio": agendamento.consultorio,
            "data": {"$gte": inicio_dia, "$lt": fim_dia},
            "horario": agendamento.horario,
            "status": {"$nin": ["cancelado"]}
        })
        
        if conflito:
            raise HTTPException(
                status_code=400,
                detail="Já existe agendamento para este consultório no horário especificado"
            )
        
        # Criar agendamento
        agendamento_data = agendamento.dict()
        agendamento_data["created_at"] = datetime.utcnow()
        agendamento_data["updated_at"] = datetime.utcnow()
        agendamento_data["status"] = StatusAgendamento.CONFIRMADO
        
        result = await db.agendamentos.insert_one(agendamento_data)
        agendamento_data["_id"] = str(result.inserted_id)
        
        return Agendamento(**agendamento_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar agendamento: {str(e)}")

@router.put("/{agendamento_id}", response_model=Agendamento)
async def update_agendamento(
    agendamento_id: str = Path(..., description="ID do agendamento"),
    updates: AgendamentoUpdate = None
):
    """Atualiza status ou observações de um agendamento"""
    try:
        # Verificar se o agendamento existe
        existing = await db.agendamentos.find_one({"_id": agendamento_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Preparar dados para atualização
        update_data = {k: v for k, v in updates.dict(exclude_unset=True).items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        if update_data:
            await db.agendamentos.update_one(
                {"_id": agendamento_id},
                {"$set": update_data}
            )
        
        # Buscar e retornar dados atualizados
        updated_data = await db.agendamentos.find_one({"_id": agendamento_id})
        return Agendamento(**updated_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar agendamento: {str(e)}")

@router.delete("/{agendamento_id}")
async def delete_agendamento(agendamento_id: str = Path(..., description="ID do agendamento")):
    """Cancela um agendamento"""
    try:
        # Verificar se o agendamento existe
        existing = await db.agendamentos.find_one({"_id": agendamento_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Verificar se pode ser cancelado
        agendamento = Agendamento(**existing)
        if agendamento.status in [StatusAgendamento.CONCLUIDO, StatusAgendamento.CANCELADO]:
            raise HTTPException(
                status_code=400,
                detail="Não é possível cancelar agendamento já concluído ou cancelado"
            )
        
        # Cancelar agendamento
        await db.agendamentos.update_one(
            {"_id": agendamento_id},
            {"$set": {
                "status": StatusAgendamento.CANCELADO,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return {"message": "Agendamento cancelado com sucesso"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cancelar agendamento: {str(e)}")

@router.get("/consultorio/{codigo}")
async def get_agendamentos_consultorio(
    codigo: str = Path(..., description="Código do consultório"),
    data_inicio: Optional[str] = Query(None, description="Data início (YYYY-MM-DD)"),
    data_fim: Optional[str] = Query(None, description="Data fim (YYYY-MM-DD)")
):
    """Retorna agendamentos de um consultório em um período"""
    try:
        # Preparar filtros
        filtros = {"consultorio": codigo}
        
        # Definir período
        if data_inicio:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        else:
            inicio = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if data_fim:
            fim = datetime.strptime(data_fim, "%Y-%m-%d") + timedelta(days=1)
        else:
            fim = inicio + timedelta(days=1)
        
        filtros["data"] = {"$gte": inicio, "$lt": fim}
        
        # Buscar agendamentos
        agendamentos_data = await db.agendamentos.find(filtros).sort("data", 1).sort("horario", 1).to_list(100)
        
        agendamentos = [Agendamento(**ag) for ag in agendamentos_data]
        
        # Agrupar por status
        stats = {
            "total": len(agendamentos),
            "confirmado": len([ag for ag in agendamentos if ag.status == StatusAgendamento.CONFIRMADO]),
            "em_atendimento": len([ag for ag in agendamentos if ag.status == StatusAgendamento.EM_ATENDIMENTO]),
            "aguardando": len([ag for ag in agendamentos if ag.status == StatusAgendamento.AGUARDANDO]),
            "concluido": len([ag for ag in agendamentos if ag.status == StatusAgendamento.CONCLUIDO]),
            "cancelado": len([ag for ag in agendamentos if ag.status == StatusAgendamento.CANCELADO])
        }
        
        return {
            "consultorio": codigo,
            "periodo": {
                "inicio": inicio.isoformat(),
                "fim": (fim - timedelta(days=1)).isoformat()
            },
            "agendamentos": agendamentos,
            "estatisticas": stats
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamentos do consultório: {str(e)}")

@router.post("/{agendamento_id}/iniciar-atendimento")
async def iniciar_atendimento(agendamento_id: str = Path(..., description="ID do agendamento")):
    """Marca um agendamento como 'em atendimento'"""
    try:
        result = await db.agendamentos.update_one(
            {
                "_id": agendamento_id,
                "status": {"$in": [StatusAgendamento.CONFIRMADO.value, StatusAgendamento.AGUARDANDO.value]}
            },
            {"$set": {
                "status": StatusAgendamento.EM_ATENDIMENTO.value,
                "updated_at": datetime.utcnow()
            }}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Agendamento não encontrado ou já está em atendimento"
            )
        
        return {"message": "Atendimento iniciado com sucesso"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar atendimento: {str(e)}")

@router.post("/{agendamento_id}/concluir-atendimento")
async def concluir_atendimento(
    agendamento_id: str = Path(..., description="ID do agendamento"),
    observacoes: Optional[str] = Query(None, description="Observações sobre o atendimento")
):
    """Marca um agendamento como 'concluído'"""
    try:
        update_data = {
            "status": StatusAgendamento.CONCLUIDO.value,
            "updated_at": datetime.utcnow()
        }
        
        if observacoes:
            update_data["observacoes"] = observacoes
        
        result = await db.agendamentos.update_one(
            {
                "_id": agendamento_id,
                "status": StatusAgendamento.EM_ATENDIMENTO.value
            },
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Agendamento não encontrado ou não está em atendimento"
            )
        
        return {"message": "Atendimento concluído com sucesso"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao concluir atendimento: {str(e)}")
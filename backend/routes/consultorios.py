from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from datetime import datetime
from ..models import (
    Consultorio, ConsultorioCreate, ConsultorioUpdate,
    ConsultoriosResponse, TipoConsultorio
)
from ..database import db

router = APIRouter(prefix="/consultorios", tags=["consultórios"])

@router.get("/", response_model=ConsultoriosResponse)
async def get_consultorios():
    """Retorna todos os consultórios separados por tipo (fixos e variáveis)"""
    try:
        # Buscar todos os consultórios
        consultorios_data = await db.consultorios.find({"ativo": True}).sort("codigo", 1).to_list(100)
        
        fixos = []
        variaveis = []
        
        for consultorio_data in consultorios_data:
            consultorio = Consultorio(**consultorio_data)
            if consultorio.tipo == TipoConsultorio.FIXO:
                fixos.append(consultorio)
            else:
                variaveis.append(consultorio)
        
        return ConsultoriosResponse(fixos=fixos, variaveis=variaveis)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultórios: {str(e)}")

@router.get("/{codigo}", response_model=Consultorio)
async def get_consultorio(codigo: str = Path(..., description="Código do consultório (ex: C1, C2)")):
    """Retorna dados de um consultório específico"""
    try:
        consultorio_data = await db.consultorios.find_one({"codigo": codigo, "ativo": True})
        
        if not consultorio_data:
            raise HTTPException(status_code=404, detail="Consultório não encontrado")
        
        return Consultorio(**consultorio_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultório: {str(e)}")

@router.post("/", response_model=Consultorio)
async def create_consultorio(consultorio: ConsultorioCreate):
    """Cria um novo consultório"""
    try:
        # Verificar se já existe consultório com o mesmo código
        existing = await db.consultorios.find_one({"codigo": consultorio.codigo})
        if existing:
            raise HTTPException(status_code=400, detail="Já existe um consultório com este código")
        
        consultorio_data = consultorio.dict()
        consultorio_data["created_at"] = datetime.utcnow()
        consultorio_data["updated_at"] = datetime.utcnow()
        consultorio_data["ativo"] = True
        
        result = await db.consultorios.insert_one(consultorio_data)
        consultorio_data["_id"] = str(result.inserted_id)
        
        return Consultorio(**consultorio_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar consultório: {str(e)}")

@router.put("/{codigo}", response_model=Consultorio)
async def update_consultorio(
    codigo: str = Path(..., description="Código do consultório"),
    updates: ConsultorioUpdate = None
):
    """Atualiza dados de um consultório"""
    try:
        # Verificar se o consultório existe
        existing = await db.consultorios.find_one({"codigo": codigo, "ativo": True})
        if not existing:
            raise HTTPException(status_code=404, detail="Consultório não encontrado")
        
        # Preparar dados para atualização
        update_data = {k: v for k, v in updates.dict(exclude_unset=True).items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        if update_data:
            await db.consultorios.update_one(
                {"codigo": codigo, "ativo": True},
                {"$set": update_data}
            )
        
        # Buscar e retornar dados atualizados
        updated_data = await db.consultorios.find_one({"codigo": codigo, "ativo": True})
        return Consultorio(**updated_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar consultório: {str(e)}")

@router.delete("/{codigo}")
async def delete_consultorio(codigo: str = Path(..., description="Código do consultório")):
    """Remove um consultório (soft delete)"""
    try:
        # Verificar se o consultório existe
        existing = await db.consultorios.find_one({"codigo": codigo, "ativo": True})
        if not existing:
            raise HTTPException(status_code=404, detail="Consultório não encontrado")
        
        # Verificar se existem agendamentos ativos para este consultório
        agendamentos_ativos = await db.agendamentos.count_documents({
            "consultorio": codigo,
            "data": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)},
            "status": {"$nin": ["cancelado", "concluido"]}
        })
        
        if agendamentos_ativos > 0:
            raise HTTPException(
                status_code=400, 
                detail="Não é possível remover consultório com agendamentos ativos"
            )
        
        # Soft delete
        await db.consultorios.update_one(
            {"codigo": codigo},
            {"$set": {"ativo": False, "updated_at": datetime.utcnow()}}
        )
        
        return {"message": "Consultório removido com sucesso"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover consultório: {str(e)}")

@router.get("/{codigo}/disponibilidade")
async def get_disponibilidade_consultorio(
    codigo: str = Path(..., description="Código do consultório"),
    data: Optional[str] = Query(None, description="Data no formato YYYY-MM-DD")
):
    """Retorna a disponibilidade de um consultório em uma data específica"""
    try:
        # Verificar se o consultório existe
        consultorio_data = await db.consultorios.find_one({"codigo": codigo, "ativo": True})
        if not consultorio_data:
            raise HTTPException(status_code=404, detail="Consultório não encontrado")
        
        # Se não especificar data, usar hoje
        if not data:
            data_consulta = datetime.utcnow().date()
        else:
            data_consulta = datetime.strptime(data, "%Y-%m-%d").date()
        
        # Buscar agendamentos para a data
        inicio_dia = datetime.combine(data_consulta, datetime.min.time())
        fim_dia = datetime.combine(data_consulta, datetime.max.time())
        
        agendamentos = await db.agendamentos.find({
            "consultorio": codigo,
            "data": {"$gte": inicio_dia, "$lte": fim_dia},
            "status": {"$nin": ["cancelado"]}
        }).sort("horario", 1).to_list(100)
        
        # Calcular slots livres baseado no horário padrão
        consultorio = Consultorio(**consultorio_data)
        
        return {
            "consultorio": codigo,
            "data": data_consulta.isoformat(),
            "horario_funcionamento": consultorio.horario_padrao,
            "agendamentos_existentes": len(agendamentos),
            "agendamentos": [
                {
                    "horario": ag["horario"],
                    "paciente": ag["paciente"],
                    "status": ag["status"]
                } for ag in agendamentos
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar disponibilidade: {str(e)}")
from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from models import (
    CronogramaSemanal, CronogramaSemanalCreate, CronogramaSemanalUpdate,
    CronogramaSemanalResponse, DiaSemana
)
from database import db

router = APIRouter(prefix="/cronograma", tags=["cronograma"])

def get_semana_referencia(data: datetime = None) -> str:
    """Gera string de referência da semana no formato YYYY-WW"""
    if not data:
        data = datetime.utcnow()
    return data.strftime("%Y-W%U")

@router.get("/semanal", response_model=CronogramaSemanalResponse)
async def get_cronograma_semanal(
    semana: Optional[str] = Query(None, description="Semana no formato YYYY-WW")
):
    """Retorna o cronograma semanal completo dos consultórios variáveis"""
    try:
        if not semana:
            semana = get_semana_referencia()
        
        # Buscar cronograma da semana
        cronogramas = await db.cronograma_semanal.find({
            "semana_referencia": semana,
            "ativo": True
        }).to_list(100)
        
        # Organizar por dia da semana
        resultado = {
            "segunda": {},
            "terca": {},
            "quarta": {},
            "quinta": {},
            "sexta": {}
        }
        
        for cronograma_data in cronogramas:
            cronograma = CronogramaSemanal(**cronograma_data)
            dia = cronograma.dia.value
            consultorio = cronograma.consultorio
            
            if dia in resultado:
                resultado[dia][consultorio] = {
                    "especialidade": cronograma.especialidade,
                    "periodo": cronograma.periodo.value,
                    "horario": cronograma.horario
                }
        
        return CronogramaSemanalResponse(**resultado)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cronograma semanal: {str(e)}")

@router.put("/semanal")
async def update_cronograma_semanal(
    dia: DiaSemana,
    consultorio: str,
    dados: CronogramaSemanalUpdate,
    semana: Optional[str] = Query(None, description="Semana no formato YYYY-WW")
):
    """Atualiza uma entrada específica do cronograma semanal"""
    try:
        if not semana:
            semana = get_semana_referencia()
        
        # Verificar se o consultório é variável (C6, C7, C8)
        if consultorio not in ["C6", "C7", "C8"]:
            raise HTTPException(
                status_code=400, 
                detail="Apenas consultórios variáveis (C6, C7, C8) podem ter cronograma alterado"
            )
        
        # Buscar entrada existente
        filtro = {
            "consultorio": consultorio,
            "dia": dia.value,
            "semana_referencia": semana
        }
        
        existing = await db.cronograma_semanal.find_one(filtro)
        
        if existing:
            # Atualizar entrada existente
            update_data = {k: v for k, v in dados.dict(exclude_unset=True).items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()
            
            await db.cronograma_semanal.update_one(
                filtro,
                {"$set": update_data}
            )
        else:
            # Criar nova entrada
            nova_entrada = CronogramaSemanalCreate(
                consultorio=consultorio,
                dia=dia,
                especialidade=dados.especialidade or "Disponível",
                periodo=dados.periodo or "Disponível",
                horario=dados.horario or "Conforme demanda",
                semana_referencia=semana
            )
            
            entrada_data = nova_entrada.dict()
            entrada_data["created_at"] = datetime.utcnow()
            entrada_data["updated_at"] = datetime.utcnow()
            entrada_data["ativo"] = True
            
            await db.cronograma_semanal.insert_one(entrada_data)
        
        return {"message": "Cronograma atualizado com sucesso"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cronograma: {str(e)}")

@router.get("/semanal/{consultorio}")
async def get_cronograma_consultorio(
    consultorio: str = Path(..., description="Código do consultório (C6, C7, C8)"),
    semana: Optional[str] = Query(None, description="Semana no formato YYYY-WW")
):
    """Retorna o cronograma semanal de um consultório específico"""
    try:
        if consultorio not in ["C6", "C7", "C8"]:
            raise HTTPException(
                status_code=400,
                detail="Apenas consultórios variáveis têm cronograma semanal"
            )
        
        if not semana:
            semana = get_semana_referencia()
        
        cronogramas = await db.cronograma_semanal.find({
            "consultorio": consultorio,
            "semana_referencia": semana,
            "ativo": True
        }).sort("dia", 1).to_list(10)
        
        resultado = {}
        for cronograma_data in cronogramas:
            cronograma = CronogramaSemanal(**cronograma_data)
            resultado[cronograma.dia.value] = {
                "especialidade": cronograma.especialidade,
                "periodo": cronograma.periodo.value,
                "horario": cronograma.horario
            }
        
        return {
            "consultorio": consultorio,
            "semana_referencia": semana,
            "cronograma": resultado
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cronograma do consultório: {str(e)}")

@router.post("/semanal/duplicar")
async def duplicar_cronograma_semanal(
    semana_origem: str = Query(..., description="Semana origem no formato YYYY-WW"),
    semana_destino: str = Query(..., description="Semana destino no formato YYYY-WW")
):
    """Duplica cronograma de uma semana para outra"""
    try:
        # Verificar se já existe cronograma na semana destino
        existing = await db.cronograma_semanal.count_documents({
            "semana_referencia": semana_destino,
            "ativo": True
        })
        
        if existing > 0:
            raise HTTPException(
                status_code=400,
                detail="Já existe cronograma para a semana destino"
            )
        
        # Buscar cronograma da semana origem
        cronogramas_origem = await db.cronograma_semanal.find({
            "semana_referencia": semana_origem,
            "ativo": True
        }).to_list(100)
        
        if not cronogramas_origem:
            raise HTTPException(
                status_code=404,
                detail="Cronograma da semana origem não encontrado"
            )
        
        # Duplicar para semana destino
        novos_cronogramas = []
        for cronograma in cronogramas_origem:
            novo_cronograma = cronograma.copy()
            novo_cronograma.pop("_id")
            novo_cronograma["semana_referencia"] = semana_destino
            novo_cronograma["created_at"] = datetime.utcnow()
            novo_cronograma["updated_at"] = datetime.utcnow()
            novos_cronogramas.append(novo_cronograma)
        
        if novos_cronogramas:
            await db.cronograma_semanal.insert_many(novos_cronogramas)
        
        return {
            "message": "Cronograma duplicado com sucesso",
            "semana_origem": semana_origem,
            "semana_destino": semana_destino,
            "entradas_copiadas": len(novos_cronogramas)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao duplicar cronograma: {str(e)}")

@router.delete("/semanal/{semana}")
async def delete_cronograma_semanal(
    semana: str = Path(..., description="Semana no formato YYYY-WW")
):
    """Remove cronograma de uma semana específica"""
    try:
        # Verificar se existem agendamentos para esta semana
        # (implementar lógica de validação se necessário)
        
        result = await db.cronograma_semanal.update_many(
            {"semana_referencia": semana},
            {"$set": {"ativo": False, "updated_at": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Cronograma não encontrado")
        
        return {
            "message": "Cronograma removido com sucesso",
            "semana": semana,
            "entradas_removidas": result.modified_count
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover cronograma: {str(e)}")
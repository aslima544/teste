import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def init_database():
    """Inicializa o banco de dados com dados básicos"""
    
    # Verificar se já existem consultórios
    consultorios_count = await db.consultorios.count_documents({})
    
    if consultorios_count == 0:
        print("Inicializando dados básicos do banco...")
        
        # Consultórios fixos (ESF)
        consultorios_fixos = [
            {
                "codigo": "C1",
                "nome": "Consultório 1",
                "tipo": "fixo",
                "ocupacao_fixa": "ESF 1",
                "horario_padrao": "07h - 16h",
                "cor": "#4F46E5",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "codigo": "C2",
                "nome": "Consultório 2",
                "tipo": "fixo",
                "ocupacao_fixa": "ESF 2",
                "horario_padrao": "07h - 16h",
                "cor": "#059669",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "codigo": "C3",
                "nome": "Consultório 3",
                "tipo": "fixo",
                "ocupacao_fixa": "ESF 3",
                "horario_padrao": "08h - 17h",
                "cor": "#DC2626",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "codigo": "C4",
                "nome": "Consultório 4",
                "tipo": "fixo",
                "ocupacao_fixa": "ESF 4",
                "horario_padrao": "10h - 19h",
                "cor": "#7C2D12",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "codigo": "C5",
                "nome": "Consultório 5",
                "tipo": "fixo",
                "ocupacao_fixa": "ESF 5",
                "horario_padrao": "12h - 21h",
                "cor": "#581C87",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        # Consultórios variáveis
        consultorios_variaveis = [
            {
                "codigo": "C6",
                "nome": "Consultório 6",
                "tipo": "variavel",
                "ocupacao_fixa": None,
                "horario_padrao": "08h - 17h",
                "cor": "#2563EB",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "codigo": "C7",
                "nome": "Consultório 7",
                "tipo": "variavel",
                "ocupacao_fixa": None,
                "horario_padrao": "07h - 16h",
                "cor": "#7C3AED",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "codigo": "C8",
                "nome": "Consultório 8",
                "tipo": "variavel",
                "ocupacao_fixa": None,
                "horario_padrao": "Conforme demanda",
                "cor": "#059669",
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        # Inserir consultórios
        await db.consultorios.insert_many(consultorios_fixos + consultorios_variaveis)
        
        # Especialidades básicas
        especialidades = [
            {
                "nome": "ESF 1",
                "tipo": "esf",
                "cor": "#4F46E5",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "ESF 2",
                "tipo": "esf",
                "cor": "#059669",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "ESF 3",
                "tipo": "esf",
                "cor": "#DC2626",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "ESF 4",
                "tipo": "esf",
                "cor": "#7C2D12",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "ESF 5",
                "tipo": "esf",
                "cor": "#581C87",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "Cardiologia",
                "tipo": "especialista",
                "cor": "#DC2626",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "Acupuntura",
                "tipo": "especialista",
                "cor": "#059669",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "Pediatria",
                "tipo": "especialista",
                "cor": "#2563EB",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "Ginecologista",
                "tipo": "especialista",
                "cor": "#7C3AED",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "E-MULTI",
                "tipo": "especialista",
                "cor": "#16A34A",
                "ativo": True,
                "created_at": datetime.utcnow()
            },
            {
                "nome": "Médico Apoio",
                "tipo": "apoio",
                "cor": "#6B7280",
                "ativo": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        await db.especialidades.insert_many(especialidades)
        
        # Cronograma semanal padrão (semana atual)
        semana_atual = datetime.utcnow().strftime("%Y-W%U")
        
        cronograma_padrao = [
            # Segunda-feira
            {
                "consultorio": "C6",
                "dia": "segunda",
                "especialidade": "Cardiologia",
                "periodo": "Manhã/Tarde",
                "horario": "08h-17h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "consultorio": "C7",
                "dia": "segunda",
                "especialidade": "Médico Apoio",
                "periodo": "Integral",
                "horario": "07h-16h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "consultorio": "C8",
                "dia": "segunda",
                "especialidade": "E-MULTI",
                "periodo": "Manhã/Tarde",
                "horario": "08h-17h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Terça-feira
            {
                "consultorio": "C6",
                "dia": "terca",
                "especialidade": "Acupuntura",
                "periodo": "Manhã/Tarde",
                "horario": "08h-17h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "consultorio": "C7",
                "dia": "terca",
                "especialidade": "Cardiologia",
                "periodo": "Tarde",
                "horario": "13h-17h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "consultorio": "C8",
                "dia": "terca",
                "especialidade": "Médico Apoio",
                "periodo": "Integral",
                "horario": "07h-16h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            # Sexta-feira
            {
                "consultorio": "C6",
                "dia": "sexta",
                "especialidade": "Acupuntura",
                "periodo": "Manhã/Tarde",
                "horario": "08h-17h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "consultorio": "C7",
                "dia": "sexta",
                "especialidade": "Médico Apoio",
                "periodo": "Integral",
                "horario": "07h-16h",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "consultorio": "C8",
                "dia": "sexta",
                "especialidade": "Apoio/Reserva",
                "periodo": "Disponível",
                "horario": "Conforme demanda",
                "semana_referencia": semana_atual,
                "ativo": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        await db.cronograma_semanal.insert_many(cronograma_padrao)
        
        print("✅ Dados básicos inseridos com sucesso!")
    
    # Criar índices para performance
    await db.agendamentos.create_index([("consultorio", 1), ("data", 1), ("horario", 1)])
    await db.agendamentos.create_index([("data", 1), ("status", 1)])
    await db.cronograma_semanal.create_index([("consultorio", 1), ("dia", 1), ("semana_referencia", 1)])
    await db.consultorios.create_index([("codigo", 1), ("ativo", 1)])
    
    print("✅ Índices criados com sucesso!")

# Função para fechar conexão
async def close_db():
    client.close()
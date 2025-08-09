#!/usr/bin/env python3
"""
FastAPI Server - Versão otimizada para Railway
Com startup não-bloqueante e fallbacks robustos
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing import Optional, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import uuid
import asyncio

load_dotenv()

app = FastAPI(title="Sistema de Gestão de Consultórios", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Configuration
print("🔍 Verificando variáveis de ambiente...")
print(f"MONGO_URL exists: {'MONGO_URL' in os.environ}")
print(f"DATABASE_URL exists: {'DATABASE_URL' in os.environ}")

# Get the MongoDB URL with better validation
MONGO_URL = (os.getenv("MONGO_URL") or 
             os.getenv("DATABASE_URL") or 
             os.getenv("MONGODB_URI") or "").strip()

print(f"🔍 MONGO_URL valor bruto: '{MONGO_URL}'")
print(f"🔍 MONGO_URL length: {len(MONGO_URL)}")

DATABASE_NAME = os.getenv("DATABASE_NAME", "sistema_consultorio")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-jwt-tokens-consultorio")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

# Validation and fallback with detailed logging
if MONGO_URL and MONGO_URL.startswith(('mongodb://', 'mongodb+srv://')):
    print(f"✅ MONGO_URL válida: {MONGO_URL[:50]}...")
elif MONGO_URL:
    print(f"❌ URI inválida! Valor recebido: '{MONGO_URL}'")
    print("🔄 Usando fallback para Atlas...")
    MONGO_URL = "mongodb+srv://admin:senha45195487@cluster0.8skwoca.mongodb.net/sistema_consultorio?retryWrites=true&w=majority&appName=Cluster0"
    print(f"✅ Fallback configurado: {MONGO_URL[:50]}...")
else:
    print("❌ NENHUMA variável de MongoDB encontrada ou está vazia!")
    print(f"💡 Todas as variáveis de ambiente:")
    for key in sorted(os.environ.keys()):
        if any(keyword in key.upper() for keyword in ['MONGO', 'DATABASE', 'DB']):
            print(f"    {key} = {os.environ[key][:50]}...")
    
    print("🔄 Usando fallback para Atlas...")
    MONGO_URL = "mongodb+srv://admin:senha45195487@cluster0.8skwoca.mongodb.net/sistema_consultorio?retryWrites=true&w=majority&appName=Cluster0"
    print(f"✅ Fallback configurado: {MONGO_URL[:50]}...")

print(f"🌐 URL FINAL sendo usada: {MONGO_URL[:50]}...")

# Global variables for database (initialized later)
client = None
db = None

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simple health check that doesn't require database
@app.get("/api/health")
async def health_check():
    """Health check endpoint - doesn't require database"""
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "database_connected": db is not None
    }

@app.get("/api/debug-config")
async def debug_config():
    """Endpoint para debug das configurações"""
    return {
        "mongo_url_configured": bool(os.getenv("MONGO_URL")),
        "database_url_configured": bool(os.getenv("DATABASE_URL")),
        "mongodb_uri_configured": bool(os.getenv("MONGODB_URI")),
        "database_name": DATABASE_NAME,
        "mongo_url_prefix": MONGO_URL[:20] if MONGO_URL else "NONE",
        "available_env_vars": [k for k in os.environ.keys() if 'MONGO' in k.upper() or 'DATABASE' in k.upper()],
        "database_connected": db is not None
    }

# Lazy database initialization
def init_database():
    """Initialize database connection lazily"""
    global client, db
    if client is None:
        try:
            client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')  # Test connection
            db = client[DATABASE_NAME]
            print("✅ MongoDB conexão estabelecida!")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar MongoDB: {e}")
            client = None
            db = None
            return False
    return db is not None

@app.on_event("startup")
async def startup_event():
    """Non-blocking startup event"""
    print("🚀 Sistema iniciando...")
    
    # Try to initialize database (non-blocking)
    try:
        init_database()
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
    
    print("✅ Sistema pronto! (Database será inicializado sob demanda)")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
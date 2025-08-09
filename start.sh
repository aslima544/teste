#!/bin/bash
echo "🚀 Iniciando aplicação no Railway..."
echo "📁 Diretório atual: $(pwd)"
echo "📂 Arquivos disponíveis:"
ls -la

echo "🔍 Verificando variáveis de ambiente..."
env | grep -i mongo

echo "🌐 Iniciando servidor FastAPI..."
cd /app/backend || cd backend
python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime

# Import routes
from routes import consultorios, cronograma, agendamentos
from database import init_database, close_db, db


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Inicializando aplicação...")
    await init_database()
    logger.info("✅ Aplicação inicializada com sucesso!")
    
    yield
    
    # Shutdown
    logger.info("Finalizando aplicação...")
    await close_db()
    logger.info("✅ Aplicação finalizada!")

# Create the main app
app = FastAPI(
    title="Sistema de Gestão de Consultórios",
    description="API para gerenciamento de consultórios médicos",
    version="1.0.0",
    lifespan=lifespan
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "Sistema de Gestão de Consultórios API",
        "version": "1.0.0",
        "status": "online"
    }

@api_router.get("/health")
async def health_check():
    try:
        # Test database connection
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Include routers
api_router.include_router(consultorios.router)
api_router.include_router(cronograma.router)
api_router.include_router(agendamentos.router)

# Include the main router in the app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

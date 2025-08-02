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
from bson import ObjectId

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
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "consultorio_db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-jwt-tokens-consultorio")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

client = MongoClient(MONGO_URL)
db = client[DATABASE_NAME]

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic Models
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: str = "reception"  # admin, doctor, reception

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool = True
    created_at: datetime

class PatientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: str
    cpf: str
    birth_date: datetime
    address: Optional[str] = None
    medical_history: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: str
    created_at: datetime
    updated_at: datetime

class DoctorBase(BaseModel):
    name: str
    email: str
    phone: str
    crm: str
    specialty: str
    available_hours: List[str] = []  # ["09:00", "10:00", "14:00"]

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: str
    created_at: datetime
    is_active: bool = True

class ConsultorioBase(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: int = 1
    equipment: Optional[List[str]] = []
    location: Optional[str] = None
    is_active: bool = True

class ConsultorioCreate(ConsultorioBase):
    pass

class Consultorio(ConsultorioBase):
    id: str
    created_at: datetime

class AppointmentBase(BaseModel):
    patient_id: str
    doctor_id: str
    consultorio_id: str
    appointment_date: datetime
    duration_minutes: int = 30
    notes: Optional[str] = None
    status: str = "scheduled"  # scheduled, completed, canceled

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: str
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Helper Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

def serialize_doc(doc):
    """Convert MongoDB document to dict with string ID"""
    if doc:
        # If document already has custom 'id' field, keep it; otherwise use _id
        if "id" not in doc:
            doc["id"] = str(doc["_id"])
        if "_id" in doc:
            del doc["_id"]
    return doc

# Initialize default admin user
@app.on_event("startup")
async def startup_event():
    # Create default admin user if doesn't exist
    admin_user = db.users.find_one({"username": "admin"})
    if not admin_user:
        admin_data = {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@consultorio.com",
            "full_name": "Administrador",
            "role": "admin",
            "password_hash": get_password_hash("admin123"),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        db.users.insert_one(admin_data)
        print("Default admin user created: admin/admin123")

# Auth Routes
@app.post("/api/auth/login", response_model=Token)
async def login(login_request: LoginRequest):
    user = db.users.find_one({"username": login_request.username})
    if not user or not verify_password(login_request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return serialize_doc(current_user)

# User Routes
@app.post("/api/users", response_model=User)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create users")
    
    # Check if username already exists
    if db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_data = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "password_hash": get_password_hash(user.password),
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    result = db.users.insert_one(user_data)
    created_user = db.users.find_one({"_id": result.inserted_id})
    return serialize_doc(created_user)

@app.get("/api/users", response_model=List[User])
async def get_users(current_user: dict = Depends(get_current_user)):
    users = list(db.users.find({}))
    return [serialize_doc(user) for user in users]

# Patient Routes
@app.post("/api/patients", response_model=Patient)
async def create_patient(patient: PatientCreate, current_user: dict = Depends(get_current_user)):
    patient_data = {
        "id": str(uuid.uuid4()),
        **patient.dict(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.patients.insert_one(patient_data)
    created_patient = db.patients.find_one({"_id": result.inserted_id})
    return serialize_doc(created_patient)

@app.get("/api/patients", response_model=List[Patient])
async def get_patients(current_user: dict = Depends(get_current_user)):
    patients = list(db.patients.find({}))
    return [serialize_doc(patient) for patient in patients]

@app.get("/api/patients/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str, current_user: dict = Depends(get_current_user)):
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return serialize_doc(patient)

@app.put("/api/patients/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, patient_update: PatientCreate, current_user: dict = Depends(get_current_user)):
    update_data = {
        **patient_update.dict(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.patients.update_one({"id": patient_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    updated_patient = db.patients.find_one({"id": patient_id})
    return serialize_doc(updated_patient)

@app.delete("/api/patients/{patient_id}")
async def delete_patient(patient_id: str, current_user: dict = Depends(get_current_user)):
    result = db.patients.delete_one({"id": patient_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

# Doctor Routes
@app.post("/api/doctors", response_model=Doctor)
async def create_doctor(doctor: DoctorCreate, current_user: dict = Depends(get_current_user)):
    doctor_data = {
        "id": str(uuid.uuid4()),
        **doctor.dict(),
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = db.doctors.insert_one(doctor_data)
    created_doctor = db.doctors.find_one({"_id": result.inserted_id})
    return serialize_doc(created_doctor)

@app.get("/api/doctors", response_model=List[Doctor])
async def get_doctors(current_user: dict = Depends(get_current_user)):
    doctors = list(db.doctors.find({"is_active": True}))
    return [serialize_doc(doctor) for doctor in doctors]

@app.get("/api/doctors/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: str, current_user: dict = Depends(get_current_user)):
    doctor = db.doctors.find_one({"id": doctor_id})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return serialize_doc(doctor)

# Consultorio Routes
@app.post("/api/consultorios", response_model=Consultorio)
async def create_consultorio(consultorio: ConsultorioCreate, current_user: dict = Depends(get_current_user)):
    consultorio_data = {
        "id": str(uuid.uuid4()),
        **consultorio.dict(),
        "created_at": datetime.utcnow()
    }
    
    result = db.consultorios.insert_one(consultorio_data)
    created_consultorio = db.consultorios.find_one({"_id": result.inserted_id})
    return serialize_doc(created_consultorio)

@app.get("/api/consultorios", response_model=List[Consultorio])
async def get_consultorios(current_user: dict = Depends(get_current_user)):
    consultorios = list(db.consultorios.find({"is_active": True}))
    return [serialize_doc(consultorio) for consultorio in consultorios]

@app.get("/api/consultorios/{consultorio_id}", response_model=Consultorio)
async def get_consultorio(consultorio_id: str, current_user: dict = Depends(get_current_user)):
    consultorio = db.consultorios.find_one({"id": consultorio_id})
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultório not found")
    return serialize_doc(consultorio)

@app.put("/api/consultorios/{consultorio_id}", response_model=Consultorio)
async def update_consultorio(consultorio_id: str, consultorio_update: ConsultorioCreate, current_user: dict = Depends(get_current_user)):
    update_data = {
        **consultorio_update.dict(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.consultorios.update_one({"id": consultorio_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Consultório not found")
    
    updated_consultorio = db.consultorios.find_one({"id": consultorio_id})
    return serialize_doc(updated_consultorio)

@app.delete("/api/consultorios/{consultorio_id}")
async def delete_consultorio(consultorio_id: str, current_user: dict = Depends(get_current_user)):
    result = db.consultorios.update_one({"id": consultorio_id}, {"$set": {"is_active": False}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Consultório not found")
    return {"message": "Consultório deleted successfully"}

# Appointment Routes
@app.post("/api/appointments", response_model=Appointment)
async def create_appointment(appointment: AppointmentCreate, current_user: dict = Depends(get_current_user)):
    # Check if patient exists
    patient = db.patients.find_one({"id": appointment.patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Check if doctor exists
    doctor = db.doctors.find_one({"id": appointment.doctor_id})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Check if consultorio exists
    consultorio = db.consultorios.find_one({"id": appointment.consultorio_id, "is_active": True})
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultório not found")
    
    # Check for conflicts (same consultorio at same time)
    start_time = appointment.appointment_date
    end_time = start_time + timedelta(minutes=appointment.duration_minutes)
    
    existing_appointment = db.appointments.find_one({
        "consultorio_id": appointment.consultorio_id,
        "status": {"$ne": "canceled"},
        "$or": [
            {
                "$and": [
                    {"appointment_date": {"$lte": start_time}},
                    {"appointment_date": {"$gte": start_time}}
                ]
            },
            {
                "$and": [
                    {"appointment_date": {"$lt": end_time}},
                    {"appointment_date": {"$gt": start_time}}
                ]
            }
        ]
    })
    
    if existing_appointment:
        raise HTTPException(status_code=409, detail="Consultório já ocupado neste horário")
    
    appointment_data = {
        "id": str(uuid.uuid4()),
        **appointment.dict(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.appointments.insert_one(appointment_data)
    created_appointment = db.appointments.find_one({"_id": result.inserted_id})
    return serialize_doc(created_appointment)

@app.get("/api/appointments", response_model=List[Appointment])
async def get_appointments(current_user: dict = Depends(get_current_user)):
    appointments = list(db.appointments.find({}))
    return [serialize_doc(appointment) for appointment in appointments]

@app.get("/api/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str, current_user: dict = Depends(get_current_user)):
    appointment = db.appointments.find_one({"id": appointment_id})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return serialize_doc(appointment)

@app.put("/api/appointments/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, appointment_update: AppointmentCreate, current_user: dict = Depends(get_current_user)):
    update_data = {
        **appointment_update.dict(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.appointments.update_one({"id": appointment_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    updated_appointment = db.appointments.find_one({"id": appointment_id})
    return serialize_doc(updated_appointment)

# Dashboard Routes
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    # Get today's date range
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    # Count statistics
    total_patients = db.patients.count_documents({})
    total_doctors = db.doctors.count_documents({"is_active": True})
    total_consultorios = db.consultorios.count_documents({"is_active": True})
    total_appointments = db.appointments.count_documents({})
    
    # Today's appointments
    today_appointments = db.appointments.count_documents({
        "appointment_date": {
            "$gte": today,
            "$lt": tomorrow
        }
    })
    
    # Recent appointments with patient, doctor and consultorio names
    recent_appointments = list(db.appointments.find({}).sort("created_at", -1).limit(5))
    for appointment in recent_appointments:
        patient = db.patients.find_one({"id": appointment["patient_id"]})
        doctor = db.doctors.find_one({"id": appointment["doctor_id"]})
        consultorio = db.consultorios.find_one({"id": appointment.get("consultorio_id", "")})
        appointment["patient_name"] = patient["name"] if patient else "Unknown"
        appointment["doctor_name"] = doctor["name"] if doctor else "Unknown"
        appointment["consultorio_name"] = consultorio["name"] if consultorio else "N/A"
        appointment = serialize_doc(appointment)
    
    # Consultorio occupancy today
    consultorio_stats = []
    consultorios = list(db.consultorios.find({"is_active": True}))
    for consultorio in consultorios:
        occupied_slots = db.appointments.count_documents({
            "consultorio_id": consultorio["id"],
            "appointment_date": {
                "$gte": today,
                "$lt": tomorrow
            },
            "status": {"$ne": "canceled"}
        })
        consultorio_stats.append({
            "name": consultorio["name"],
            "occupied_slots": occupied_slots,
            "id": consultorio["id"]
        })
    
    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_consultorios": total_consultorios,
        "total_appointments": total_appointments,
        "today_appointments": today_appointments,
        "recent_appointments": [serialize_doc(app) for app in recent_appointments],
        "consultorio_stats": consultorio_stats
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
#!/usr/bin/env python3
"""
Script para popular MongoDB Atlas diretamente com dados
"""
import os
from pymongo import MongoClient
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
import sys

def populate_atlas_direct():
    """Popula o Atlas diretamente via MongoDB"""
    
    # Connection string do Atlas
    atlas_url = input("Cole a connection string do MongoDB Atlas: ")
    
    if not atlas_url:
        print("❌ Connection string não fornecida")
        return
    
    try:
        client = MongoClient(atlas_url)
        db = client["consultorio_db"]
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        print("🔄 Conectado ao Atlas. Populando dados...")
        
        # Clear existing data
        print("🗑️  Limpando dados existentes...")
        db.users.delete_many({})
        db.patients.delete_many({})
        db.doctors.delete_many({})
        db.appointments.delete_many({})
        db.consultorios.delete_many({})
        
        # 1. Create Users
        print("👥 Criando usuários...")
        users_data = [
            {
                "id": str(uuid.uuid4()),
                "username": "admin",
                "email": "admin@consultorio.com",
                "full_name": "Administrador",
                "role": "admin",
                "password_hash": pwd_context.hash("admin123"),
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "username": "recepcao",
                "email": "recepcao@consultorio.com",
                "full_name": "Recepção Geral",
                "role": "reception", 
                "password_hash": pwd_context.hash("recepcao123"),
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "username": "dr.silva",
                "email": "dr.silva@consultorio.com", 
                "full_name": "Dr. João Silva",
                "role": "doctor",
                "password_hash": pwd_context.hash("doctor123"),
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        db.users.insert_many(users_data)
        print(f"   ✅ {len(users_data)} usuários criados")
        
        # 2. Create Consultorios
        print("🏥 Criando consultórios...")
        consultorios_data = [
            {
                "id": str(uuid.uuid4()),
                "name": "C1",
                "description": "Consultório 1 - Estratégia Saúde da Família 1",
                "capacity": 2,
                "equipment": ["Estetoscópio", "Tensiômetro", "Balança", "Mesa ginecológica"],
                "location": "Térreo - Ala Oeste",
                "occupancy_type": "fixed",
                "is_active": True,
                "fixed_schedule": {
                    "team": "ESF 1",
                    "start": "07:00",
                    "end": "16:00"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "name": "C2",
                "description": "Consultório 2 - Estratégia Saúde da Família 2", 
                "capacity": 2,
                "equipment": ["Estetoscópio", "Tensiômetro", "Balança"],
                "location": "Térreo - Ala Oeste",
                "occupancy_type": "fixed",
                "is_active": True,
                "fixed_schedule": {
                    "team": "ESF 2",
                    "start": "07:00",
                    "end": "16:00"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "name": "C3",
                "description": "Consultório 3 - Estratégia Saúde da Família 3",
                "capacity": 2,
                "equipment": ["Estetoscópio", "Tensiômetro", "Balança"],
                "location": "Térreo - Ala Este",
                "occupancy_type": "fixed",
                "is_active": True,
                "fixed_schedule": {
                    "team": "ESF 3",
                    "start": "07:00", 
                    "end": "16:00"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "name": "C4",
                "description": "Consultório 4 - Estratégia Saúde da Família 4",
                "capacity": 2,
                "equipment": ["Estetoscópio", "Tensiômetro", "Balança"],
                "location": "Térreo - Ala Este",
                "occupancy_type": "fixed",
                "is_active": True,
                "fixed_schedule": {
                    "team": "ESF 4",
                    "start": "07:00",
                    "end": "16:00"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "name": "C5", 
                "description": "Consultório 5 - Estratégia Saúde da Família 5",
                "capacity": 2,
                "equipment": ["Estetoscópio", "Tensiômetro", "Balança"],
                "location": "1º Andar - Ala Norte",
                "occupancy_type": "fixed",
                "is_active": True,
                "fixed_schedule": {
                    "team": "ESF 5",
                    "start": "07:00",
                    "end": "16:00"
                }
            }
        ]
        
        db.consultorios.insert_many(consultorios_data)
        print(f"   ✅ {len(consultorios_data)} consultórios criados")
        
        # 3. Create Doctors
        print("👨‍⚕️ Criando médicos...")
        doctors_data = [
            {
                "id": str(uuid.uuid4()),
                "name": "Dr. João Silva",
                "specialty": "Clínico Geral",
                "crm": "12345-SP",
                "phone": "(11) 99999-1111",
                "email": "dr.silva@consultorio.com",
                "is_active": True
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Dra. Maria Santos",
                "specialty": "Pediatra", 
                "crm": "23456-SP",
                "phone": "(11) 99999-2222",
                "email": "dra.santos@consultorio.com",
                "is_active": True
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Dr. Carlos Oliveira",
                "specialty": "Cardiologista",
                "crm": "34567-SP",
                "phone": "(11) 99999-3333", 
                "email": "dr.oliveira@consultorio.com",
                "is_active": True
            }
        ]
        
        db.doctors.insert_many(doctors_data)
        print(f"   ✅ {len(doctors_data)} médicos criados")
        
        # 4. Create Patients
        print("🏥 Criando pacientes...")
        patients_data = [
            {
                "id": str(uuid.uuid4()),
                "name": "Ana Silva",
                "cpf": "123.456.789-01",
                "birth_date": "1985-03-15",
                "phone": "(11) 98888-1111",
                "email": "ana.silva@email.com",
                "address": "Rua das Flores, 123, Centro",
                "emergency_contact": "José Silva - (11) 98888-1112",
                "is_active": True
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Pedro Santos", 
                "cpf": "234.567.890-12",
                "birth_date": "1990-07-22",
                "phone": "(11) 98888-2222",
                "email": "pedro.santos@email.com", 
                "address": "Av. Principal, 456, Vila Nova",
                "emergency_contact": "Maria Santos - (11) 98888-2223",
                "is_active": True
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Carla Oliveira",
                "cpf": "345.678.901-23", 
                "birth_date": "1978-11-08",
                "phone": "(11) 98888-3333",
                "email": "carla.oliveira@email.com",
                "address": "Rua do Comércio, 789, Centro",
                "emergency_contact": "João Oliveira - (11) 98888-3334",
                "is_active": True
            }
        ]
        
        db.patients.insert_many(patients_data)
        print(f"   ✅ {len(patients_data)} pacientes criados")
        
        print("\n" + "="*50)
        print("🎉 POPULAÇÃO COMPLETA!")
        print("="*50)
        print(f"👥 Usuários: {db.users.count_documents({})}")
        print(f"🏥 Consultórios: {db.consultorios.count_documents({})}")
        print(f"👨‍⚕️ Médicos: {db.doctors.count_documents({})}")
        print(f"🏥 Pacientes: {db.patients.count_documents({})}")
        
        print("\n💡 Credenciais de acesso:")
        print("   👨‍💼 Admin: admin / admin123")
        print("   📞 Recepção: recepcao / recepcao123") 
        print("   👨‍⚕️ Médico: dr.silva / doctor123")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    populate_atlas_direct()
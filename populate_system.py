#!/usr/bin/env python3
"""
Sistema de Gestão de Consultórios - Script de População de Dados
Cria todos os médicos, pacientes e consultas de exemplo
"""

import requests
import json
from datetime import datetime, timedelta
import sys

BASE_URL = "http://localhost:8001"

def get_auth_token():
    """Get authentication token"""
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to authenticate: {response.status_code}")
        sys.exit(1)

def create_doctors(token):
    """Create all doctors for the system"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    doctors = [
        # ESF Doctors (C1-C5)
        {"name": "Dr. Ana Silva", "email": "ana.silva@esf1.com", "phone": "(11) 99001-0001", "crm": "CRM/SP 111001", "specialty": "ESF 1 - Medicina de Família"},
        {"name": "Dr. Bruno Santos", "email": "bruno.santos@esf2.com", "phone": "(11) 99002-0002", "crm": "CRM/SP 111002", "specialty": "ESF 2 - Medicina de Família"},
        {"name": "Dra. Carla Oliveira", "email": "carla.oliveira@esf3.com", "phone": "(11) 99003-0003", "crm": "CRM/SP 111003", "specialty": "ESF 3 - Medicina de Família"},
        {"name": "Dr. Daniel Costa", "email": "daniel.costa@esf4.com", "phone": "(11) 99004-0004", "crm": "CRM/SP 111004", "specialty": "ESF 4 - Medicina de Família"},
        {"name": "Dra. Elena Ferreira", "email": "elena.ferreira@esf5.com", "phone": "(11) 99005-0005", "crm": "CRM/SP 111005", "specialty": "ESF 5 - Medicina de Família"},
        
        # Specialists (C6-C8 Rotativo)
        {"name": "Dr. Fernando Cardoso", "email": "fernando.cardoso@cardio.com", "phone": "(11) 99006-0006", "crm": "CRM/SP 222001", "specialty": "Cardiologia"},
        {"name": "Dr. Lucas Barbosa", "email": "lucas.barbosa@cardio.com", "phone": "(11) 99007-0007", "crm": "CRM/SP 222002", "specialty": "Cardiologia"},
        {"name": "Dra. Gabriela Martins", "email": "gabriela.martins@acup.com", "phone": "(11) 99008-0008", "crm": "CRM/SP 333001", "specialty": "Acupuntura"},
        {"name": "Dr. Henrique Lima", "email": "henrique.lima@pediatria.com", "phone": "(11) 99009-0009", "crm": "CRM/SP 444001", "specialty": "Pediatria"},
        {"name": "Dra. Isabel Rocha", "email": "isabel.rocha@gineco.com", "phone": "(11) 99010-0010", "crm": "CRM/SP 555001", "specialty": "Ginecologia"},
        {"name": "Dr. João Pereira", "email": "joao.pereira@apoio.com", "phone": "(11) 99011-0011", "crm": "CRM/SP 666001", "specialty": "Médico Apoio"},
        {"name": "Dr. Ricardo Almeida", "email": "ricardo.almeida@apoio.com", "phone": "(11) 99012-0012", "crm": "CRM/SP 666002", "specialty": "Médico Apoio"},
        {"name": "Dra. Karen Silva", "email": "karen.silva@emulti.com", "phone": "(11) 99013-0013", "crm": "CRM/SP 777001", "specialty": "E-MULTI"},
        {"name": "Dr. Marcos Oliveira", "email": "marcos.oliveira@emulti.com", "phone": "(11) 99014-0014", "crm": "CRM/SP 777002", "specialty": "E-MULTI"}
    ]
    
    created_doctors = []
    for doctor in doctors:
        response = requests.post(f"{BASE_URL}/api/doctors", headers=headers, json=doctor)
        if response.status_code == 200:
            created_doctors.append(response.json())
            print(f"✅ Created doctor: {doctor['name']}")
        else:
            print(f"❌ Failed to create doctor: {doctor['name']} - {response.status_code}")
    
    return created_doctors

def create_patients(token):
    """Create patients for the system"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    patients = [
        {"name": "Maria da Silva Santos", "email": "maria.santos@email.com", "phone": "(11) 98701-1001", "cpf": "123.456.789-01", "birth_date": "1985-03-15T00:00:00Z", "address": "Rua das Flores, 123 - São Paulo, SP", "medical_history": "Hipertensão arterial controlada"},
        {"name": "José Carlos Oliveira", "email": "jose.oliveira@email.com", "phone": "(11) 98702-1002", "cpf": "234.567.890-12", "birth_date": "1970-07-20T00:00:00Z", "address": "Av. Paulista, 456 - São Paulo, SP", "medical_history": "Diabetes tipo 2, acompanhamento regular"},
        {"name": "Ana Paula Costa", "email": "ana.costa@email.com", "phone": "(11) 98703-1003", "cpf": "345.678.901-23", "birth_date": "1992-11-08T00:00:00Z", "address": "Rua Augusta, 789 - São Paulo, SP", "medical_history": "Gestante - 2º trimestre"},
        {"name": "Pedro Henrique Alves", "email": "pedro.alves@email.com", "phone": "(11) 98704-1004", "cpf": "456.789.012-34", "birth_date": "2010-05-12T00:00:00Z", "address": "Rua da Consolação, 321 - São Paulo, SP", "medical_history": "Acompanhamento pediátrico de rotina"},
        {"name": "Mariana Ferreira Lima", "email": "mariana.lima@email.com", "phone": "(11) 98705-1005", "cpf": "567.890.123-45", "birth_date": "1988-09-25T00:00:00Z", "address": "Rua Oscar Freire, 654 - São Paulo, SP", "medical_history": "Dor crônica - tratamento com acupuntura"},
        {"name": "Roberto Silva Mendes", "email": "roberto.mendes@email.com", "phone": "(11) 98706-1006", "cpf": "678.901.234-56", "birth_date": "1965-12-03T00:00:00Z", "address": "Av. Faria Lima, 987 - São Paulo, SP", "medical_history": "Cardiopatia - acompanhamento cardiológico"},
        {"name": "Fernanda Rodrigues", "email": "fernanda.rodrigues@email.com", "phone": "(11) 98707-1007", "cpf": "789.012.345-67", "birth_date": "1995-04-18T00:00:00Z", "address": "Rua Haddock Lobo, 234 - São Paulo, SP", "medical_history": "Acompanhamento ginecológico preventivo"},
        {"name": "Carlos Eduardo Pereira", "email": "carlos.pereira@email.com", "phone": "(11) 98708-1008", "cpf": "890.123.456-78", "birth_date": "1975-08-30T00:00:00Z", "address": "Av. Rebouças, 567 - São Paulo, SP", "medical_history": "Hipertensão e colesterol alto"},
        {"name": "Juliana Santos Martins", "email": "juliana.martins@email.com", "phone": "(11) 98709-1009", "cpf": "901.234.567-89", "birth_date": "1990-01-22T00:00:00Z", "address": "Rua Estados Unidos, 890 - São Paulo, SP", "medical_history": "Enxaqueca crônica - tratamento multidisciplinar"},
        {"name": "Antonio Marcos da Silva", "email": "antonio.silva@email.com", "phone": "(11) 98710-1010", "cpf": "012.345.678-90", "birth_date": "1955-06-14T00:00:00Z", "address": "Rua Teodoro Sampaio, 432 - São Paulo, SP", "medical_history": "Diabetes, hipertensão - ESF acompanhamento"},
        {"name": "Claudia Regina Souza", "email": "claudia.souza@email.com", "phone": "(11) 98711-1011", "cpf": "123.098.765-43", "birth_date": "1980-10-05T00:00:00Z", "address": "Av. Ipiranga, 1500 - São Paulo, SP", "medical_history": "Acompanhamento preventivo"},
        {"name": "Marcos Paulo Dias", "email": "marcos.dias@email.com", "phone": "(11) 98712-1012", "cpf": "321.654.987-21", "birth_date": "1968-04-30T00:00:00Z", "address": "Rua da Liberdade, 678 - São Paulo, SP", "medical_history": "Hipertensão, acompanhamento cardiológico"}
    ]
    
    created_patients = []
    for patient in patients:
        response = requests.post(f"{BASE_URL}/api/patients", headers=headers, json=patient)
        if response.status_code == 200:
            created_patients.append(response.json())
            print(f"✅ Created patient: {patient['name']}")
        else:
            print(f"❌ Failed to create patient: {patient['name']} - {response.status_code}")
    
    return created_patients

def create_appointments(token, doctors, patients):
    """Create sample appointments"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Get consultórios
    response = requests.get(f"{BASE_URL}/api/consultorios", headers=headers)
    if response.status_code != 200:
        print("Failed to get consultórios")
        return []
    consultorios = response.json()
    
    # Find consultórios by name
    c1 = next((c for c in consultorios if c['name'] == 'C1'), None)
    c2 = next((c for c in consultorios if c['name'] == 'C2'), None)
    c6 = next((c for c in consultorios if c['name'] == 'C6'), None)
    c7 = next((c for c in consultorios if c['name'] == 'C7'), None)
    c8 = next((c for c in consultorios if c['name'] == 'C8'), None)
    
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    appointments = [
        # ESF appointments in fixed consultórios
        {
            "patient_id": patients[0]["id"] if len(patients) > 0 else "",
            "doctor_id": doctors[0]["id"] if len(doctors) > 0 else "", # ESF 1
            "consultorio_id": c1["id"] if c1 else "",
            "appointment_date": f"{today.strftime('%Y-%m-%d')}T09:00:00Z",
            "duration_minutes": 30,
            "notes": "Consulta ESF 1 - acompanhamento hipertensão",
            "status": "scheduled"
        },
        {
            "patient_id": patients[1]["id"] if len(patients) > 1 else "",
            "doctor_id": doctors[1]["id"] if len(doctors) > 1 else "", # ESF 2
            "consultorio_id": c2["id"] if c2 else "",
            "appointment_date": f"{today.strftime('%Y-%m-%d')}T08:30:00Z",
            "duration_minutes": 30,
            "notes": "Consulta ESF 2 - diabetes acompanhamento",
            "status": "scheduled"
        },
        # Cardiology in C6 (rotativo)
        {
            "patient_id": patients[5]["id"] if len(patients) > 5 else "",
            "doctor_id": doctors[5]["id"] if len(doctors) > 5 else "", # Cardiologista
            "consultorio_id": c6["id"] if c6 else "",
            "appointment_date": f"{today.strftime('%Y-%m-%d')}T14:00:00Z",
            "duration_minutes": 45,
            "notes": "Consulta cardiológica - acompanhamento cardiopatia",
            "status": "scheduled"
        },
        # Pediatria in C7
        {
            "patient_id": patients[3]["id"] if len(patients) > 3 else "",
            "doctor_id": doctors[8]["id"] if len(doctors) > 8 else "", # Pediatra
            "consultorio_id": c7["id"] if c7 else "",
            "appointment_date": f"{today.strftime('%Y-%m-%d')}T10:00:00Z",
            "duration_minutes": 30,
            "notes": "Consulta pediátrica - acompanhamento crescimento",
            "status": "scheduled"
        },
        # E-MULTI in C8
        {
            "patient_id": patients[8]["id"] if len(patients) > 8 else "",
            "doctor_id": doctors[12]["id"] if len(doctors) > 12 else "", # E-MULTI
            "consultorio_id": c8["id"] if c8 else "",
            "appointment_date": f"{today.strftime('%Y-%m-%d')}T15:30:00Z",
            "duration_minutes": 45,
            "notes": "Consulta E-MULTI - tratamento multidisciplinar enxaqueca",
            "status": "scheduled"
        },
        # Tomorrow appointments
        {
            "patient_id": patients[4]["id"] if len(patients) > 4 else "",
            "doctor_id": doctors[7]["id"] if len(doctors) > 7 else "", # Acupunturista
            "consultorio_id": c6["id"] if c6 else "",
            "appointment_date": f"{tomorrow.strftime('%Y-%m-%d')}T09:00:00Z", # Tuesday - Acupuntura in C6
            "duration_minutes": 45,
            "notes": "Sessão de acupuntura - dor crônica",
            "status": "scheduled"
        }
    ]
    
    created_appointments = []
    for appointment in appointments:
        if appointment["patient_id"] and appointment["doctor_id"] and appointment["consultorio_id"]:
            response = requests.post(f"{BASE_URL}/api/appointments", headers=headers, json=appointment)
            if response.status_code == 200:
                created_appointments.append(response.json())
                print(f"✅ Created appointment: {appointment['notes']}")
            else:
                print(f"❌ Failed to create appointment: {appointment['notes']} - {response.status_code}")
                print(f"   Response: {response.text}")
        else:
            print(f"❌ Skipped appointment due to missing IDs: {appointment['notes']}")
    
    return created_appointments

def main():
    """Main execution"""
    print("🏥 SISTEMA DE GESTÃO DE CONSULTÓRIOS - POPULAÇÃO DE DADOS")
    print("=" * 60)
    
    # Get authentication token
    print("1. Getting authentication token...")
    token = get_auth_token()
    print("✅ Authentication successful")
    
    # Create doctors
    print("\n2. Creating doctors...")
    doctors = create_doctors(token)
    print(f"✅ Created {len(doctors)} doctors")
    
    # Create patients  
    print("\n3. Creating patients...")
    patients = create_patients(token)
    print(f"✅ Created {len(patients)} patients")
    
    # Create appointments
    print("\n4. Creating appointments...")
    appointments = create_appointments(token, doctors, patients)
    print(f"✅ Created {len(appointments)} appointments")
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 SISTEMA COMPLETAMENTE POPULADO!")
    print(f"📊 Total Médicos: {len(doctors)}")
    print(f"👥 Total Pacientes: {len(patients)}")
    print(f"📅 Total Consultas: {len(appointments)}")
    print(f"🏢 Total Consultórios: 8 (C1-C8)")
    print("\n🌐 Acesse: http://localhost:3000")
    print("🔑 Login: admin / admin123")

if __name__ == "__main__":
    main()
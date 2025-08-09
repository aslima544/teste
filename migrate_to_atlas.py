#!/usr/bin/env python3
"""
Script para migrar dados do MongoDB local para MongoDB Atlas
"""
import os
from pymongo import MongoClient
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def migrate_database():
    print("🔄 MIGRAÇÃO DE DADOS - LOCAL PARA ATLAS")
    print("=" * 50)
    
    # Conexões
    local_client = MongoClient("mongodb://localhost:27017")
    local_db = local_client["consultorio_db"]
    
    # Atlas connection - usando a string fornecida
    atlas_url = "mongodb+srv://admin:senha45195487@cluster0.8skwoca.mongodb.net/sistema_consultorio?retryWrites=true&w=majority&appName=Cluster0"
    atlas_client = MongoClient(atlas_url)
    atlas_db = atlas_client["sistema_consultorio"]  # Usando o nome do banco da URL
    
    # Collections to migrate
    collections = ["users", "patients", "doctors", "appointments", "consultorios", "procedimentos"]
    
    migration_report = {}
    
    for collection_name in collections:
        try:
            print(f"\n📊 Migrando coleção: {collection_name}")
            
            # Get data from local
            local_collection = local_db[collection_name]
            local_data = list(local_collection.find({}))
            
            if not local_data:
                print(f"   ⚠️  Coleção {collection_name} está vazia localmente")
                migration_report[collection_name] = {"status": "empty", "count": 0}
                continue
            
            # Clear Atlas collection (optional)
            atlas_collection = atlas_db[collection_name]
            atlas_collection.delete_many({})  # Remove existing data
            
            # Insert data to Atlas
            if local_data:
                atlas_collection.insert_many(local_data)
                print(f"   ✅ {len(local_data)} documentos migrados")
                migration_report[collection_name] = {"status": "success", "count": len(local_data)}
            
        except Exception as e:
            print(f"   ❌ Erro ao migrar {collection_name}: {str(e)}")
            migration_report[collection_name] = {"status": "error", "error": str(e)}
    
    # Migration summary
    print("\n" + "=" * 50)
    print("📋 RELATÓRIO DE MIGRAÇÃO:")
    print("=" * 50)
    
    total_migrated = 0
    for collection, report in migration_report.items():
        status_icon = "✅" if report["status"] == "success" else "⚠️" if report["status"] == "empty" else "❌"
        print(f"{status_icon} {collection}: {report.get('count', 0)} documentos")
        if report["status"] == "success":
            total_migrated += report["count"]
    
    print(f"\n🎉 TOTAL MIGRADO: {total_migrated} documentos")
    print("\n💡 Agora você pode usar as mesmas credenciais no Railway:")
    print("   Username: admin")
    print("   Password: admin123")
    
    # Close connections
    local_client.close()
    atlas_client.close()

def export_to_json():
    """Alternativa: exportar para JSON"""
    print("📁 EXPORTANDO DADOS PARA JSON")
    print("=" * 30)
    
    local_client = MongoClient("mongodb://localhost:27017")
    local_db = local_client["consultorio_db"]
    
    collections = ["users", "patients", "doctors", "appointments", "consultorios", "procedimentos"]
    
    export_data = {}
    
    for collection_name in collections:
        collection = local_db[collection_name]
        data = list(collection.find({}))
        
        # Convert ObjectId to string for JSON serialization
        for doc in data:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        
        export_data[collection_name] = data
        print(f"✅ {collection_name}: {len(data)} documentos")
    
    # Save to JSON file
    filename = f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n💾 Dados exportados para: {filename}")
    print("   Você pode usar este arquivo para importar manualmente no Atlas")
    
    local_client.close()

if __name__ == "__main__":
    print("🔄 INICIANDO MIGRAÇÃO AUTOMÁTICA PARA ATLAS")
    print("=" * 50)
    
    # Primeiro, vamos ver os dados locais
    local_client = MongoClient("mongodb://localhost:27017")
    local_db = local_client["consultorio_db"]
    
    print("📊 DADOS LOCAIS ENCONTRADOS:")
    collections = ["users", "patients", "doctors", "appointments", "consultorios", "procedimentos"]
    
    total_docs = 0
    for collection_name in collections:
        count = local_db[collection_name].count_documents({})
        total_docs += count
        print(f"   📁 {collection_name}: {count} documentos")
    
    print(f"\n📈 TOTAL: {total_docs} documentos para migrar")
    local_client.close()
    
    if total_docs == 0:
        print("⚠️  Nenhum dado encontrado localmente!")
        print("💡 Execute primeiro o populate_system.py localmente")
    else:
        print("\n" + "="*50)
        print("🔗 PARA CONTINUAR, VOCÊ PRECISA:")
        print("="*50)
        print("1. Connection string do MongoDB Atlas")
        print("2. Format: mongodb+srv://user:pass@cluster.mongodb.net/dbname")
        print("\n💡 Copie a string do Atlas e execute:")
        print(f'   python -c "from migrate_to_atlas import migrate_database; migrate_database()"')
        print("\n🔄 Ou execute diretamente com a string:")
        print('   export ATLAS_URL="sua-connection-string"')
        print("   python migrate_to_atlas.py")
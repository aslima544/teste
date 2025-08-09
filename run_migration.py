#!/usr/bin/env python3
"""
Script de migração interativo - execute este após ter a connection string
"""
from migrate_to_atlas import migrate_database

if __name__ == "__main__":
    print("🚀 MIGRAÇÃO INTERATIVA PARA ATLAS")
    print("=" * 40)
    print("\n📋 Você tem 58 documentos prontos para migração!")
    print("   👥 3 usuários")
    print("   🏥 12 pacientes") 
    print("   👨‍⚕️ 14 médicos")
    print("   📅 15 consultas")
    print("   🏥 8 consultórios")
    print("   📋 6 procedimentos")
    print("\n🔗 Cole sua connection string do Atlas abaixo:")
    
    migrate_database()
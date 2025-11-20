#!/usr/bin/env python3
"""Setup automático de entorno de desarrollo"""
import os
import subprocess
import sys

def setup():
    print("🚀 Configurando entorno de desarrollo ICFES...\n")

    # 1. Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requerido")
        sys.exit(1)

    # 2. Crear .env si no existe
    if not os.path.exists('.env'):
        print("📄 Creando .env desde .env.example...")
        subprocess.run(['cp', '.env.example', '.env'], check=True)
        print("✅ Archivo .env creado. ¡Edítalo con tus credenciales reales!")
    else:
        print("✅ Archivo .env ya existe")

    # 3. Instalar dependencias
    print("\n📦 Instalando dependencias...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)

    # 4. Generar claves
    print("\n🔑 Generando claves de prueba...")
    os.environ['FLASK_ENV'] = 'development'
    from scripts.generate_keys import generate_all_keys
    generate_all_keys()

    # 5. Crear directorios necesarios
    os.makedirs('logs', exist_ok=True)
    os.makedirs('instance', exist_ok=True)

    print("\n✅ Setup completado!")
    print("\nSiguientes pasos:")
    print("1. Edita el archivo .env con tus credenciales reales")
    print("2. Ejecuta: flask run")
    print("3. Corre tests: pytest -v")

if __name__ == "__main__":
    setup()

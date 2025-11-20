#!/usr/bin/env python3
"""Script para generar todas las claves necesarias"""
import os
import secrets
from cryptography.fernet import Fernet

def generate_all_keys():
    print("🔐 Generando claves de seguridad...\n")

    # Flask Secret Key
    flask_key = secrets.token_hex(32)
    print(f"FLASK_SECRET_KEY={flask_key}")

    # CSRF Secret Key
    csrf_key = secrets.token_hex(32)
    print(f"CSRF_SECRET_KEY={csrf_key}")

    # Fernet Encryption Key
    fernet_key = Fernet.generate_key().decode()
    print(f"ENCRYPTION_KEY={fernet_key}")

    # Admin Password (prompt)
    print("\n⚠️  Para ADMIN_PASSWORD_HASH:")
    print("1. Ejecuta: python -c \"from encryption import hash_text; print(hash_text('TU_PASSWORD'))\"")
    print("2. Copia el hash en tu .env")

if __name__ == "__main__":
    generate_all_keys()

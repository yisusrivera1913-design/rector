import os
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("ENCRYPTION_KEY")
if not KEY:
    raise Exception("ENCRYPTION_KEY no encontrada en variables de entorno")

# Fernet espera bytes
f = Fernet(KEY.encode() if isinstance(KEY, str) else KEY)

def encrypt_text(text: str) -> bytes:
    return f.encrypt(text.encode())

def decrypt_text(token: bytes) -> str:
    return f.decrypt(token).decode()

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

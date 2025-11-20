import pytest
import os
import tempfile
from datetime import datetime
from flask import Flask
from unittest.mock import Mock, patch
import sys
import io

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from cryptography.fernet import Fernet

@pytest.fixture
def app():
    """Crea app de Flask para testing"""
    # Usar database temporal para tests
    db_fd, db_path = tempfile.mkstemp()

    os.environ['FLASK_ENV'] = 'testing'
    os.environ['FLASK_SECRET_KEY'] = 'test-secret-key-1234567890abcdef'
    os.environ['ENCRYPTION_KEY'] = Fernet.generate_key().decode()
    os.environ['CSRF_SECRET_KEY'] = 'test-csrf-key-1234567890abcdef'
    os.environ['SUPABASE_URL'] = 'http://test.supabase.co'
    os.environ['SUPABASE_ANON_KEY'] = 'test-anon-key'
    os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'test-service-role-key'

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para tests unitarios

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Cliente de test para hacer requests"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner de CLI"""
    return app.test_cli_runner()

@pytest.fixture
def mock_supabase():
    """Mock de cliente Supabase"""
    with patch('supabase.create_client') as mock:
        client = Mock()
        client.table = Mock()
        client.rpc = Mock()
        mock.return_value = client
        yield client

@pytest.fixture
def encryption_manager():
    """Instancia de EncryptionManager para tests"""
    from encryption import encrypt_text, decrypt_text
    # Usar la implementación existente
    key = Fernet.generate_key().decode()
    os.environ['ENCRYPTION_KEY'] = key
    # Importar dinámicamente para evitar problemas
    import encryption
    return encryption

@pytest.fixture
def admin_logged_client(client):
    """Cliente con sesión de admin activa"""
    with client.session_transaction() as session:
        session['admin'] = True
        session['admin_pass_verified'] = True
        session['admin_last_activity'] = datetime.utcnow().isoformat()
    return client

@pytest.fixture
def student_logged_client(client, mock_supabase):
    """Cliente con sesión de estudiante activa"""
    # Mock usuario
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'nombre': 'Test Student', 'cedula_hash': 'test_hash'}
    ]

    with client.session_transaction() as session:
        session['user'] = {'id': 1, 'nombre': 'Test Student'}
        session['last_activity'] = datetime.utcnow().isoformat()

    return client

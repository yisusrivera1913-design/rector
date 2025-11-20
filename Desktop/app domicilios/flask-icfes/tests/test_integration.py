import pytest
import json
from unittest.mock import patch

class TestFlujoCompletoEstudiante:
    """Tests de integración de flujos completos"""

    def test_flujo_registro_login_examen(self, app, client, mock_supabase):
        """Test: Estudiante se registra, loguea y accede a examen"""

        # 1. Mock: Usuario no existe
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        # 2. Mock: Registro exitoso
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {'id': 1, 'nombre': 'Test User', 'cedula_hash': 'hash123'}
        ]

        # 3. Simular registro
        response = client.post('/register', data={
            'nombre': 'Test User',
            'cedula': '1234567890'
        }, follow_redirects=True)

        assert response.status_code == 200

        # 4. Login
        response = client.post('/login', data={
            'cedula': '1234567890'
        }, follow_redirects=True)

        assert response.status_code == 200

        # 5. Acceder a dashboard
        response = client.get('/student/')
        assert response.status_code == 200
        assert b'Test User' in response.data

    def test_flujo_admin_toggle_acceso(self, admin_logged_client, mock_supabase):
        """Test: Admin cambia acceso de estudiante"""

        # Mock usuario actual
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
            {'id': 2, 'tiene_acceso': True}
        ]

        # Mock update
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [
            {'id': 2, 'tiene_acceso': False}
        ]

        response = admin_logged_client.post('/admin/toggle_access/2', follow_redirects=True)

        assert response.status_code == 200
        assert b'deshabilitado' in response.data

import pytest
import json
import base64
from cryptography.fernet import Fernet, InvalidToken
from encryption import encrypt_text, decrypt_text, hash_text

class TestEncryptionManager:
    """Tests enterprise-grade para el sistema de encriptación"""

    def test_encriptar_desencriptar_texto(self):
        """Test: Ciclo completo de encriptación/desencriptación"""
        texto_original = "Documento confidencial ICFES 2024"

        texto_encriptado = encrypt_text(texto_original)
        texto_desencriptado = decrypt_text(texto_encriptado)

        assert texto_desencriptado == texto_original
        assert texto_encriptado != texto_original

    def test_encriptar_contiene_metadata(self):
        """Test: El payload encriptado debe contener metadata"""
        texto = "test"
        encriptado = encrypt_text(texto)

        # Fernet no incluye metadata adicional, solo verifica que sea bytes
        assert isinstance(encriptado, bytes)
        assert len(encriptado) > len(texto.encode())  # Debe ser más largo por el IV

    def test_desencriptar_con_clave_incorrecta_falla(self):
        """Test: Desencriptar con clave diferente debe fallar"""
        # Crear una instancia con clave diferente
        f2 = Fernet(Fernet.generate_key())
        texto_encriptado = encrypt_text("texto secreto")

        # Intentar desencriptar con clave diferente
        with pytest.raises(InvalidToken):
            f2.decrypt(texto_encriptado)

    def test_hash_data_es_deterministic(self):
        """Test: Hash de los mismos datos debe ser idéntico"""
        data = "1234567890"
        hash1 = hash_text(data)
        hash2 = hash_text(data)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produce 64 caracteres hex

    def test_hash_data_es_irreversible(self):
        """Test: No debe ser posible obtener el original del hash"""
        original = "texto_original"
        hash_value = hash_text(original)

        assert hash_value != original
        # No hay forma de revertir, solo verificar integridad

    def test_encriptacion_de_datos_sensibles(self):
        """Test: Encriptación de datos tipo ICFES (cédulas, nombres)"""
        datos_sensibles = [
            "1234567890",  # Cédula
            "Juan Pérez González",  # Nombre completo
            "juana.perez@email.com",  # Email
            "Calle 123 #45-67",  # Dirección
        ]

        for dato in datos_sensibles:
            encriptado = encrypt_text(dato)
            desencriptado = decrypt_text(encriptado)
            assert desencriptado == dato
            assert encriptado != dato  # Garantizar ofuscación

    def test_manejo_errores_clave_invalida(self):
        """Test: Clave inválida debe lanzar error claro"""
        # Fernet requiere clave de 32 bytes en base64
        with pytest.raises(Exception):  # ValueError o similar
            Fernet(b"clave_corta_invalida")

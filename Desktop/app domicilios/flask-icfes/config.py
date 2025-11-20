import os
from datetime import timedelta

class Config:
    """Configuración centralizada de la aplicación"""

    # Flask Security
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "cambia_esto_en_produccion")
    WTF_CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY", SECRET_KEY)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hora

    # Session Security
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
    SESSION_COOKIE_SAMESITE = "Lax"

    # Rate Limiting (básico)
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "10 per minute"

    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';",
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }

    # Admin Password Policy
    ADMIN_PASSWORD_MIN_LENGTH = 8

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "app.log")

    # Database
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # App
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

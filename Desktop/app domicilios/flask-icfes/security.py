from flask import request, Response, session, redirect, url_for, current_app
from functools import wraps
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def security_headers_decorator(f):
    """Aplica headers de seguridad a todas las respuestas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, Response):
            for header, value in current_app.config['SECURITY_HEADERS'].items():
                response.headers[header] = value
        return response
    return decorated_function

def require_auth(f):
    """Requiere autenticación de usuario"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            logger.warning(f"Intento de acceso sin autenticación a {request.path}")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Requiere autenticación de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            logger.warning(f"Intento de acceso a admin sin privilegios: {request.remote_addr}")
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def log_security_event(event_type: str, details: dict):
    """Loguea eventos de seguridad"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'event_type': event_type,
        'details': details
    }
    logger.info(f"SECURITY_EVENT: {log_entry}")

def rate_limit_check():
    """Verificación básica de rate limiting"""
    # Implementación simple - en producción usar Flask-Limiter
    now = time.time()
    requests = session.get('requests', [])
    # Limpiar requests antiguos (último minuto)
    requests = [r for r in requests if now - r < 60]
    requests.append(now)
    session['requests'] = requests

    if len(requests) > 10:  # 10 requests por minuto
        logger.warning(f"Rate limit excedido por {request.remote_addr}")
        return False
    return True

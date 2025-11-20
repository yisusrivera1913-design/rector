import os
import logging
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, g
from dotenv import load_dotenv
from config import DevelopmentConfig, ProductionConfig
from supabase_client import supabase
from encryption import encrypt_text, decrypt_text, hash_text
from security import security_headers_decorator
from auth import auth_bp
from admin_routes import admin_bp
from student_routes import student_bp
import time

load_dotenv()

# Configuración de la app
env = os.getenv("FLASK_ENV", "development")
if env == "production":
    config_class = ProductionConfig
else:
    config_class = DevelopmentConfig

app = Flask(__name__)
app.config.from_object(config_class)

# Configurar logging
logging.basicConfig(level=app.config['LOG_LEVEL'])
logger = logging.getLogger(__name__)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)

# Middleware de seguridad
@app.after_request
def set_security_headers(response):
    for header, value in app.config['SECURITY_HEADERS'].items():
        response.headers[header] = value
    return response

@app.before_request
def before_request():
    g.start_time = time.time()

# ---------- RUTAS PÚBLICAS ----------

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("admin", None)
    flash("Sesión cerrada", "info")
    return redirect(url_for("index"))

def create_app(config_class=None):
    """Factory function para crear la aplicación Flask"""
    if config_class is None:
        env = os.getenv("FLASK_ENV", "development")
        if env == "production":
            config_class = ProductionConfig
        else:
            config_class = DevelopmentConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configurar logging
    logging.basicConfig(level=app.config['LOG_LEVEL'])
    logger = logging.getLogger(__name__)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)

    # Middleware de seguridad
    @app.after_request
    def set_security_headers(response):
        for header, value in app.config['SECURITY_HEADERS'].items():
            response.headers[header] = value
        return response

    @app.before_request
    def before_request():
        g.start_time = time.time()

    # ---------- RUTAS PÚBLICAS ----------

    @app.route("/")
    def index():
        user = session.get("user")
        return render_template("index.html", user=user)

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        session.pop("admin", None)
        flash("Sesión cerrada", "info")
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)

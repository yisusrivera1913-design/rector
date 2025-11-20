from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from forms import RegistrationForm, LoginForm
from encryption import encrypt_text, hash_text
from security import require_auth, log_security_event, rate_limit_check
from supabase_client import supabase
import base64

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if not rate_limit_check():
        flash("Demasiados intentos. Intente más tarde.", "error")
        return redirect(url_for('auth.register'))

    form = RegistrationForm()
    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        cedula = form.cedula.data.strip()

        cedula_hash = hash_text(cedula)

        # Check if cedula already exists
        existing_user = supabase.table("usuarios").select("*").eq("cedula_hash", cedula_hash).execute()
        if existing_user.data:
            log_security_event("registration_failed", {"reason": "cedula_already_exists", "cedula_hash": cedula_hash[:8] + "..."})
            flash("Esta cédula ya está registrada.", "error")
            return redirect(url_for('auth.register'))

        cedula_cifrada = encrypt_text(cedula)
        cedula_cifrada_b64 = base64.b64encode(cedula_cifrada).decode('utf-8')

        supabase.table("usuarios").insert({
            "nombre": nombre,
            "cedula_hash": cedula_hash,
            "cedula_cifrada": cedula_cifrada_b64,
            "tiene_acceso": False  # Default to no access, admin must grant
        }).execute()

        log_security_event("user_registered", {"cedula_hash": cedula_hash[:8] + "..."})
        flash("Registrado con éxito. Ahora puede iniciar sesión.", "success")

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if not rate_limit_check():
        flash("Demasiados intentos. Intente más tarde.", "error")
        return redirect(url_for('auth.login'))

    form = LoginForm()
    if form.validate_on_submit():
        cedula = form.cedula.data.strip()
        cedula_hash = hash_text(cedula)

        resp = supabase.table("usuarios").select("*").eq("cedula_hash", cedula_hash).execute()
        if not resp.data:
            log_security_event("login_failed", {"reason": "user_not_found"})
            flash("Cédula no encontrada", "error")
            return redirect(url_for('auth.login'))

        user = resp.data[0]
        if not user.get("tiene_acceso", False):
            log_security_event("login_failed", {"reason": "no_access", "user_id": user["id"]})
            flash("Aún no tienes acceso. Pide al administrador.", "error")
            return redirect(url_for('auth.login'))

        session["user"] = {
            "id": user["id"],
            "nombre": user["nombre"]
        }
        log_security_event("login_success", {"user_id": user["id"]})
        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for('student.student_panel'))

    return render_template("login.html", form=form)

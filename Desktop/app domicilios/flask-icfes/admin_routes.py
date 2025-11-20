from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from forms import AdminLoginForm
from security import require_admin, log_security_event
from encryption import decrypt_text
from supabase_client import supabase
import base64
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        password = form.password.data
        admin_pass = os.getenv("ADMIN_PASSWORD")

        if password == admin_pass:
            session['admin'] = True
            log_security_event("admin_login_success", {"ip": request.remote_addr})

            return redirect(url_for('admin.admin_panel'))
        else:
            log_security_event("admin_login_failed", {"ip": request.remote_addr})
            flash("Clave admin incorrecta", "error")
            return render_template("admin.html", form=form, admin=False)

    return render_template("admin.html", form=form, admin=False)

def decrypt_user_cedulas(users):
    """Decrypt cedulas for admin display with strict error handling"""
    for u in users:
        try:
            enc = u.get("cedula_cifrada")
            if isinstance(enc, str):
                # Handle escaped bytes string from database
                if enc.startswith("\\x"):
                    # Convert escaped hex string to bytes
                    hex_str = enc.replace("\\x", "")
                    enc_b = bytes.fromhex(hex_str)
                else:
                    # Clean the base64 string by removing whitespace and ensuring proper padding
                    enc_clean = enc.strip()
                    # Add padding if needed
                    missing_padding = len(enc_clean) % 4
                    if missing_padding:
                        enc_clean += '=' * (4 - missing_padding)
                    enc_b = base64.b64decode(enc_clean)
            else:
                enc_b = enc
            u["cedula_descifrada"] = decrypt_text(enc_b)
        except Exception as e:
            log_security_event("cedula_decrypt_error", {"user_id": u.get("id"), "error": str(e)})
            u["cedula_descifrada"] = "[error al descifrar]"
    return users

def auto_grant_access_to_new_users():
    """Strictly grant access to users without access, return count of granted users"""
    try:
        resp = supabase.table("usuarios").select("*").eq("tiene_acceso", False).execute()
        new_users = resp.data or []

        if not new_users:
            return 0

        granted_count = 0
        for u in new_users:
            # Double-check access status before granting
            current_status = supabase.table("usuarios").select("tiene_acceso").eq("id", u["id"]).execute()
            if current_status.data and not current_status.data[0].get("tiene_acceso", False):
                supabase.table("usuarios").update({"tiene_acceso": True}).eq("id", u["id"]).execute()
                log_security_event("admin_auto_grant_access", {"user_id": u["id"]})
                granted_count += 1

        return granted_count
    except Exception as e:
        log_security_event("auto_grant_access_error", {"error": str(e)})
        return 0

@admin_bp.route("/panel")
@require_admin
def admin_panel():
    # Get user data - no auto-grant on panel visits, only on login
    resp = supabase.table("usuarios").select("*").order("created_at", desc=True).execute()
    users = resp.data or []

    # Decrypt cedulas with strict error handling
    users = decrypt_user_cedulas(users)

    return render_template("admin.html", admin=True, users=users)

def validate_user_exists(user_id):
    """Strictly validate user exists and return user data"""
    try:
        resp = supabase.table("usuarios").select("*").eq("id", user_id).execute()
        if not resp.data:
            return None
        return resp.data[0]
    except Exception as e:
        log_security_event("user_validation_error", {"user_id": user_id, "error": str(e)})
        return None

def update_user_access(user_id, new_access_state):
    """Strictly update user access with validation"""
    try:
        # Verify user exists before update
        user = validate_user_exists(user_id)
        if not user:
            return False, "Usuario no encontrado"

        # Update access
        supabase.table("usuarios").update({"tiene_acceso": new_access_state}).eq("id", user_id).execute()

        # Log the change
        log_security_event("admin_toggle_access", {
            "target_user_id": user_id,
            "new_state": new_access_state,
            "previous_state": user.get("tiene_acceso", False)
        })

        return True, "Acceso actualizado"
    except Exception as e:
        log_security_event("access_update_error", {"user_id": user_id, "error": str(e)})
        return False, "Error al actualizar acceso"

@admin_bp.route("/toggle_access/<user_id>", methods=["POST"])
@require_admin
def toggle_access(user_id):
    # Validate user exists
    user = validate_user_exists(user_id)
    if not user:
        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
        flash("Usuario no encontrado", "error")
        return redirect(url_for('admin.admin_panel'))

    # Calculate new access state
    current_access = user.get("tiene_acceso", False)
    new_access = not current_access

    # Update access with strict validation
    success, message = update_user_access(user_id, new_access)

    if success:
        # If revoking access, clear any active sessions for this user
        if not new_access:
            # Note: In a real app, you'd want to invalidate sessions properly
            # For now, we'll just log that access was revoked
            log_security_event("access_revoked_logout_required", {"user_id": user_id})

        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return jsonify({"success": True, "message": "Guardado", "new_state": new_access})
        flash(message, "success")
    else:
        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return jsonify({"success": False, "message": message}), 400
        flash(message, "error")

    return redirect(url_for('admin.admin_panel'))

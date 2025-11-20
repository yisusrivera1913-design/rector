from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
import re
from encryption import hash_text
from supabase_client import supabase

class RegistrationForm(FlaskForm):
    """Formulario de registro con validación"""

    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message="Nombre es obligatorio"),
        Length(min=3, max=100, message="Nombre debe tener 3-100 caracteres"),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message="Solo letras y espacios")
    ])

    cedula = StringField('Cédula', validators=[
        DataRequired(message="Cédula es obligatoria"),
        Length(min=6, max=20, message="Cédula inválida"),
        Regexp(r'^[0-9]+$', message="Solo números permitidos")
    ])

    def validate_cedula(self, field):
        """Valida que la cédula no esté registrada"""
        cedula_hash = hash_text(field.data.strip())
        resp = supabase.table("usuarios").select("id").eq("cedula_hash", cedula_hash).execute()
        if resp.data:
            raise ValidationError("Esta cédula ya está registrada")

class LoginForm(FlaskForm):
    """Formulario de login"""

    cedula = StringField('Cédula', validators=[
        DataRequired(),
        Length(min=6, max=20)
    ])

class AdminLoginForm(FlaskForm):
    """Formulario de admin"""

    password = PasswordField('Password Admin', validators=[
        DataRequired(),
        Length(min=8, message="Mínimo 8 caracteres")
    ])

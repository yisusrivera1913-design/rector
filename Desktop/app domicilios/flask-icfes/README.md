# Flask ICFES App

Aplicación web para estudiantes de ICFES con registro seguro, panel de administración y simulacros de exámenes.

## Características

- Registro y login de estudiantes con encriptación de datos sensibles (cédula).
- Panel de administración para gestionar acceso de estudiantes.
- Generador de simulacros ICFES con preguntas de opción múltiple.
- Almacenamiento en Supabase (PostgreSQL).

## Instalación

1. Clona el repositorio.
2. Instala dependencias: `pip install -r requirements.txt`
3. Copia `.env.example` a `.env` y configura las variables:
   - `FLASK_SECRET_KEY`: Clave secreta para sesiones.
   - `SUPABASE_URL`: URL de tu proyecto Supabase.
   - `SUPABASE_SERVICE_ROLE_KEY`: Clave de servicio de Supabase.
   - `ENCRYPTION_KEY`: Clave Fernet para encriptación (genera una segura).
   - `ADMIN_PASSWORD`: Contraseña para acceso admin.
4. Configura las tablas en Supabase ejecutando el script `create_tables.sql` en el SQL Editor de Supabase.
5. Ejecuta: `python app.py`

## Seguridad en Plataformas de Despliegue

### General
- Usa HTTPS siempre (configura SSL/TLS).
- Almacena variables de entorno de forma segura (no en código).
- Habilita 2FA en cuentas de despliegue.
- Monitorea logs y auditorías.
- Cumple con leyes de protección de datos (e.g., Habeas Data en Colombia).

### Heroku
- Configura variables de entorno en Dashboard.
- Usa Heroku Postgres si no usas Supabase.
- Habilita SSL automático.
- Configura logs: `heroku logs --tail`

### Vercel
- Usa Vercel Secrets para env vars.
- Configura `vercel.json` para rutas.
- Habilita HTTPS automático.
- Monitorea con Vercel Analytics.

### Railway
- Configura env vars en Dashboard.
- Usa Railway Postgres si aplica.
- Habilita SSL.
- Logs en Dashboard.

### Render
- Configura env vars en Dashboard.
- Usa Render Postgres.
- SSL automático.
- Logs en Dashboard.

## Mejoras Futuras
- Más preguntas en base de datos.
- UI mejorada con CSS/JS.
- Autenticación OAuth.
- Reportes de resultados.

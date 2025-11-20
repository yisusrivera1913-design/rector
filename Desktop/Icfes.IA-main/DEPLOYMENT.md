# 🚀 Guía de Deployment - ICFES App

## ⚠️ ANTES DE SUBIR A PRODUCCIÓN

### 1. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (NO lo subas a Git):

```bash
GOOGLE_API_KEY=tu_api_key_de_google_gemini
FLASK_ENV=production
SECRET_KEY=genera_una_clave_secreta_aleatoria
```

### 2. Verificar que `.gitignore` existe
```bash
# Verifica que estos archivos NO se suban:
- .env
- __pycache__/
- *.pyc
```

### 3. Deployment en Render/Railway/Heroku

#### Variables de Entorno a Configurar:
- `GOOGLE_API_KEY`: Tu API key de Google Gemini
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Clave secreta aleatoria (mínimo 32 caracteres)
- `CORS_ORIGINS`: Tu dominio de producción (ej: https://tu-app.onrender.com)

#### Comando de Inicio:
```bash
gunicorn app:application
```

### 4. Deployment en Vercel

Vercel soporta aplicaciones Flask mediante funciones serverless. Sigue estos pasos:

#### Preparación:
- Asegúrate de tener `vercel.json` en la raíz (ya creado).
- `requirements.txt` debe incluir todas las dependencias (ya configurado).
- El archivo `app.py` expone `application = app` para WSGI.

#### Pasos para Desplegar:
1. **Instala Vercel CLI** (opcional, para deploy local):
   ```bash
   npm i -g vercel
   ```

2. **Inicializa Git** (ya hecho: `git init`):
   ```bash
   git add .
   git commit -m "Initial commit for Vercel deployment"
   ```

3. **Crea un repositorio en GitHub** y sube el código:
   ```bash
   git remote add origin https://github.com/tu-usuario/tu-repo.git
   git branch -M main
   git push -u origin main
   ```

4. **Importa el repositorio en Vercel**:
   - Ve a [vercel.com](https://vercel.com) y crea una cuenta.
   - Haz clic en "New Project" > Importa desde GitHub.
   - Selecciona el repositorio.
   - Configura el framework como "Other" (Python detectado automáticamente).

5. **Configura Variables de Entorno en Vercel**:
   - En el dashboard del proyecto: Settings > Environment Variables.
   - Agrega:
     - `GOOGLE_API_KEY`: Tu API key de Google Gemini
     - `FLASK_ENV`: `production`
     - `SECRET_KEY`: Genera una clave secreta (e.g., `python -c 'import secrets; print(secrets.token_hex(16))'`)
     - `CORS_ORIGINS`: Tu dominio de Vercel (e.g., `https://tu-app.vercel.app`) o `*` para desarrollo (no recomendado en prod).

6. **Despliega**:
   - Vercel build y deploy automáticamente.
   - URL: `https://tu-app.vercel.app`

#### Notas para Vercel:
- Funciones serverless: timeouts ~10s, ajusta prompts si es necesario.
- Archivos estáticos (static/, templates/): Servidos automáticamente.
- Logs: Revisa en Vercel dashboard > Functions.
- Custom Domain: Configura en Settings > Domains.

Si usas Vercel CLI:
```bash
vercel --prod
```

### 4. Checklist de Seguridad

- [x] Archivo `.env` creado y NO incluido en Git
- [x] Variables de entorno configuradas en plataforma de deployment
- [x] API keys removidas del código fuente
- [x] `.gitignore` configurado correctamente
- [x] `debug=False` en producción (ya configurado con gunicorn)
- [x] Usuarios demo eliminados
- [x] CORS configurado apropiadamente para tu dominio (actualiza origins en icfes_api.py con tu dominio de producción)

### 5. Testing Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env con tus credenciales

# Ejecutar en modo desarrollo
python app.py

# Ejecutar en modo producción (local)
gunicorn app:application
```

## 📝 Notas Importantes

- **NUNCA** subas archivos `.env` a Git
- **NUNCA** hardcodees API keys en el código
- Usa variables de entorno en todas las plataformas
- El archivo `.env.example` muestra qué variables necesitas (sin valores reales)
- La autenticación se maneja completamente con Supabase (frontend)

## 🔒 Seguridad Frontend (Supabase)

Las credenciales de Supabase están en `static/js/config.js`:
- En desarrollo: usa valores por defecto
- En producción: configura `window.ENV` en tu servidor

## 📊 Endpoints Disponibles

- POST /generate-question - Generar preguntas ICFES
- POST /get-feedback - Retroalimentación individual
- POST /analyze-document - Análisis PDF/Word completo
- POST /generate-visual - Generar gráficos (bar/pie)
- POST /save-model - Guardar modelo entrenado
- GET /users - Lista de usuarios
- GET /health - Estado del sistema
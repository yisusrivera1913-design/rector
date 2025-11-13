@echo off
echo Iniciando servidor en modo desarrollo...
set FLASK_ENV=development
set CORS_ORIGINS=*
set GOOGLE_API_KEY=AIzaSyDBv91sukUg8BHVLde_1Jf5LjTNUyN4eKE
set SECRET_KEY=dev_secret_key_12345
python app.py

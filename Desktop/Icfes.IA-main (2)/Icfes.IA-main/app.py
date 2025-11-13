from flask import render_template, redirect
from icfes_api import app

# Rutas de páginas (Front)
@app.route('/')
@app.route('/login')
@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/simulator')
def simulator_page():
    return render_template('icfes_exam_simulator.html')

@app.route('/generator')
def generator_page():
    return render_template('icfes_generator_mcq.html')

@app.route('/pdf-evaluation')
def pdf_evaluation_page():
    return render_template('icfes_pdf_evaluation.html')

@app.route('/order-exercise')
def order_exercise_page():
    return render_template('icfes_order_exercise.html')

if __name__ == '__main__':
    import os
    host = '0.0.0.0' if os.getenv('FLASK_ENV') == 'production' else '127.0.0.1'
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host=host, port=5000)
else:
    # Para producción con gunicorn
    application = app

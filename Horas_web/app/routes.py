from flask import render_template, request, redirect, flash
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/guardar_horas', methods=['POST'])
def guardar_horas():
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    horas_35 = request.form['horas_35']
    horas_100 = request.form['horas_100']
    comentario = request.form.get('comentario', '')

    # Validación mejorada del formato
    import re
    hora_pattern = r'^[0-9]:[0-5][0-9]$'
    
    if not re.match(hora_pattern, horas_35) or not re.match(hora_pattern, horas_100):
        flash('Formato de horas inválido. Use H:MM (ej: 2:30)')
        return redirect('/registro')

    # Aquí guardarías los datos en la base de datos.
    # Ejemplo de impresión para pruebas (luego reemplazar con lógica real)
    print(f"Datos recibidos: {codigo}, {nombre}, {fecha}, {horas_35}, {horas_100}, {comentario}")
    flash('Registro guardado exitosamente.')
    return redirect('/')
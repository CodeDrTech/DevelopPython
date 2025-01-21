from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)

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

    # Validación del formato de horas
    import re
    if not re.match(r'^[0-9]:[0-5][0-9]$', horas_35):
        flash('El campo Horas al 35% tiene un formato inválido.')
        return redirect('/registro')
    if not re.match(r'^[0-9]:[0-5][0-9]$', horas_100):
        flash('El campo Horas al 100% tiene un formato inválido.')
        return redirect('/registro')

    # Aquí guardarías los datos en la base de datos.
    # Ejemplo de impresión para pruebas (luego reemplazar con lógica real)
    print(f"Datos recibidos: {codigo}, {nombre}, {fecha}, {horas_35}, {horas_100}, {comentario}")
    flash('Registro guardado exitosamente.')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

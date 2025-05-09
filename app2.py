from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data/registros.json'

TIPOS_TRAMITE = [
    (1, 'Obra nueva'),
    (2, 'Regularizacion'),
    (3, 'Ampliacion'),
    (4, 'Modificacion'),
    (5, 'Remodelacion'),
    (6, 'Demolicion'),
    (7, 'Muros de delimitacion (bardeo)'),
    (8, 'Alineamiento'),
    (9, 'Acabados'),
    (10, 'Revalidacion'),
    (11, 'Pintura de fachada'),
    (12, 'Suspension temporal de obra'),
    (13, 'Cambio de propietario'),
    (14, 'Cambio del/de la D.R.O.'),
    (15, 'Obras menores'),
    (16, 'Cambio de proyecto'),
    (17, 'Invasion de la via publica'),
    (18, 'Validacion'),
    (19, 'Integral 1: Licencia (regularizacion) y Terminacion de Obra')
]

# Asegurar que existe el archivo de datos
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/', methods=['GET'])
def index():
    data = {
        'titulo': 'Bitácora de Obra',
        'tipos_tramite': TIPOS_TRAMITE
    }
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    registro_json = {}
    print("request.form")
    for key in request.form:
        registro_json[key] = request.form[key]


    #return jsonify(registro_json)
    print("si llega aqui??")
    # registro = {
    #     "id_obra":request.form['id_obra'],
    #     "nombre_obra": request.form['nombre_obra'],
    #     "direccion": request.form['direccion'],
    #     "tramites": request.form['tramites'],
    #     "tipo_uso": request.form['tipo_uso'],
    #     "dictamen_comercial_texto": request.form['dictamen_comercial_texto'],
    #     "dictamen_industrial": request.form['dictamen_industrial'],
    #     "licencia": request.form['licencia'],
    #     "clave_catastral": request.form['clave_catastral'],
    #     "propietario_nombre": request.form['propietario_nombre'],
    #     "datos_dro": request.form['datos_dro'],
    #     "fechas": request.form['fechas'],
    #     "numero_contrato": request.form['numero_contrato'],
    # }
    # print(registro)
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        data.append(registro_json)
        f.seek(0)
        json.dump(data, f, indent=4)
    return redirect(url_for('ver_registros'))

# @app.route('/', methods=['GET', 'POST'])
# def formulario():
#     seleccionados = []
#     if request.method == 'POST':
#         ids_seleccionados = request.form.getlist('tramites')
#         seleccionados = [texto for (id, texto) in TIPOS_TRAMITE if str(id) in ids_seleccionados]
#         print(seleccionados)
#     return render_template_string(HTML_FORM, tipos=TIPOS_TRAMITE, seleccionados=seleccionados)


@app.route('/registros')
def ver_registros():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return render_template('registros.html', registros=data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, send_file, redirect, url_for
from datetime import datetime
from io import BytesIO
import json
import os

app = Flask(__name__)
DATA_FILE = 'data/registros.json'

# Asegurar que existe el archivo de datos
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    registro = {
        "clave_obra": request.form["clave_obra"],
        "nombre_obra": request.form["nombre_obra"],
        "direccion_predio": request.form["direccion_predio"],
        "tipo_obra": request.form["tipo_obra"],
        "descripcion_cambios": request.form.get("descripcion_cambios") if request.form["tipo_obra"] == "remodelacion" else None,
        "numero_licencia": request.form["numero_licencia"],
        "datos_propietario": request.form["datos_propietario"],
        "datos_dro": request.form["datos_dro"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"],
        "numero_contrato": request.form.get("numero_contrato"),
        "fecha_envio": datetime.now().isoformat()
    }

    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        data.append(registro)
        f.seek(0)
        json.dump(data, f, indent=4)
    return redirect(url_for('ver_registros'))

@app.route('/registros')
def ver_registros():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return render_template('registros.html', registros=data)

    # json_data = json.dumps(registro, indent=2, ensure_ascii=False)
    # tipo = data['tipo_obra']
    # fecha = datetime.now().isoformat().replace(":", "-")
    # filename = f"bitacora_{tipo}_{fecha}.json"
    #
    # return send_file(BytesIO(json_data.encode('utf-8')),
    #                  mimetype='application/json',
    #                  as_attachment=True,
    #                  download_name=filename)

if __name__ == "__main__":
    app.run(debug=True)



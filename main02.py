from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario_bitacora.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.form.to_dict(flat=False)
    # Aquí podrías guardarlos en una base de datos
    print("Datos recibidos:")
    for clave, valor in datos.items():
        print(f"{clave}: {valor}")
    return "Datos recibidos correctamente"

if __name__ == '__main__':
    app.run(debug=True)
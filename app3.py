from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def mostrar_formulario():
    return render_template('bitacora_obra.html')

@app.route('/guardar_informacion', methods=['POST'])
def guardar_informacion():
    registro_json = {}
    for key in request.form:
        registro_json[key] = request.form[key]

    return jsonify(registro_json)

if __name__ == '__main__':
    app.run(debug=True)
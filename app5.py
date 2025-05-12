from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_mysqldb import MySQL
import mysql.connector

import json
import os
import pymysql

app = Flask(__name__)


# conn = mysql.connector.connect(host="localhost",
#                                           database="bitacora_obra",
#                                           user="root",
#                                           password="Pampi2012") # Reemplazar con tus credenciales
#            cursor = conn.cursor()
#Conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pampi2012$'
app.config['MYSQL_DB'] = 'bitacora_obra'

conexion = MySQL(app)

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


@app.route('/')
def formulario():
    data = {
        'tipos_tramite': TIPOS_TRAMITE
    }
    return render_template('formulario_bitacora_accordion.html', data=data)
    #formulario_bitacora_accordion


@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.form.to_dict(flat=False)

    try:
        cursor = conexion.connection.cursor()

        sql = """
            INSERT INTO registro_obras (
                nombre_obra, direccion, tramites, tipo_uso,
                dictamen_comercial_texto, dictamen_industrial_texto, licencia, clave_catastral,
                propietario_nombre, propietario_direccion, propietario_rfc,
                dro_nombre, dro_cedula, dro_colegio, dro_registro_colegio, dro_registro_municipal,
                estructura_nombre, estructura_cedula, estructura_colegio, estructura_registro_colegio, estructura_registro_municipal,
                instalaciones_nombre, instalaciones_cedula, instalaciones_colegio, instalaciones_registro_colegio, instalaciones_registro_municipal,
                diseno_nombre, diseno_cedula, diseno_colegio, diseno_registro_colegio, diseno_registro_municipal,
                gas_nombre, gas_cedula, gas_colegio, gas_registro_colegio, gas_registro_municipal,
                fecha_inicio, fecha_termino, numero_contrato
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            datos.get("nombre_obra", [""])[0],
            datos.get("direccion", [""])[0],
            ",".join(request.form.getlist("tramites")),
            datos.get("tipo_uso", [""])[0],
            datos.get("dictamen_comercial_texto", [""])[0],
            datos.get("dictamen_industrial_texto", [""])[0],
            datos.get("licencia", [""])[0],
            datos.get("clave_catastral", [""])[0],
            datos.get("propietario_nombre", [""])[0],
            datos.get("propietario_direccion", [""])[0],
            datos.get("propietario_rfc", [""])[0],
            datos.get("dro_nombre", [""])[0],
            datos.get("dro_cedula", [""])[0],
            datos.get("dro_colegio", [""])[0],
            datos.get("dro_registro_colegio", [""])[0],
            datos.get("dro_registro_municipal", [""])[0],
            datos.get("estructura_nombre", [""])[0],
            datos.get("estructura_cedula", [""])[0],
            datos.get("estructura_colegio", [""])[0],
            datos.get("estructura_registro_colegio", [""])[0],
            datos.get("estructura_registro_municipal", [""])[0],
            datos.get("instalaciones_nombre", [""])[0],
            datos.get("instalaciones_cedula", [""])[0],
            datos.get("instalaciones_colegio", [""])[0],
            datos.get("instalaciones_registro_colegio", [""])[0],
            datos.get("instalaciones_registro_municipal", [""])[0],
            datos.get("diseno_nombre", [""])[0],
            datos.get("diseno_cedula", [""])[0],
            datos.get("diseno_colegio", [""])[0],
            datos.get("diseno_registro_colegio", [""])[0],
            datos.get("diseno_registro_municipal", [""])[0],
            datos.get("gas_nombre", [""])[0],
            datos.get("gas_cedula", [""])[0],
            datos.get("gas_colegio", [""])[0],
            datos.get("gas_registro_colegio", [""])[0],
            datos.get("gas_registro_municipal", [""])[0],
            datos.get("fecha_inicio", [""])[0],
            datos.get("fecha_termino", [""])[0],
            datos.get("numero_contrato", [""])[0],
        )
        cursor.execute(sql, valores)
        conexion.connection.commit()
        cursor.close()

        #datos = request.form.to_dict(flat=False)
        registro_json = {}
        print("Datos recibidos:")
        for clave, valor in datos.items():
            registro_json[clave] = request.form[clave]
        #print(f" jason {jsonify(registro_json)}")
        return "Datos guardados correctamente"#, jsonify(registro_json)
    except Exception as e:
        return f"Error al guardar: {str(e)}"

@app.route('/buscar_bitacora')
def buscar_bitacora():
    return render_template('buscar_bitacora.html')


@app.route('/editar/<id>', methods=['GET'])
def editar_registro():
    print(f"valor del id {id}")
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM registro_obras WHERE id = %s"
        #print(f"id {id}")
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        #cursor.close()

        if registro:
            #print(f"veamos el registro 2 {registro}")
            #print(f"cursor.description {cursor.description}")
            # Convertir la tupla del registro a un diccionario para facilitar el acceso en el template
            column_names = [column[0] for column in cursor.description]
            #print(f"column_names {column_names}")
            data = dict(zip(column_names, registro))
            cursor.close()
            # Separar los trámites (que están guardados como una cadena separada por comas)
            if data.get('tramites'):
                data['tramites'] = data['tramites'].split(',')

            return render_template('formulario_editar_bitacora.html', data=data, tipos_tramite=TIPOS_TRAMITE)
        else:
            return "Registro no encontrado."

    except Exception as e:
        return f"Error al cargar el registro para editar: {str(e)}"

@app.route('/actualizar/<id>', methods=['POST'])
#@app.route('/actualizar', methods=['POST'])
def actualizar_registro(id):
    datos = request.form.to_dict(flat=False)
    try:
        cursor = conexion.connection.cursor()
        sql = """
            UPDATE registro_obras SET
                nombre_obra = %s,
                direccion = %s,
                tramites = %s,
                tipo_uso = %s,
                dictamen_comercial_texto = %s,
                dictamen_industrial_texto = %s,
                licencia = %s,
                clave_catastral = %s,
                propietario_nombre = %s,
                propietario_direccion = %s,
                propietario_rfc = %s,
                dro_nombre = %s,
                dro_cedula = %s,
                dro_colegio = %s,
                dro_registro_colegio = %s,
                dro_registro_municipal = %s,
                estructura_nombre = %s,
                estructura_cedula = %s,
                estructura_colegio = %s,
                estructura_registro_colegio = %s,
                estructura_registro_municipal = %s,
                instalaciones_nombre = %s,
                instalaciones_cedula = %s,
                instalaciones_colegio = %s,
                instalaciones_registro_colegio = %s,
                instalaciones_registro_municipal = %s,
                diseno_nombre = %s,
                diseno_cedula = %s,
                diseno_colegio = %s,
                diseno_registro_colegio = %s,
                diseno_registro_municipal = %s,
                gas_nombre = %s,
                gas_cedula = %s,
                gas_colegio = %s,
                gas_registro_colegio = %s,
                gas_registro_municipal = %s,
                fecha_inicio = %s,
                fecha_termino = %s,
                numero_contrato = %s
            WHERE id = %s
        """
        valores = (
            datos.get("nombre_obra", [""])[0],
            datos.get("direccion", [""])[0],
            ",".join(request.form.getlist("tramites")),
            datos.get("tipo_uso", [""])[0],
            datos.get("dictamen_comercial_texto", [""])[0],
            datos.get("dictamen_industrial_texto", [""])[0],
            datos.get("licencia", [""])[0],
            datos.get("clave_catastral", [""])[0],
            datos.get("propietario_nombre", [""])[0],
            datos.get("propietario_direccion", [""])[0],
            datos.get("propietario_rfc", [""])[0],
            datos.get("dro_nombre", [""])[0],
            datos.get("dro_cedula", [""])[0],
            datos.get("dro_colegio", [""])[0],
            datos.get("dro_registro_colegio", [""])[0],
            datos.get("dro_registro_municipal", [""])[0],
            datos.get("estructura_nombre", [""])[0],
            datos.get("estructura_cedula", [""])[0],
            datos.get("estructura_colegio", [""])[0],
            datos.get("estructura_registro_colegio", [""])[0],
            datos.get("estructura_registro_municipal", [""])[0],
            datos.get("instalaciones_nombre", [""])[0],
            datos.get("instalaciones_cedula", [""])[0],
            datos.get("instalaciones_colegio", [""])[0],
            datos.get("instalaciones_registro_colegio", [""])[0],
            datos.get("instalaciones_registro_municipal", [""])[0],
            datos.get("diseno_nombre", [""])[0],
            datos.get("diseno_cedula", [""])[0],
            datos.get("diseno_colegio", [""])[0],
            datos.get("diseno_registro_colegio", [""])[0],
            datos.get("diseno_registro_municipal", [""])[0],
            datos.get("gas_nombre", [""])[0],
            datos.get("gas_cedula", [""])[0],
            datos.get("gas_colegio", [""])[0],
            datos.get("gas_registro_colegio", [""])[0],
            datos.get("gas_registro_municipal", [""])[0],
            datos.get("fecha_inicio", [""])[0],
            datos.get("fecha_termino", [""])[0],
            datos.get("numero_contrato", [""])[0],
            id  # El ID para la cláusula WHERE
        )
        print(f"valores {valores}")
        cursor.execute(sql, valores)
        conexion.connection.commit()
        cursor.close()
        return redirect(url_for('formulario')) # Redirigir a la página principal o a una lista de registros
    except Exception as e:
        return f"Error al actualizar el registro: {str(e)}"

# @app.route('/guardar', methods=['POST'])
# def guardar():
#     datos = request.form.to_dict(flat=False)
#     registro_json = {}
#     print("Datos recibidos:")
#     for clave, valor in datos.items():
#         #print(f"{clave}: {valor}")
#         registro_json[clave] = request.form[clave]
#     #return "Datos recibidos correctamente"
#     return jsonify(registro_json)

if __name__ == '__main__':
    app.run(debug=True)

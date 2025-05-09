from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)

# Configuración de conexión a MySQL
#Conexion MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pampi2012$'
app.config['MYSQL_DB'] = 'bitacora_obra'

conexion = MySQL(app)


@app.route('/')
def formulario():
    return render_template('formulario_bitacora.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.form.to_dict(flat=False)

    try:
        cursor = conexion.connection.cursor()

        sql = """
            INSERT INTO obras (
                id_obra, nombre_obra, direccion, tramites, tipo_uso,
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
            datos.get("id_obra", [""])[0],
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
        return "Datos guardados correctamente"
    except Exception as e:
        return f"Error al guardar: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

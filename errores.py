from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pampi2012$'
app.config['MYSQL_DB'] = 'bitacora_obra'

mysql = MySQL(app)

@app.route('/')
def formulario():
    data = {
        'tipos_tramite': 'bla bla'
    }
    return render_template('errores.html')
    #formulario_bitacora_accordion



@app.route('/submit', methods=['POST'])
def submit():
    print("si entra")
    try:
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO curso (idcurso, cursocol, instructor) VALUES (%s, %s, %s)"
        valores = (4, 'Ingles', 'John Wick')
        cursor.execute(sql, valores)
        mysql.connection.commit()
        cursor.close()
        return "Datos del curso insertados correctamente en la tabla 'curso'."
    except Exception as e:
        return f"Error al insertar datos: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
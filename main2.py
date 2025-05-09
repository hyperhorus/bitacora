from flask import Flask, render_template_string, request

app = Flask(__name__)

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
    (12, 'Suspencion temporal de obra'),
    (13, 'Cambio de propietario'),
    (14, 'Cambio del/de la D.R.O.'),
    (15, 'Obras menores'),
    (16, 'Cambio de proyecto'),
    (17, 'Invasion de la via publica'),
    (18, 'Validacion'),
    (19, 'Integral 1: Licencia (regularizacion) y Terminacion de Obra')
]

HTML_FORM = """
<h2>Selecciona los tipos de trámite</h2>
<form method="post">
  <div class="checkbox-grid">
    {% for id, texto in tipos %}
      <label><input type="checkbox" name="tramites" value="{{ id }}"> {{ texto }}</label>
    {% endfor %}
  </div>
  <br>
  <button type="submit">Guardar</button>
</form>

{% if seleccionados %}
  <h3>Trámites seleccionados:</h3>
  <ul>
    {% for t in seleccionados %}
      <li>{{ t }}</li>
    {% endfor %}
  </ul>
{% endif %}
<style>
  .checkbox-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 16px;
    max-width: 600px;
  }
</style>
"""


@app.route('/', methods=['GET', 'POST'])
def formulario():
    seleccionados = []
    if request.method == 'POST':
        ids_seleccionados = request.form.getlist('tramites')
        seleccionados = [texto for (id, texto) in TIPOS_TRAMITE if str(id) in ids_seleccionados]
        print(seleccionados)
    return render_template_string(HTML_FORM, tipos=TIPOS_TRAMITE, seleccionados=seleccionados)

if __name__ == '__main__':
    app.run(debug=True)

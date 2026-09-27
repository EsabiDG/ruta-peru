"""
app.py
Servidor Flask de RUTA PERÚ.
"""

from flask import Flask, render_template, request
from sistema_experto import (
    recomendar, verificar_base_hechos,
    obtener_imagen_destino, obtener_descripcion_destino, base_hechos,
)

app = Flask(__name__)
verificar_base_hechos()


@app.route("/")
def index():
    destinos = []
    for nombre in base_hechos.keys():
        destinos.append({
            "nombre": nombre,
            "descripcion": obtener_descripcion_destino(nombre),
            "imagen": obtener_imagen_destino(nombre),
        })
    return render_template("index.html", destinos=destinos)


@app.route("/recomendar", methods=["POST"])
def procesar_recomendacion():
    intereses = request.form.getlist("intereses")
    resultado = recomendar(set(intereses))
    if resultado["encontrado"]:
        destino = resultado["recomendacion"]
        resultado["imagen"] = obtener_imagen_destino(destino)
        resultado["descripcion"] = obtener_descripcion_destino(destino)
    return render_template("resultado.html", resultado=resultado, intereses=intereses)


if __name__ == "__main__":
    app.run(debug=True)
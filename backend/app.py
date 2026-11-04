from flask import Flask, jsonify
from flask_cors import CORS
from servicio import AlumnoServicio

app = Flask(__name__)
CORS(app)
servicio = AlumnoServicio()

@app.route("/api/alumnos", methods=["GET"])
def listar_alumnos():

    try:
        alumnos = (servicio.listar_alumnos())
        return jsonify(alumnos), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/api/dashboard/facultades", methods=["GET"])
def alumnos_por_facultad():
    try:
        datos = (servicio.obtener_alumnos_por_facultad())
        return jsonify(datos), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/api/dashboard/estado-academico", methods=["GET"])
def estado_academico():
    try:
        datos = (servicio.obtener_estado_academico())
        return jsonify(datos), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
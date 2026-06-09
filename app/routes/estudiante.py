from flask import Blueprint, jsonify
from app.models import Estudiante

estudiante_bp = Blueprint('estudiante', __name__)

@estudiante_bp.route('/estudiantes', methods=['GET'])
def listar_estudiantes():

    estudiantes = Estudiante.query.all()

    resultado = []

    for e in estudiantes:
        resultado.append({
            "id": e.id_estudiante,
            "matricula": e.matricula,
            "nombre": e.nombre,
            "apellido": e.apellido,
            "ci": e.ci,
            "correo": e.correo
        })

    return jsonify(resultado)
#practica.py
from flask import Blueprint, jsonify
from app.models import Practica
from flask import render_template

practica_bp = Blueprint('practica', __name__)

@practica_bp.route('/practicas')
def ver_practicas():

    practicas = Practica.query.all()

    return render_template(
        'practicas.html',
        practicas=practicas
    )

@practica_bp.route('/api/practicas', methods=['GET'])
def listar_practicas():

    practicas = Practica.query.all()

    resultado = []

    for p in practicas:

        porcentaje = 0

        if p.horas_requeridas:
            porcentaje = (
                p.horas_completadas /
                p.horas_requeridas
            ) * 100

        resultado.append({
            "id": p.id_practica,
            "estudiante":
                f"{p.estudiante.nombre} {p.estudiante.apellido}",
            "estado": p.estado,
            "avance": round(porcentaje, 2)
        })

    return jsonify(resultado)
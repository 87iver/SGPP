from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required

from app.models import Practica  # 🔥 IMPORTANTE

practica_inf_general_bp = Blueprint(
    'practica_inf_general',
    __name__
)


@practica_inf_general_bp.route('/practicas-general')
def ver_practicas():
    return render_template('practicas.html')


@practica_inf_general_bp.route('/api/practicas', methods=['GET'])
@jwt_required()
def listar_practicas():

    practicas = Practica.query.all()

    resultado = []

    for p in practicas:

        porcentaje = 0
        if p.horas_requeridas:
            porcentaje = (p.horas_completadas / p.horas_requeridas) * 100

        resultado.append({
            "id": p.id_practica,
            "estudiante": f"{p.estudiante.nombre} {p.estudiante.apellido}",
            "estado": p.estado,
            "avance": round(porcentaje, 2)
        })

    return jsonify(resultado)
from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required
from app.database import get_connection

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

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.id_practica,
            p.estado,
            p.horas_requeridas,
            p.horas_completadas,
            e.nombre,
            e.apellido
        FROM practica p
        JOIN estudiante e ON p.id_estudiante = e.id_estudiante
    """

    cursor.execute(query)
    practicas = cursor.fetchall()

    resultado = []

    for p in practicas:

        porcentaje = 0
        if p["horas_requeridas"]:
            porcentaje = (p["horas_completadas"] / p["horas_requeridas"]) * 100

        resultado.append({
            "id": p["id_practica"],
            "estudiante": f"{p['nombre']} {p['apellido']}",
            "estado": p["estado"],
            "avance": round(porcentaje, 2)
        })

    cursor.close()
    conn.close()

    return jsonify(resultado)
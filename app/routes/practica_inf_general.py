#practica.py
from flask import Blueprint, jsonify, render_template
from app.database import get_connection

practica_inf_general_bp = Blueprint(
    'practica_inf_general',
    __name__
)

@practica_inf_general_bp.route('/practicas-general')
def ver_practicas():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM practica")
            practicas = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        'practicas.html',
        practicas=practicas
    )

@practica_inf_general_bp.route('/api/practicas', methods=['GET'])
def listar_practicas():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.id_practica, p.estado, p.horas_requeridas, p.horas_completadas,
                    e.nombre, e.apellido
                FROM practica p
                JOIN estudiante e ON p.id_estudiante = e.id_estudiante
            """)
            practicas = cursor.fetchall()

        resultado = []
        for p in practicas:
            porcentaje = 0
            if p.get('horas_requeridas') and p['horas_requeridas'] > 0:
                porcentaje = (p['horas_completadas'] / p['horas_requeridas']) * 100

            resultado.append({
                "id": p['id_practica'],
                "estudiante": f"{p['nombre']} {p['apellido']}",
                "estado": p['estado'],
                "avance": round(porcentaje, 2)
            })
    finally:
        conn.close()

    return jsonify(resultado)
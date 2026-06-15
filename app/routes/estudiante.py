# app/routes/estudiante.py

from flask import Blueprint, jsonify
from app.database import get_connection

estudiante_bp = Blueprint('estudiante', __name__)

@estudiante_bp.route('/estudiantes', methods=['GET'])
def listar_estudiantes():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_estudiante, matricula, nombre, apellido, ci, correo
                FROM estudiante
            """)
            estudiantes = cursor.fetchall()
    finally:
        conn.close()

    return jsonify(estudiantes)
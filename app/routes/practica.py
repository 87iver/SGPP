# app/routes/practica.py

from flask import Blueprint, request, jsonify, render_template, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import get_connection
from datetime import datetime

practica_bp = Blueprint('practica', __name__)


def _is_admin():
    identity = get_jwt_identity() or {}
    return (identity.get('rol') if isinstance(identity, dict) else None) == 'Administrador'


@practica_bp.route('/practicas', methods=['POST'])
@jwt_required()
def registrar_practica():
    if not _is_admin():
        return jsonify({"mensaje": "No autorizado"}), 403

    datos = request.get_json()

    fecha_inicio = datetime.strptime(datos['fecha_inicio'], '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(datos['fecha_fin'], '%Y-%m-%d').date() if datos.get('fecha_fin') else None

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO practica (
                    id_estudiante, id_institucion, fecha_inicio, fecha_fin,
                    estado, modalidad, remuneracion, tipo_practica,
                    horas_requeridas, horas_completadas, area_trabajo, descripcion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                datos['id_estudiante'], datos['id_institucion'],
                fecha_inicio, fecha_fin,
                datos['estado'], datos['modalidad'], datos['remuneracion'],
                datos['tipo_practica'], datos['horas_requeridas'],
                datos['horas_completadas'], datos['area_trabajo'], datos['descripcion']
            ))
        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensaje": "Práctica registrada correctamente"}), 201


@practica_bp.route('/practicas', methods=['GET'])
def listar_practicas():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_practica, id_estudiante, id_institucion,
                       estado, modalidad, tipo_practica, horas_completadas
                FROM practica
            """)
            practicas = cursor.fetchall()
    finally:
        conn.close()

    return jsonify(practicas)

@practica_bp.route('/informacion_practicas')
def vista_practicas():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.id_practica,
                    p.fecha_inicio,
                    p.fecha_fin,
                    p.estado,
                    p.modalidad,
                    p.remuneracion,
                    p.tipo_practica,
                    p.horas_requeridas,
                    p.horas_completadas,
                    p.area_trabajo,
                    p.descripcion,
                    e.nombre AS estudiante_nombre,
                    e.apellido AS estudiante_apellido,
                    i.nombre AS institucion_nombre
                FROM practica p
                JOIN estudiante e ON p.id_estudiante = e.id_estudiante
                JOIN institucion i ON p.id_institucion = i.id_institucion
            """)
            practicas = cursor.fetchall()
    finally:
        conn.close()

    return render_template('informacion_practicas.html', practicas=practicas)


@practica_bp.route('/registrar-practica')
def formulario_registrar_practica():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_estudiante, nombre, apellido FROM estudiante")
            estudiantes = cursor.fetchall()

            cursor.execute("SELECT id_institucion, nombre FROM institucion")
            instituciones = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        'registrar_practica.html',
        estudiantes=estudiantes,
        instituciones=instituciones
    )


@practica_bp.route('/practicas/<int:id_practica>', methods=['GET'])
def obtener_practica(id_practica):

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM practica WHERE id_practica = %s", (id_practica,))
            practica = cursor.fetchone()
    finally:
        conn.close()

    if not practica:
        abort(404)

    practica['fecha_inicio'] = practica['fecha_inicio'].strftime('%Y-%m-%d')
    practica['fecha_fin'] = practica['fecha_fin'].strftime('%Y-%m-%d') if practica['fecha_fin'] else None

    return jsonify(practica)


@practica_bp.route('/practicas/<int:id_practica>', methods=['PUT'])
@jwt_required()
def editar_practica(id_practica):
    if not _is_admin():
        return jsonify({"mensaje": "No autorizado"}), 403

    conn = get_connection()
    try:
        with conn.cursor() as cursor:

            cursor.execute("SELECT id_practica FROM practica WHERE id_practica = %s", (id_practica,))
            if not cursor.fetchone():
                abort(404)

            datos = request.get_json()
            fecha_inicio = datetime.strptime(datos['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(datos['fecha_fin'], '%Y-%m-%d').date() if datos.get('fecha_fin') else None

            cursor.execute("""
                UPDATE practica SET
                    id_estudiante = %s, id_institucion = %s,
                    fecha_inicio = %s, fecha_fin = %s,
                    estado = %s, modalidad = %s, remuneracion = %s,
                    tipo_practica = %s, horas_requeridas = %s,
                    horas_completadas = %s, area_trabajo = %s, descripcion = %s
                WHERE id_practica = %s
            """, (
                datos['id_estudiante'], datos['id_institucion'],
                fecha_inicio, fecha_fin,
                datos['estado'], datos['modalidad'], datos['remuneracion'],
                datos['tipo_practica'], datos['horas_requeridas'],
                datos['horas_completadas'], datos['area_trabajo'],
                datos['descripcion'], id_practica
            ))
        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensaje": "Práctica actualizada correctamente"})


@practica_bp.route('/editar-practica/<int:id_practica>')
@jwt_required()
def formulario_editar_practica(id_practica):
    if not _is_admin():
        abort(403)

    conn = get_connection()
    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT p.*, 
                       e.nombre AS estudiante_nombre,
                       e.apellido AS estudiante_apellido,
                       i.nombre AS institucion_nombre
                FROM practica p
                JOIN estudiante e ON p.id_estudiante = e.id_estudiante
                JOIN institucion i ON p.id_institucion = i.id_institucion
                WHERE p.id_practica = %s
            """, (id_practica,))
            practica = cursor.fetchone()
            if not practica:
                abort(404)

            cursor.execute("SELECT id_estudiante, nombre, apellido FROM estudiante")
            estudiantes = cursor.fetchall()

            cursor.execute("SELECT id_institucion, nombre FROM institucion")
            instituciones = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        'editar_practica.html',
        practica=practica,
        estudiantes=estudiantes,
        instituciones=instituciones
    )


@practica_bp.route('/practicas/<int:id_practica>', methods=['DELETE'])
@jwt_required()
def eliminar_practica(id_practica):
    if not _is_admin():
        return jsonify({"mensaje": "No autorizado"}), 403

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_practica FROM practica WHERE id_practica = %s", (id_practica,))
            if not cursor.fetchone():
                abort(404)

            # Primero eliminar registros relacionados
            cursor.execute("DELETE FROM seguimiento WHERE id_practica = %s", (id_practica,))

            # Luego eliminar la práctica
            cursor.execute("DELETE FROM practica WHERE id_practica = %s", (id_practica,))

        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensaje": "Práctica eliminada correctamente"})

@practica_bp.route('/api/dashboard')
def dashboard_stats():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT COUNT(*) as total FROM practica")
            total_practicas = cursor.fetchone()['total']

            
            cursor.execute("SELECT COUNT(*) as total FROM estudiante")
            total_estudiantes = cursor.fetchone()['total']

            
            cursor.execute("SELECT COUNT(*) as total FROM institucion")
            total_instituciones = cursor.fetchone()['total']

            
            cursor.execute("""
                SELECT estado, COUNT(*) as cantidad 
                FROM practica 
                GROUP BY estado
            """)
            practicas_por_estado = cursor.fetchall()

            
            cursor.execute("""
                SELECT modalidad, COUNT(*) as cantidad 
                FROM practica 
                GROUP BY modalidad
            """)
            practicas_por_modalidad = cursor.fetchall()

            
            cursor.execute("""
                SELECT i.nombre, COUNT(p.id_practica) as cantidad
                FROM institucion i
                LEFT JOIN practica p ON i.id_institucion = p.id_institucion
                GROUP BY i.id_institucion, i.nombre
                ORDER BY cantidad DESC
                LIMIT 5
            """)
            top_instituciones = cursor.fetchall()

            
            cursor.execute("""
                SELECT 
                    ROUND(AVG(horas_completadas), 2) as promedio_completadas,
                    ROUND(AVG(horas_requeridas), 2) as promedio_requeridas
                FROM practica
            """)
            horas_promedio = cursor.fetchone()

            
            cursor.execute("""
                SELECT COUNT(*) as total 
                FROM practica 
                WHERE estado IN ('Activo', 'En Proceso', 'Pendiente')
            """)
            practicas_activas = cursor.fetchone()['total']

    finally:
        conn.close()

    return jsonify({
        'total_practicas': total_practicas,
        'total_estudiantes': total_estudiantes,
        'total_instituciones': total_instituciones,
        'practicas_activas': practicas_activas,
        'practicas_por_estado': practicas_por_estado,
        'practicas_por_modalidad': practicas_por_modalidad,
        'top_instituciones': top_instituciones,
        'horas_promedio': horas_promedio
    })

@practica_bp.route('/estado_practicas')
def estado_practicas():

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT
        p.id_practica,
        CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
        i.nombre AS institucion,
        p.fecha_inicio,
        p.fecha_fin,
        p.estado,
        p.modalidad,
        p.horas_completadas,
        p.horas_requeridas
    FROM practica p
    INNER JOIN estudiante e
        ON p.id_estudiante = e.id_estudiante
    INNER JOIN institucion i
        ON p.id_institucion = i.id_institucion
    ORDER BY p.id_practica DESC
    """

    cursor.execute(sql)
    practicas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'estado_practicas.html',
        practicas=practicas
    )
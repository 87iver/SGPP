# app/routes/practica.py

from flask import Blueprint, request, jsonify, render_template, abort
from app.database import get_connection
from datetime import datetime

practica_bp = Blueprint('practica', __name__)


@practica_bp.route('/practicas', methods=['POST'])
def registrar_practica():

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
def editar_practica(id_practica):

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
def formulario_editar_practica(id_practica):

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
def eliminar_practica(id_practica):

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
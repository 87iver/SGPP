#seguimineto.py
from flask import Blueprint, request, jsonify, render_template, redirect, abort
from datetime import datetime
from app.database import get_connection

seguimiento_bp = Blueprint(
    'seguimiento',
    __name__
)


@seguimiento_bp.route('/seguimientos')
def formulario():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM seguimiento")
            seguimientos = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        'seguimiento/index.html',
        seguimientos=seguimientos
    )


@seguimiento_bp.route('/registrar-seguimiento')
def formulario_registrar_practica():

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.id_practica,
                    p.fecha_inicio,
                    p.fecha_fin,
                    p.estado,
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

    return render_template(
        'seguimiento/registrar_seguimiento.html',
        practicas=practicas
    )



@seguimiento_bp.route('/seguimiento/<int:id_seguimiento>', methods=['GET'])
def obtener_seguimiento(id_seguimiento):

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM seguimiento WHERE id_seguimiento = %s", (id_seguimiento,))
            seguimiento = cursor.fetchone()
    finally:
        conn.close()

    if not seguimiento:
        abort(404)

    
    return jsonify(seguimiento)


@seguimiento_bp.route('/editar-seguimiento/<int:id_seguimiento>')
def formulario_editar_seguimiento(id_seguimiento):

    conn = get_connection()
    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT 
                    s.*, 
                    e.nombre AS estudiante_nombre,
                    e.apellido AS estudiante_apellido,
                    i.nombre AS institucion_nombre
                FROM seguimiento s
                JOIN practica p ON s.id_practica = p.id_practica
                JOIN estudiante e ON p.id_estudiante = e.id_estudiante
                JOIN institucion i ON p.id_institucion = i.id_institucion
                WHERE s.id_seguimiento = %s
            """, (id_seguimiento,))
            seguimiento = cursor.fetchone()
            if not seguimiento:
                abort(404)

            # Formateamos la fecha para que sea compatible con el input type="date"
            if seguimiento.get('fecha'):
                seguimiento['fecha'] = seguimiento['fecha'].strftime('%Y-%m-%d')

            cursor.execute("""
                SELECT 
                    p.id_practica, 
                    p.fecha_inicio, 
                    p.fecha_fin, 
                    p.estado,
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

    return render_template(
        'seguimiento/editar_seguimiento.html',
        seguimiento=seguimiento,
        practicas=practicas
    )












# POST
@seguimiento_bp.route(
    '/seguimiento',
    methods=['POST']
)
def registrar_avance():

    datos = request.get_json()
    fecha = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO seguimiento (id_practica, fecha, observacion, porcentaje_avance, horas_registradas)
                VALUES (%s, %s, %s, %s, %s)
            """, (datos['id_practica'], fecha, datos['observacion'], datos['porcentaje_avance'], datos['horas_registradas']))
        conn.commit()
    finally:
        conn.close()

    return jsonify({"mensaje": "Seguimiento registrado correctamente"})


# PUT
@seguimiento_bp.route(
    '/seguimiento/<int:id_seguimiento>',
    methods=['PUT']
)
def actualizar_seguimiento(id_seguimiento):

    datos = request.get_json()
    # Convertimos la fecha recibida en string a objeto date
    fecha = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_seguimiento FROM seguimiento WHERE id_seguimiento = %s", (id_seguimiento,))
            if not cursor.fetchone():
                return jsonify({"mensaje": "Seguimiento no encontrado"}), 404

            cursor.execute("""
                UPDATE seguimiento 
                SET id_practica = %s, fecha = %s, observacion = %s, 
                    porcentaje_avance = %s, horas_registradas = %s
                WHERE id_seguimiento = %s
            """, (
                datos["id_practica"], fecha, datos["observacion"], 
                datos["porcentaje_avance"], datos["horas_registradas"], id_seguimiento
            ))
        conn.commit()
    finally:
        conn.close()

    return jsonify({
        "mensaje": "Actualizado"
    })


# DELETE
@seguimiento_bp.route(
    '/seguimiento/<int:id_seguimiento>',
    methods=['DELETE']
)
def eliminar_seguimiento(id_seguimiento):

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM seguimiento WHERE id_seguimiento = %s", (id_seguimiento,))
            if cursor.rowcount == 0:
                return jsonify({"mensaje": "Seguimiento no encontrado"}), 404
        conn.commit()
    finally:
        conn.close()

    return jsonify({
        "mensaje": "Eliminado"
    })

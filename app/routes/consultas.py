from flask import Blueprint, render_template
from app.database import get_connection

consultas_bp = Blueprint(
    'consultas',
    __name__,
    url_prefix='/consultas'
)

@consultas_bp.route('/')
def index():
    return render_template('consultas/index.html')


@consultas_bp.route('/horas_incompletas')
def horas_incompletas():

    conexion = get_connection()

    cursor = conexion.cursor()

    sql = """
        SELECT
            e.nombre,
            e.apellido,
            i.nombre AS institucion,
            p.horas_requeridas,
            p.horas_completadas,
            (p.horas_requeridas - p.horas_completadas) AS pendientes
        FROM practica p
        INNER JOIN estudiante e
            ON p.id_estudiante = e.id_estudiante
        INNER JOIN institucion i
            ON p.id_institucion = i.id_institucion
        WHERE p.horas_completadas < p.horas_requeridas
    """

    cursor.execute(sql)

    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'consultas/horas_incompletas.html',
        datos=datos
    )

@consultas_bp.route('/practicas_por_institucion')
def practicas_por_institucion():

    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        SELECT
            i.nombre AS institucion,
            COUNT(p.id_practica) AS total_practicas
        FROM practica p
        INNER JOIN institucion i
            ON p.id_institucion = i.id_institucion
        GROUP BY i.id_institucion, i.nombre
        ORDER BY total_practicas DESC
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'consultas/practicas_por_institucion.html',
        datos=datos
    )

@consultas_bp.route('/estudiantes_por_carrera')
def estudiantes_por_carrera():

    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        SELECT
            carrera,
            COUNT(*) AS total_estudiantes
        FROM estudiante
        GROUP BY carrera
        ORDER BY total_estudiantes DESC
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'consultas/estudiantes_por_carrera.html',
        datos=datos
    )

@consultas_bp.route('/practicas_por_estado')
def practicas_por_estado():

    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        SELECT
            estado,
            COUNT(*) AS total
        FROM practica
        GROUP BY estado
        ORDER BY total DESC
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'consultas/practicas_por_estado.html',
        datos=datos
    )

@consultas_bp.route('/practicas_por_modalidad')
def practicas_por_modalidad():

    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        SELECT
            modalidad,
            COUNT(*) AS total
        FROM practica
        GROUP BY modalidad
        ORDER BY total DESC
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'consultas/practicas_por_modalidad.html',
        datos=datos
    )

@consultas_bp.route('/practicas_por_remuneracion')
def practicas_por_remuneracion():

    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
        SELECT
            remuneracion,
            COUNT(*) AS total
        FROM practica
        GROUP BY remuneracion
        ORDER BY total DESC
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'consultas/practicas_por_remuneracion.html',
        datos=datos
    )
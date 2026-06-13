from flask import Blueprint, request, jsonify
from app import db
from app.models import Practica
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template 

practica_bp = Blueprint('practica', __name__)

@practica_bp.route('/practicas', methods=['POST'])
def registrar_practica():

    datos = request.get_json()

    practica = Practica(
        id_estudiante=datos['id_estudiante'],
        id_institucion=datos['id_institucion'],
        fecha_inicio=datetime.strptime(
            datos['fecha_inicio'],
            '%Y-%m-%d'
        ).date(),
        fecha_fin=datetime.strptime(
            datos['fecha_fin'],
            '%Y-%m-%d'
        ).date() if datos.get('fecha_fin') else None,

        estado=datos['estado'],
        modalidad=datos['modalidad'],
        remuneracion=datos['remuneracion'],
        tipo_practica=datos['tipo_practica'],
        horas_requeridas=datos['horas_requeridas'],
        horas_completadas=datos['horas_completadas'],
        area_trabajo=datos['area_trabajo'],
        descripcion=datos['descripcion']
    )

    db.session.add(practica)
    db.session.commit()

    return jsonify({
        "mensaje": "Práctica registrada correctamente"
    }), 201

@practica_bp.route('/practicas', methods=['GET'])
def listar_practicas():

    practicas = Practica.query.all()

    resultado = []

    for p in practicas:
        resultado.append({
            "id_practica": p.id_practica,
            "id_estudiante": p.id_estudiante,
            "id_institucion": p.id_institucion,
            "estado": p.estado,
            "modalidad": p.modalidad,
            "tipo_practica": p.tipo_practica,
            "horas_completadas": p.horas_completadas
        })

    return jsonify(resultado)

@practica_bp.route('/informacion_practicas')
def vista_practicas():

    practicas = Practica.query.all()

    return render_template(
        'informacion_practicas.html',
        practicas=practicas
    )

@practica_bp.route('/registrar-practica')
def formulario_practica():
    return render_template('registrar_practica.html')
#seguimineto.py
from flask import Blueprint, request, jsonify, render_template, redirect
from datetime import datetime
from app import db
from app.models import Seguimiento
from flask_jwt_extended import jwt_required

seguimiento_bp = Blueprint(
    'seguimiento',
    __name__
)


@seguimiento_bp.route('/seguimiento-form')
def formulario():

    seguimientos = Seguimiento.query.all()

    return render_template(
        'seguimiento.html',
        seguimientos=seguimientos
    )


# GET TODOS
@seguimiento_bp.route('/seguimiento', methods=['GET'])
def listar_seguimientos():

    seguimientos = Seguimiento.query.all()

    resultado = []

    for s in seguimientos:

        resultado.append({
            "id": s.id_seguimiento,
            "practica": s.id_practica,
            "fecha": str(s.fecha),
            "observacion": s.observacion,
            "avance": s.porcentaje_avance,
            "horas": s.horas_registradas
        })

    return jsonify(resultado)


# GET UNO
@seguimiento_bp.route(
    '/seguimiento/<int:id>',
    methods=['GET']
)
def obtener_seguimiento(id):

    seguimiento = Seguimiento.query.get(id)

    if not seguimiento:
        return jsonify({
            "error": "No encontrado"
        }), 404

    return jsonify({
        "id": seguimiento.id_seguimiento,
        "practica": seguimiento.id_practica,
        "fecha": str(seguimiento.fecha),
        "observacion": seguimiento.observacion,
        "avance": seguimiento.porcentaje_avance,
        "horas": seguimiento.horas_registradas
    })


# POST
@seguimiento_bp.route(
    '/seguimiento',
    methods=['POST']
)
def registrar_avance():

    datos = request.form

    nuevo = Seguimiento(
        id_practica=datos['id_practica'],
        fecha=datetime.strptime(
            datos['fecha'],
            '%Y-%m-%d'
        ).date(),
        observacion=datos['observacion'],
        porcentaje_avance=datos['porcentaje_avance'],
        horas_registradas=datos['horas_registradas']
    )

    db.session.add(nuevo)
    db.session.commit()

    return redirect('/seguimiento-form')


# PUT
@seguimiento_bp.route(
    '/seguimiento/<int:id>',
    methods=['PUT']
)
@jwt_required()
def actualizar_seguimiento(id):

    datos = request.get_json()

    seguimiento = Seguimiento.query.get(id)

    if not seguimiento:
        return jsonify({
            "error": "No encontrado"
        }), 404

    seguimiento.observacion = datos["observacion"]
    seguimiento.porcentaje_avance = datos["porcentaje_avance"]
    seguimiento.horas_registradas = datos["horas_registradas"]

    db.session.commit()

    return jsonify({
        "mensaje": "Actualizado"
    })


# DELETE
@seguimiento_bp.route(
    '/seguimiento/<int:id>',
    methods=['DELETE']
)
@jwt_required()
def eliminar_seguimiento(id):

    seguimiento = Seguimiento.query.get(id)

    if not seguimiento:
        return jsonify({
            "error": "No encontrado"
        }), 404

    db.session.delete(seguimiento)
    db.session.commit()

    return jsonify({
        "mensaje": "Eliminado"
    })


# ELIMINAR DESDE INTERFAZ
@seguimiento_bp.route(
    '/seguimiento/eliminar/<int:id>'
)
def eliminar_web(id):

    seguimiento = Seguimiento.query.get(id)

    if seguimiento:

        db.session.delete(seguimiento)
        db.session.commit()

    return redirect('/seguimiento-form')
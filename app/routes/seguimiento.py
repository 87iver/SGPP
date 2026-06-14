#seguimineto.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Seguimiento
from flask import render_template

seguimiento_bp = Blueprint(
    'seguimiento',
    __name__
)

@seguimiento_bp.route('/seguimiento-form')
def formulario():

    return render_template(
        'seguimiento.html'
    )

@seguimiento_bp.route(
    '/seguimiento',
    methods=['POST']
)
def registrar_avance():

    datos = request.get_json()

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

    return jsonify({
        "mensaje":
        "Seguimiento registrado correctamente"
    })
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

auth_bp = Blueprint('auth', __name__)

# PERFIL
@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    user = get_jwt_identity()
    return jsonify({"user": user})

# LOGIN PAGE
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# LOGIN REAL
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    # Validación temporal sin base de datos
    valid_users = {
        'admin': '1234',
        'usuario': '1234'
    }

    if valid_users.get(username) == password:
        rol = 'Administrador' if username == 'admin' else 'Usuario'
        token = create_access_token(identity={"username": username, "rol": rol})
        return jsonify({"access_token": token, "token": token, "msg": "Inicio de sesión correcto"}), 200

    return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401
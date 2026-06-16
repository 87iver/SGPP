from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.database import get_connection
import hashlib

auth_bp = Blueprint('auth', __name__)




@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuario WHERE username=%s",
        (username,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({"msg": "Usuario no existe"}), 404

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if password_hash != user["password_hash"]:
        return jsonify({"msg": "Contraseña incorrecta"}), 401

    token = create_access_token(identity={
        "id": user["id_usuario"],
        "username": user["username"],
        "rol": user["rol"]
    })
    return jsonify({"token": token})
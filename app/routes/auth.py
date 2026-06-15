#auth.py
from flask import Blueprint, render_template
from flask_jwt_extended import (create_access_token)
from flask_jwt_extended import (jwt_required)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route(
    '/api/login',
    methods=['POST']
)
def api_login():

    token = create_access_token(
        identity="admin"
    )

    return {
        "token": token
    }


# app/__init__.py

from flask import Flask, render_template
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'sgpp-secret'

    jwt.init_app(app)

    @app.route('/')
    def home():
        return render_template('index.html')

    from app.routes.estudiante import estudiante_bp
    app.register_blueprint(estudiante_bp)

    from app.routes.practica import practica_bp
    app.register_blueprint(practica_bp)

    from app.routes.consultas import consultas_bp
    app.register_blueprint(consultas_bp)

    return app
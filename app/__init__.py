from flask import Flask, app, render_template
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # cambia esto
    jwt = JWTManager(app)
    
    # Ruta principal (login)
    @app.route('/')
    def home():
        return render_template('login.html')

    # Dashboard separado (mejor práctica)
    @app.route('/dashboard')
    def dashboard():
        return render_template('index.html')

    # ==========================
    # BLUEPRINTS
    # ==========================

    from app.routes.estudiante import estudiante_bp
    app.register_blueprint(estudiante_bp)

    from app.routes.practica import practica_bp
    app.register_blueprint(practica_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.practica_inf_general import practica_inf_general_bp
    app.register_blueprint(practica_inf_general_bp)

    from app.routes.seguimiento import seguimiento_bp
    app.register_blueprint(seguimiento_bp)

    from app.routes.consultas import consultas_bp
    app.register_blueprint(consultas_bp)

    return app
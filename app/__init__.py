from flask import Flask, render_template
from flask_jwt_extended import JWTManager

from app.extensions import db, jwt


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secret'

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)

    # Crear tablas (opcional en desarrollo)
    with app.app_context():
        db.create_all()

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
#__init__.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sgpp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sgpp-secret'

    db.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def home():
        return render_template('index.html')

    from app.routes.auth import auth_bp
    from app.routes.estudiante import estudiante_bp
    from app.routes.practica import practica_bp
    from app.routes.seguimiento import seguimiento_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(estudiante_bp)
    app.register_blueprint(practica_bp)
    app.register_blueprint(seguimiento_bp)

    from app import models

    return app
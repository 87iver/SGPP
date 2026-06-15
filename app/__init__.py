# app/__init__.py

from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from app.database import get_connection

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'sgpp-secret'

    jwt.init_app(app)

    @app.route('/')
    def home():
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. Estadísticas de las tarjetas superiores
                cursor.execute("SELECT COUNT(*) as total FROM estudiante")
                total_estudiantes = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM practica")
                total_practicas = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM institucion")
                total_instituciones = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM practica WHERE estado = 'En Proceso'")
                total_practicas_activas = cursor.fetchone()['total']

                # 2. Datos para el gráfico de Dona (Prácticas por Estado)
                cursor.execute("SELECT estado, COUNT(*) as cantidad FROM practica GROUP BY estado")
                res_estados = cursor.fetchall()
                estados_labels = [r['estado'] for r in res_estados]
                estados_data = [r['cantidad'] for r in res_estados]

                # 3. Datos para el gráfico de Barras (Avance de Horas - Top 7)
                cursor.execute("""
                    SELECT e.nombre, p.horas_completadas, p.horas_requeridas 
                    FROM practica p 
                    JOIN estudiante e ON p.id_estudiante = e.id_estudiante 
                    ORDER BY p.id_practica DESC LIMIT 7
                """)
                res_avance = cursor.fetchall()
                avance_labels = [r['nombre'] for r in res_avance]
                avance_completadas = [r['horas_completadas'] for r in res_avance]
                avance_requeridas = [r['horas_requeridas'] for r in res_avance]

                # 4. Últimas prácticas registradas
                cursor.execute("""
                    SELECT p.*, e.nombre AS estudiante_nombre, e.apellido AS estudiante_apellido, i.nombre AS institucion_nombre 
                    FROM practica p 
                    JOIN estudiante e ON p.id_estudiante = e.id_estudiante 
                    JOIN institucion i ON p.id_institucion = i.id_institucion 
                    ORDER BY p.id_practica DESC LIMIT 5
                """)
                ultimas_practicas = cursor.fetchall()

                # 5. Últimos seguimientos registrados
                cursor.execute("""
                    SELECT s.*, e.nombre AS estudiante_nombre, e.apellido AS estudiante_apellido 
                    FROM seguimiento s 
                    JOIN practica p ON s.id_practica = p.id_practica 
                    JOIN estudiante e ON p.id_estudiante = e.id_estudiante 
                    ORDER BY s.id_seguimiento DESC LIMIT 5
                """)
                ultimos_seguimientos = cursor.fetchall()
        finally:
            conn.close()

        return render_template('index.html',
            total_estudiantes=total_estudiantes,
            total_practicas=total_practicas,
            total_instituciones=total_instituciones,
            total_practicas_activas=total_practicas_activas,
            estados_labels=estados_labels,
            estados_data=estados_data,
            avance_labels=avance_labels,
            avance_completadas=avance_completadas,
            avance_requeridas=avance_requeridas,
            ultimas_practicas=ultimas_practicas,
            ultimos_seguimientos=ultimos_seguimientos
        )


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

    # ==========================

    
    from app.routes.consultas import consultas_bp
    app.register_blueprint(consultas_bp)

    return app
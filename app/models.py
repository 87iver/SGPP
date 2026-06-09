from app import db

class Estudiante(db.Model):
    __tablename__ = 'estudiante'

    id_estudiante = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(30), unique=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    ci = db.Column(db.String(20), unique=True)
    correo = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    carrera = db.Column(db.String(100))
    mencion = db.Column(db.String(100))
    semestre = db.Column(db.Integer)
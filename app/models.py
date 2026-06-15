from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120))
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Administrador', 'Tutor'))
    fecha_registro = db.Column(db.DateTime)


class Estudiante(db.Model):
    __tablename__ = 'estudiante'

    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))


class Institucion(db.Model):
    __tablename__ = 'institucion'

    id_institucion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))


class Practica(db.Model):
    __tablename__ = "practica"

    id_practica = db.Column(db.Integer, primary_key=True)

    estado = db.Column(db.String(50))
    horas_requeridas = db.Column(db.Integer)
    horas_completadas = db.Column(db.Integer)

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiante.id_estudiante")
    )

    estudiante = db.relationship("Estudiante", backref="practicas")


class Seguimiento(db.Model):
    __tablename__ = "seguimiento"

    id_seguimiento = db.Column(db.Integer, primary_key=True)

    estado = db.Column(db.String(50))
    observacion = db.Column(db.String(255))

    estudiante_id = db.Column(
        db.Integer,
        db.ForeignKey("estudiante.id_estudiante")
    )
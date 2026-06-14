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


class Institucion(db.Model):
    __tablename__ = 'institucion'

    id_institucion = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(db.String(150))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))
    responsable = db.Column(db.String(100))

class Practica(db.Model):
    __tablename__ = 'practica'

    id_practica = db.Column(db.Integer, primary_key=True)

    id_estudiante = db.Column(
        db.Integer,
        db.ForeignKey('estudiante.id_estudiante')
    )

    id_institucion = db.Column(
        db.Integer,
        db.ForeignKey('institucion.id_institucion')
    )

    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    estado = db.Column(db.String(30))

    horas_requeridas = db.Column(db.Integer)
    horas_completadas = db.Column(db.Integer)

    estudiante = db.relationship(
        'Estudiante',
        backref='practicas'
    )

    institucion = db.relationship(
        'Institucion',
        backref='practicas'
    )

class Seguimiento(db.Model):

    __tablename__ = 'seguimiento'

    id_seguimiento = db.Column(
        db.Integer,
        primary_key=True
    )

    id_practica = db.Column(
        db.Integer,
        db.ForeignKey('practica.id_practica')
    )

    fecha = db.Column(db.Date)

    observacion = db.Column(db.Text)

    porcentaje_avance = db.Column(db.Float)

    horas_registradas = db.Column(db.Integer)

    practica = db.relationship(
        'Practica',
        backref='seguimientos'
    )
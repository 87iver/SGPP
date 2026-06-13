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

    id_institucion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))
    responsable = db.Column(db.String(100))
    sector = db.Column(db.String(20))
    descripcion = db.Column(db.Text)

class Practica(db.Model):
    __tablename__ = 'practica'

    id_practica = db.Column(db.Integer, primary_key=True)

    id_estudiante = db.Column(
        db.Integer,
        db.ForeignKey('estudiante.id_estudiante'),
        nullable=False
    )

    id_institucion = db.Column(
        db.Integer,
        db.ForeignKey('institucion.id_institucion'),
        nullable=False
    )

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)

    estado = db.Column(db.String(20), default='Pendiente')
    modalidad = db.Column(db.String(20))
    remuneracion = db.Column(db.String(20))
    tipo_practica = db.Column(db.String(30))

    horas_requeridas = db.Column(db.Integer, default=240)
    horas_completadas = db.Column(db.Integer, default=0)

    area_trabajo = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
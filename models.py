from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# ==========================
# USUARIOS
# ==========================

class Usuario(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    correo = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    contraseña = db.Column(
        db.String(200),
        nullable=False
    )

    curso = db.Column(
        db.String(50)
    )

    foto = db.Column(
        db.String(200),
        default="default.png"
    )

    administrador = db.Column(
        db.Boolean,
        default=False
    )

    rol = db.Column(
        db.String(50),
        default="Estudiante"
    )
    

    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relación con sugerencias
    sugerencias = db.relationship(
        "Sugerencia",
        backref="autor",
        lazy=True
    )

    # Relación con comentarios
    comentarios = db.relationship(
        "Comentario",
        backref="autor",
        lazy=True
    )


# ==========================
# SUGERENCIAS
# ==========================

class Sugerencia(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(200),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    categoria = db.Column(
        db.String(100)
    )

    imagen = db.Column(
        db.String(200)
    )

    estado = db.Column(
        db.String(50),
        default="Pendiente"
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    vistas = db.Column(
        db.Integer,
        default=0
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )
    

    # Relaciones
    comentarios = db.relationship(
        "Comentario",
        backref="sugerencia",
        lazy=True,
        cascade="all, delete"
    )

    apoyos = db.relationship(
        "Apoyo",
        backref="sugerencia",
        lazy=True,
        cascade="all, delete"
    )

    @property
    def cantidad_apoyos(self):
        return len(self.apoyos)



# ==========================
# APOYOS / VOTOS
# ==========================

class Apoyo(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id")
    )

    sugerencia_id = db.Column(
        db.Integer,
        db.ForeignKey("sugerencia.id")
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



# ==========================
# COMENTARIOS
# ==========================

class Comentario(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    contenido = db.Column(
        db.Text,
        nullable=False
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id")
    )

    sugerencia_id = db.Column(
        db.Integer,
        db.ForeignKey("sugerencia.id")
    )



# ==========================
# NOTICIAS
# ==========================

class Noticia(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    contenido = db.Column(
        db.Text,
        nullable=False
    )

    imagen = db.Column(
        db.String(200),
        default="noticia.png"
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )


    autor = db.relationship(
        "Usuario",
        backref="noticias"
    )



# ==========================
# EVENTOS
# ==========================

class Evento(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    titulo = db.Column(
        db.String(150),
        nullable=False
    )


    descripcion = db.Column(
        db.Text,
        nullable=False
    )


    fecha = db.Column(
        db.String(50),
        nullable=False
    )


    hora = db.Column(
        db.String(20),
        nullable=False
    )


    lugar = db.Column(
        db.String(100),
        nullable=False
    )


    creador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )



# ==========================
# NOTIFICACIONES
# ==========================

class Notificacion(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    mensaje = db.Column(
        db.String(300)
    )

    leida = db.Column(
        db.Boolean,
        default=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id")
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
import os

# Carpeta base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para sesiones y formularios
    SECRET_KEY = "CentroDeAlumnosPro2026"

    # Base de datos SQLite
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

    # Desactiva advertencias innecesarias
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Carpeta donde se subirán imágenes y archivos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    # Tamaño máximo de archivos (5 MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # Extensiones permitidas
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp",
        "pdf"
    }

    # Configuración de la aplicación
    APP_NAME = "Centro de Alumnos"

    POSTS_PER_PAGE = 10

    DEBUG = True
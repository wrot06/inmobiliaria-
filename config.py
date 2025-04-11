import os

class Config:
    SECRET_KEY = '@12345'  # Cambia a una clave secreta real
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'  # Cambia por tu base de datos real
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limitar el tamaño del archivo a 16 MB
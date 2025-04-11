from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar SQLAlchemy con la app
    db.init_app(app)

    # Registrar el blueprint
    from .routes import main
    app.register_blueprint(main)

    return app

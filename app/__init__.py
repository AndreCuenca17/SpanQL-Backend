from flask import Flask, g
from flask_cors import CORS
from .routes import register_routes

def create_app():
    # Inicializa la aplicación Flask
    app = Flask(__name__)

    # Habilitar CORS si lo necesitas
    CORS(app)  

    # Registrar las rutas desde routes.py
    register_routes(app)

    # Añadir el manejador de cierre de la conexión a la base de datos
    @app.teardown_appcontext
    def close_db_connection(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    return app

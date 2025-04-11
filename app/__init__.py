from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Crea y configura la aplicación Flask.
    
    Args:
        config_class: Clase de configuración a utilizar.
        
    Returns:
        app: Aplicación Flask configurada.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Importar y registrar Blueprints
    from app.routes import scraper_bp, api_bp, main_bp
    app.register_blueprint(scraper_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
    
    # Crear la base de datos si no existe
    with app.app_context():
        try:
            db.create_all()
            logger.info("Base de datos creada correctamente.")
        except Exception as e:
            logger.error(f"Error al crear la base de datos: {str(e)}")
    
    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """
    Función factory para crear la aplicación Flask.
    
    Args:
        config_name: Nombre de la configuración a utilizar (default, development, testing, production)
    
    Returns:
        Aplicación Flask configurada
    """
    # Crear instancia de aplicación Flask
    app = Flask(__name__)
    
    # Aplicar configuración
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    from app.views import main_bp
    app.register_blueprint(main_bp)
    
    return app

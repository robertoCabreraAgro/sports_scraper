import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

class Config:
    """Configuración de la aplicación"""
    # Configuración de la base de datos SQLite por defecto
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sports_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-muy-secreta'
    
    # URL base para el scraping
    FOOTBALL_URL = os.environ.get('FOOTBALL_URL') or 'https://livescore.football-data.co.uk/'
    TENNIS_URL = os.environ.get('TENNIS_URL') or 'https://livescore.football-data.co.uk/tennis'
    BASKETBALL_URL = os.environ.get('BASKETBALL_URL') or 'https://livescore.football-data.co.uk/basketball'

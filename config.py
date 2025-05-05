import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://roob:roob1128@localhost:5432/dataDB'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    # URL base para el scraping
    FOOTBALL_URL = os.environ.get('FOOTBALL_URL') or 'https://livescore.football-data.co.uk/'
    TENNIS_URL = os.environ.get('TENNIS_URL') or 'https://livescore.football-data.co.uk/tennis'
    BASKETBALL_URL = os.environ.get('BASKETBALL_URL') or 'https://livescore.football-data.co.uk/basketball'

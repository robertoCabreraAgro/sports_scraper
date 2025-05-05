import os
from app import create_app, db
from app.models import MatchStats
from flask_migrate import upgrade

# Obtener el entorno de configuración
env = os.environ.get('FLASK_ENV', 'default')
app = create_app(env)

@app.shell_context_processor
def make_shell_context():
    """
    Configura el contexto para el shell de Flask.
    Útil para realizar pruebas manuales en la consola.
    """
    return {'db': db, 'MatchStats': MatchStats}

@app.cli.command("init-db")
def init_db():
    """
    Comando para inicializar la base de datos desde la línea de comandos.
    Ejecutar con: flask init-db
    """
    print("Inicializando la base de datos...")
    with app.app_context():
        db.create_all()
    print("Base de datos inicializada correctamente.")

@app.cli.command("test-scraper")
def test_scraper():
    """
    Comando para probar el scraper desde la línea de comandos.
    Ejecutar con: flask test-scraper
    """
    from app.scraper import ScraperFactory
    
    print("Probando el scraper...")
    url = input("Introduce la URL a scrapear: ")
    sport_type = input("Introduce el tipo de deporte (default: tennis): ") or "tennis"
    
    scraper = ScraperFactory.get_scraper(sport_type, url)
    matches = scraper.scrape_matches()
    
    print(f"Se encontraron {len(matches)} partidos:")
    for i, match in enumerate(matches, 1):
        print(f"\nPartido {i}:")
        for key, value in match.items():
            print(f"  {key}: {value}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

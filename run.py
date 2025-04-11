from app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    logging.info("Iniciando la aplicación Flask del Scraper Deportivo")
    app.run(host='0.0.0.0', port=5000, debug=True)
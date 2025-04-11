import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app import db
from app.models import PartidoFutbol, PartidoTenis, PartidoBaloncesto
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def realizar_scraping_futbol():
    """
    Realiza scraping de la página web de fútbol y guarda los datos en la base de datos.
    
    Returns:
        dict: Mensaje de resultado y número de partidos procesados
    """
    try:
        url = Config.FOOTBALL_URL
        logger.info(f"Iniciando scraping de fútbol desde: {url}")
        
        # Hacer la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer los partidos (adaptar según la estructura real de la página)
        partidos = soup.find_all('div', class_='partido')
        
        # Contador de partidos procesados
        contador = 0
        
        for partido in partidos:
            try:
                # Extracción de datos (adaptar a la estructura real)
                competencia = partido.find('h2').text.strip()
                equipos = partido.find_all('span', class_='equipo')
                goles = partido.find_all('span', class_='goles')
                hora = partido.find('span', class_='hora').text.strip()
                
                # URL para detalles del partido (opcional)
                url_detalles = None
                link = partido.find('a')
                if link and link.get('href'):
                    url_detalles = link['href']
                    if not url_detalles.startswith('http'):
                        url_detalles = f"{Config.FOOTBALL_URL.rstrip('/')}/{url_detalles.lstrip('/')}"
                
                # Extraemos la información de los equipos y los goles
                equipo_local = equipos[0].text.strip() if len(equipos) > 0 else "Desconocido"
                equipo_visitante = equipos[1].text.strip() if len(equipos) > 1 else "Desconocido"
                goles_local = int(goles[0].text.strip()) if len(goles) > 0 else 0
                goles_visitante = int(goles[1].text.strip()) if len(goles) > 1 else 0
                
                # Verificar si el partido ya existe en la base de datos
                partido_existente = PartidoFutbol.query.filter_by(
                    competencia=competencia,
                    equipo_local=equipo_local,
                    equipo_visitante=equipo_visitante,
                    hora=hora
                ).first()
                
                if not partido_existente:
                    # Guardar los datos en la base de datos
                    nuevo_partido = PartidoFutbol(
                        competencia=competencia,
                        equipo_local=equipo_local,
                        equipo_visitante=equipo_visitante,
                        goles_local=goles_local,
                        goles_visitante=goles_visitante,
                        hora=hora,
                        url_detalles=url_detalles
                    )
                    db.session.add(nuevo_partido)
                    contador += 1
                else:
                    # Actualizar partido existente si hay cambios
                    if (partido_existente.goles_local != goles_local or 
                        partido_existente.goles_visitante != goles_visitante or
                        partido_existente.url_detalles != url_detalles):
                        partido_existente.goles_local = goles_local
                        partido_existente.goles_visitante = goles_visitante
                        partido_existente.url_detalles = url_detalles
                        contador += 1
            
            except Exception as e:
                logger.error(f"Error procesando un partido de fútbol: {str(e)}")
                continue
        
        # Guardar todos los cambios
        db.session.commit()
        
        return {
            "status": "success",
            "message": f"Scraping completado. Se procesaron {contador} partidos de fútbol.",
            "count": contador
        }
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en el scraping de fútbol: {str(e)}")
        return {
            "status": "error",
            "message": f"Error en el scraping: {str(e)}",
            "count": 0
        }

def realizar_scraping_tenis():
    """
    Realiza scraping de la página web de tenis y guarda los datos en la base de datos.
    
    Returns:
        dict: Mensaje de resultado y número de partidos procesados
    """
    try:
        url = Config.TENNIS_URL
        logger.info(f"Iniciando scraping de tenis desde: {url}")
        
        # Hacer la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()
        
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer los partidos (adaptar según la estructura real de la página)
        partidos = soup.find_all('div', class_='partido-tenis')
        
        # Contador de partidos procesados
        contador = 0
        
        for partido in partidos:
            try:
                # Extracción de datos (adaptar a la estructura real)
                torneo = partido.find('h2').text.strip()
                jugadores = partido.find_all('span', class_='jugador')
                sets = partido.find_all('span', class_='sets')
                hora = partido.find('span', class_='hora').text.strip()
                
                # URL para detalles del partido (opcional)
                url_detalles = None
                link = partido.find('a')
                if link and link.get('href'):
                    url_detalles = link['href']
                    if not url_detalles.startswith('http'):
                        url_detalles = f"{Config.TENNIS_URL.rstrip('/')}/{url_detalles.lstrip('/')}"
                
                jugador1 = jugadores[0].text.strip() if len(jugadores) > 0 else "Desconocido"
                jugador2 = jugadores[1].text.strip() if len(jugadores) > 1 else "Desconocido"
                sets_jugador1 = int(sets[0].text.strip()) if len(sets) > 0 else 0
                sets_jugador2 = int(sets[1].text.strip()) if len(sets) > 1 else 0
                
                # Verificar si el partido ya existe
                partido_existente = PartidoTenis.query.filter_by(
                    torneo=torneo,
                    jugador1=jugador1,
                    jugador2=jugador2,
                    hora=hora
                ).first()
                
                if not partido_existente:
                    # Guardar nuevo partido
                    nuevo_partido = PartidoTenis(
                        torneo=torneo,
                        jugador1=jugador1,
                        jugador2=jugador2,
                        sets_jugador1=sets_jugador1,
                        sets_jugador2=sets_jugador2,
                        hora=hora,
                        url_detalles=url_detalles
                    )
                    db.session.add(nuevo_partido)
                    contador += 1
                else:
                    # Actualizar partido existente si hay cambios
                    if (partido_existente.sets_jugador1 != sets_jugador1 or 
                        partido_existente.sets_jugador2 != sets_jugador2 or
                        partido_existente.url_detalles != url_detalles):
                        partido_existente.sets_jugador1 = sets_jugador1
                        partido_existente.sets_jugador2 = sets_jugador2
                        partido_existente.url_detalles = url_detalles
                        contador += 1
            
            except Exception as e:
                logger.error(f"Error procesando un partido de tenis: {str(e)}")
                continue
        
        # Guardar todos los cambios
        db.session.commit()
        
        return {
            "status": "success",
            "message": f"Scraping completado. Se procesaron {contador} partidos de tenis.",
            "count": contador
        }
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en el scraping de tenis: {str(e)}")
        return {
            "status": "error",
            "message": f"Error en el scraping: {str(e)}",
            "count": 0
        }

def realizar_scraping_baloncesto():
    """
    Realiza scraping de la página web de baloncesto y guarda los datos en la base de datos.
    
    Returns:
        dict: Mensaje de resultado y número de partidos procesados
    """
    try:
        url = Config.BASKETBALL_URL
        logger.info(f"Iniciando scraping de baloncesto desde: {url}")
        
        # Hacer la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()
        
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer los partidos (adaptar según la estructura real de la página)
        partidos = soup.find_all('div', class_='partido-baloncesto')
        
        # Contador de partidos procesados
        contador = 0
        
        for partido in partidos:
            try:
                # Extracción de datos (adaptar a la estructura real)
                liga = partido.find('h2').text.strip()
                equipos = partido.find_all('span', class_='equipo')
                puntos = partido.find_all('span', class_='puntos')
                hora = partido.find('span', class_='hora').text.strip()
                
                # URL para detalles del partido (opcional)
                url_detalles = None
                link = partido.find('a')
                if link and link.get('href'):
                    url_detalles = link['href']
                    if not url_detalles.startswith('http'):
                        url_detalles = f"{Config.BASKETBALL_URL.rstrip('/')}/{url_detalles.lstrip('/')}"
                
                equipo_local = equipos[0].text.strip() if len(equipos) > 0 else "Desconocido"
                equipo_visitante = equipos[1].text.strip() if len(equipos) > 1 else "Desconocido"
                puntos_local = int(puntos[0].text.strip()) if len(puntos) > 0 else 0
                puntos_visitante = int(puntos[1].text.strip()) if len(puntos) > 1 else 0
                
                # Verificar si el partido ya existe
                partido_existente = PartidoBaloncesto.query.filter_by(
                    liga=liga,
                    equipo_local=equipo_local,
                    equipo_visitante=equipo_visitante,
                    hora=hora
                ).first()
                
                if not partido_existente:
                    # Guardar nuevo partido
                    nuevo_partido = PartidoBaloncesto(
                        liga=liga,
                        equipo_local=equipo_local,
                        equipo_visitante=equipo_visitante,
                        puntos_local=puntos_local,
                        puntos_visitante=puntos_visitante,
                        hora=hora,
                        url_detalles=url_detalles
                    )
                    db.session.add(nuevo_partido)
                    contador += 1
                else:
                    # Actualizar partido existente si hay cambios
                    if (partido_existente.puntos_local != puntos_local or 
                        partido_existente.puntos_visitante != puntos_visitante or
                        partido_existente.url_detalles != url_detalles):
                        partido_existente.puntos_local = puntos_local
                        partido_existente.puntos_visitante = puntos_visitante
                        partido_existente.url_detalles = url_detalles
                        contador += 1
            
            except Exception as e:
                logger.error(f"Error procesando un partido de baloncesto: {str(e)}")
                continue
        
        # Guardar todos los cambios
        db.session.commit()
        
        return {
            "status": "success",
            "message": f"Scraping completado. Se procesaron {contador} partidos de baloncesto.",
            "count": contador
        }
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en el scraping de baloncesto: {str(e)}")
        return {
            "status": "error",
            "message": f"Error en el scraping: {str(e)}",
            "count": 0
        }
        
        